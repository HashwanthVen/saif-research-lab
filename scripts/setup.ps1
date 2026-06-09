# Windows environment bootstrap
$ErrorActionPreference = "Stop"
Write-Host "Bootstrapping saif-research-lab on Windows..."

# Conda env (assumes miniconda/conda is on PATH)
if (Get-Command conda -ErrorAction SilentlyContinue) {
    conda create -y -n saif-research python=3.11
    Write-Host "Activate with: conda activate saif-research"
} else {
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
}

pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cu124
pip install transformers accelerate peft bitsandbytes datasets sentencepiece
pip install arxiv pyyaml jsonschema pytest black ruff matplotlib pandas
pip install sae-lens wandb

Write-Host "Done. Run a paper with: python scripts/run_paper.py 01"
