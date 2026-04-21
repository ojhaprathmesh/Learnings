# run_pipeline.ps1
# ================
# Full pipeline runner for the CADI-AI Deep Learning Assignment.
# Run from the Assignment-1 directory:
#     .\run_pipeline.ps1
#
# Each step prints status.  You can run steps individually too.

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$PSNativeCommandUseErrorActionPreference = $true

# Fix Windows console encoding for Unicode output
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CADI-AI Assignment Pipeline" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# -----------------------------------------------------------------
# Step 0: Sanitize labels
# -----------------------------------------------------------------
Write-Host "[Step 0/6] Sanitizing YOLO labels..." -ForegroundColor Yellow
python "$Root\00_sanitize_labels.py"
if ($LASTEXITCODE -ne 0) { throw "Label sanitization failed." }
Write-Host "  OK" -ForegroundColor Green

# -----------------------------------------------------------------
# Step 1: Install dependencies
# -----------------------------------------------------------------
Write-Host ""
Write-Host "[Step 1/5] Installing Python dependencies..." -ForegroundColor Yellow
pip install -r "$Root\requirements.txt" --quiet
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }

# Ensure CUDA-enabled PyTorch for RTX laptop GPUs.
# requirements.txt intentionally excludes torch/torchvision so this remains stable.
Write-Host "  Installing CUDA PyTorch wheels (cu121)..." -ForegroundColor Gray
pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --quiet
if ($LASTEXITCODE -ne 0) { throw "CUDA PyTorch installation failed." }
python -c "import torch; assert torch.cuda.is_available(), 'CUDA not visible to torch'; print('  torch:', torch.__version__, '| cuda:', torch.version.cuda)"
if ($LASTEXITCODE -ne 0) { throw "CUDA validation failed after PyTorch install." }
Write-Host "  OK" -ForegroundColor Green

# -----------------------------------------------------------------
# Step 2: Dataset exploration
# -----------------------------------------------------------------
Write-Host ""
Write-Host "[Step 2/5] Running dataset exploration..." -ForegroundColor Yellow
python "$Root\01_explore_dataset.py"
if ($LASTEXITCODE -ne 0) { throw "Dataset exploration failed." }
Write-Host "  OK" -ForegroundColor Green

# -----------------------------------------------------------------
# Step 3: Baseline training
# -----------------------------------------------------------------
Write-Host ""
Write-Host "[Step 3/5] Training baseline YOLOv8n (32 epochs)..." -ForegroundColor Yellow
Write-Host "  This may take 30-90 minutes on a GPU." -ForegroundColor Gray
python "$Root\02_train_baseline.py"
if ($LASTEXITCODE -ne 0) { throw "Baseline training failed." }
Write-Host "  OK" -ForegroundColor Green

# -----------------------------------------------------------------
# Step 4: Custom YOLO-TRP training
# -----------------------------------------------------------------
Write-Host ""
Write-Host "[Step 4/5] Training YOLO-TRP (32 epochs)..." -ForegroundColor Yellow
python "$Root\03_train_custom.py"
if ($LASTEXITCODE -ne 0) { throw "YOLO-TRP training failed." }
Write-Host "  OK" -ForegroundColor Green

# -----------------------------------------------------------------
# Step 5: Evaluation + Comparison
# -----------------------------------------------------------------
Write-Host ""
Write-Host "[Step 5/5] Evaluating models and generating comparison..." -ForegroundColor Yellow
python "$Root\04_evaluate.py"
if ($LASTEXITCODE -ne 0) { throw "Evaluation failed." }
python "$Root\05_compare_results.py"
if ($LASTEXITCODE -ne 0) { throw "Comparison report generation failed." }
Write-Host "  OK" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Pipeline complete!" -ForegroundColor Green
Write-Host "  Results  : $Root\results\" -ForegroundColor Cyan
Write-Host "  Runs     : $Root\runs\detect\" -ForegroundColor Cyan
Write-Host "  Report   : $Root\report\report.tex" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
