<#
.SYNOPSIS
    Deterministic, idempotent, resumable evaluation runner for cross-model LLM
    benchmarks using the GitHub Copilot CLI.

.DESCRIPTION
    Iterates over the Cartesian product of prompts x models x seeds. For each
    (prompt, model, seed) tuple it computes a stable SHA-256 work_id, checks
    whether the output already exists (resume support), and if not, invokes
    `copilot -p <prompt> --model <cli_id>` (or your configured CLI command),
    capturing stdout, stderr, exit code, wall time, and full provenance.

    Each completed run is written to a single JSON file named by work_id in
    the configured output directory. Aggregation is done by a separate Python
    script (aggregate_results.py) so this script never re-reads its own output.

.PARAMETER PromptsFile
    Path to JSONL file with one prompt per line. Required fields per line:
      prompt_id, domain, prompt_text.

.PARAMETER ModelsFile
    Path to JSON file with a `models` array. Only entries with include=true run.

.PARAMETER OutputDir
    Directory where per-run JSON files are written. Created if missing.

.PARAMETER NumSeeds
    Independent invocations per (prompt, model). Default 3.
    LLMs are nondeterministic; 3 seeds lets us measure response stability.

.PARAMETER Resume
    Skip any (prompt, model, seed) whose output JSON already exists.

.PARAMETER DryRun
    Print work plan, do not invoke CLI or write outputs.

.PARAMETER Models, Prompts
    Comma-separated subset filters (overrides include flag / runs subset).

.EXAMPLE
    .\eval_runner.ps1 -DryRun
    .\eval_runner.ps1 -Resume
    .\eval_runner.ps1 -Models "claude-opus-4.7-high" -Prompts "med-001" -NumSeeds 1

.NOTES
    Determinism contract:
      - Same prompts.jsonl + models.json + seed set -> same work_id set
      - work_id = first 16 hex of SHA-256(prompt_id + "\0" + cli_id + "\0" + seed)
      - Outputs are idempotent: re-running with -Resume produces no new files
      - LLM sampling is NOT deterministic; we capture N seeds to quantify drift
#>

[CmdletBinding()]
param(
    [string]$PromptsFile = (Join-Path $PSScriptRoot "..\configs\prompts_sample.jsonl"),
    [string]$ModelsFile  = (Join-Path $PSScriptRoot "..\configs\models.json"),
    [string]$OutputDir   = (Join-Path $PSScriptRoot "..\..\results\runs"),
    [int]$NumSeeds       = 3,
    [string]$CliCommand  = "copilot",
    [string]$PromptArg   = "-p",
    [string]$ModelArg    = "--model",
    [int]$TimeoutSec     = 600,
    [switch]$Resume,
    [switch]$DryRun,
    [string]$Models      = "",
    [string]$Prompts     = "",
    [string]$LogFile     = ""
)

$ErrorActionPreference = "Stop"
$ProgressPreference    = "SilentlyContinue"

function Compute-WorkId {
    param([string]$PromptId, [string]$CliId, [int]$Seed)
    $key = "$PromptId`0$CliId`0$Seed"
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $bytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($key))
    return ([System.BitConverter]::ToString($bytes) -replace '-','').ToLower().Substring(0, 16)
}

function Get-IsoUtc {
    return (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
}

function Write-Log {
    param([string]$Line)
    Write-Host $Line
    if ($LogFile) {
        Add-Content -Path $LogFile -Value "$(Get-IsoUtc)`t$Line"
    }
}

function Invoke-CliOnce {
    param(
        [string]$Cli,
        [string]$ModelId,
        [string]$PromptText,
        [int]$TimeoutSeconds,
        [string]$PromptFlag,
        [string]$ModelFlag
    )
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

    # If Cli ends in .ps1, wrap with pwsh -File for Start-Process compatibility.
    # Otherwise use Start-Job so we get a clean timeout + captured stdout/stderr.
    $job = Start-Job -ScriptBlock {
        param($CliPath, $PFlag, $PText, $MFlag, $MId)
        $out = & $CliPath $PFlag $PText $MFlag $MId --no-color 2>&1
        # Separate exit code from output
        [pscustomobject]@{
            output    = ($out | Out-String)
            exit_code = $LASTEXITCODE
        }
    } -ArgumentList $Cli, $PromptFlag, $PromptText, $ModelFlag, $ModelId

    $completed = Wait-Job -Job $job -Timeout $TimeoutSeconds
    $stopwatch.Stop()

    if (-not $completed) {
        Stop-Job -Job $job -ErrorAction SilentlyContinue
        Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
        return [pscustomobject]@{
            stdout       = ""
            stderr       = "TIMEOUT after $TimeoutSeconds s"
            exit_code    = -9
            timed_out    = $true
            duration_sec = [math]::Round($stopwatch.Elapsed.TotalSeconds, 3)
        }
    }

    $result = Receive-Job -Job $job -ErrorAction SilentlyContinue
    $jobErr = $job.ChildJobs[0].Error | Out-String
    Remove-Job -Job $job -Force -ErrorAction SilentlyContinue

    return [pscustomobject]@{
        stdout       = ($result.output -as [string])
        stderr       = $jobErr
        exit_code    = ($result.exit_code -as [int])
        timed_out    = $false
        duration_sec = [math]::Round($stopwatch.Elapsed.TotalSeconds, 3)
    }
}

# -------- main --------

if (-not (Test-Path $PromptsFile)) { throw "Prompts file not found: $PromptsFile" }
if (-not (Test-Path $ModelsFile))  { throw "Models file not found: $ModelsFile" }
if (-not (Test-Path $OutputDir))   { New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null }
if (-not $LogFile) { $LogFile = Join-Path $OutputDir "_progress.tsv" }

$promptList = @(Get-Content $PromptsFile | Where-Object { $_.Trim() -ne "" } | ForEach-Object { $_ | ConvertFrom-Json })
$modelDoc = Get-Content -Raw $ModelsFile | ConvertFrom-Json
$modelList = @($modelDoc.models | Where-Object { $_.include -eq $true })

if ($Models -ne "") {
    $mfilter = $Models -split ',' | ForEach-Object { $_.Trim() }
    $modelList = @($modelDoc.models | Where-Object { $mfilter -contains $_.cli_id })
}
if ($Prompts -ne "") {
    $pfilter = $Prompts -split ',' | ForEach-Object { $_.Trim() }
    $promptList = @($promptList | Where-Object { $pfilter -contains $_.prompt_id })
}

$seeds = 0..($NumSeeds - 1)
$totalWork = $promptList.Count * $modelList.Count * $seeds.Count

Write-Log "=== eval_runner.ps1 ==="
Write-Log "PromptsFile : $PromptsFile  ($($promptList.Count) prompts)"
Write-Log "ModelsFile  : $ModelsFile   ($($modelList.Count) models)"
Write-Log "OutputDir   : $OutputDir"
Write-Log "NumSeeds    : $NumSeeds   TotalWork: $totalWork"
Write-Log "Resume=$Resume  DryRun=$DryRun"
Write-Log "CLI         : $CliCommand $PromptArg <prompt> $ModelArg <model>"

if (-not $DryRun) {
    $cliPath = Get-Command $CliCommand -ErrorAction SilentlyContinue
    if (-not $cliPath) {
        throw "CLI not found in PATH: '$CliCommand'. Override with -CliCommand <path>."
    }
    Write-Log "CLIPath     : $($cliPath.Source)"
}

# Plan
$plan = New-Object System.Collections.ArrayList
$skipped = 0
foreach ($prompt in $promptList) {
    foreach ($model in $modelList) {
        foreach ($seed in $seeds) {
            $wid = Compute-WorkId $prompt.prompt_id $model.cli_id $seed
            $outFile = Join-Path $OutputDir "$wid.json"
            if ($Resume -and (Test-Path $outFile)) { $skipped++; continue }
            $null = $plan.Add([pscustomobject]@{
                work_id    = $wid
                prompt_id  = $prompt.prompt_id
                domain     = $prompt.domain
                cli_id     = $model.cli_id
                display    = $model.display
                seed       = $seed
                out_file   = $outFile
                prompt_obj = $prompt
                model_obj  = $model
            })
        }
    }
}

Write-Log ("Planned     : {0} runs ({1} skipped via resume)" -f $plan.Count, $skipped)

if ($DryRun) {
    foreach ($p in $plan | Select-Object -First 5) {
        Write-Log ("DRYRUN  {0}  {1,-30} {2,-30} seed={3}" -f $p.work_id, $p.prompt_id, $p.cli_id, $p.seed)
    }
    if ($plan.Count -gt 5) { Write-Log "  (... $($plan.Count - 5) more)" }
    Write-Log "DryRun complete."
    return
}

# Execute
$completed = 0
$failed    = 0
$idx       = 0
foreach ($item in $plan) {
    $idx++
    $startUtc = Get-IsoUtc

    Write-Log ("[{0}/{1}] {2}  {3,-26} {4,-30} seed={5} ..." -f `
        $idx, $plan.Count, $item.work_id, $item.prompt_id, $item.cli_id, $item.seed)

    $result = Invoke-CliOnce -Cli $CliCommand `
                             -ModelId $item.cli_id `
                             -PromptText $item.prompt_obj.prompt_text `
                             -TimeoutSeconds $TimeoutSec `
                             -PromptFlag $PromptArg `
                             -ModelFlag $ModelArg

    $record = [ordered]@{
        work_id        = $item.work_id
        prompt_id      = $item.prompt_id
        domain         = $item.domain
        difficulty     = $item.prompt_obj.difficulty
        cli_id         = $item.cli_id
        display        = $item.display
        tier           = $item.model_obj.tier
        thinking       = $item.model_obj.thinking
        seed           = $item.seed
        prompt_text    = $item.prompt_obj.prompt_text
        response_text  = $result.stdout
        stderr         = $result.stderr
        exit_code      = $result.exit_code
        timed_out      = $result.timed_out
        duration_sec   = $result.duration_sec
        started_at     = $startUtc
        finished_at    = (Get-IsoUtc)
        cli_invocation = "$CliCommand $PromptArg <prompt> $ModelArg $($item.cli_id) --no-color"
        machine        = $env:COMPUTERNAME
        user           = $env:USERNAME
        ps_version     = $PSVersionTable.PSVersion.ToString()
        script_version = "eval_runner.ps1 v1.0.0"
    }

    ($record | ConvertTo-Json -Depth 6) | Set-Content -Path $item.out_file -Encoding utf8

    if ($result.exit_code -eq 0 -and -not $result.timed_out) {
        $completed++
        Write-Log ("  OK   exit=0 dur={0}s out={1}b" -f $result.duration_sec, ($result.stdout.Length))
    } else {
        $failed++
        Write-Log ("  FAIL exit={0} timed_out={1} dur={2}s" -f $result.exit_code, $result.timed_out, $result.duration_sec)
    }
}

Write-Log ""
Write-Log "=== Done ==="
Write-Log "Completed   : $completed"
Write-Log "Failed      : $failed"
Write-Log "Skipped     : $skipped (resume)"
Write-Log "Output dir  : $OutputDir"
Write-Log "Progress log: $LogFile"
Write-Log ""
Write-Log "Next: python ..\src\aggregate_results.py --runs-dir $OutputDir"
