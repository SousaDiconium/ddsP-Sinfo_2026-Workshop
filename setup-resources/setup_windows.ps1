# =========================================
# Sinfo 2026 Workshop Setup Script (Windows)
# =========================================

function Write-Section($msg) {
    Write-Host "`n==============================================================" -ForegroundColor Cyan
    Write-Host $msg -ForegroundColor Cyan
    Write-Host "==============================================================`n" -ForegroundColor Cyan
}

function Write-Success($msg) {
    Write-Host "$msg" -ForegroundColor Green
}

function Write-ErrorMsg($msg) {
    Write-Host "$msg" -ForegroundColor Red
}

function Write-Info($msg) {
    Write-Host "$msg" -ForegroundColor Yellow
}

# --- Welcome ---
Write-Section "Sinfo 2026 Workshop Setup (Windows)"
Write-Host "This script will check and help you install the required tools for the workshop."
Write-Host "You may be prompted for admin rights during installations."

# --- Git ---
Write-Section "Git"
# Check if Git is installed
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Success "Git is already installed."
} else {
    Write-Info "Git not found. Please download and install from: https://git-scm.com/install/windows"
    Read-Host "Press Enter after you have installed Git..."
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Write-Success "Git installed successfully."
    } else {
        Write-ErrorMsg "Git installation not detected. Please try again or ask for help."
    }
}

# --- Docker ---
Write-Section "Docker"
# Check if Docker is installed
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Success "Docker is already installed."
} else {
    Write-Info "Docker not found. Please download and install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    Read-Host "Press Enter after you have installed Docker Desktop..."
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        Write-Success "Docker installed successfully."
    } else {
        Write-ErrorMsg "Docker installation not detected. Please try again or ask for help."
    }
}

# --- UV ---
Write-Section "UV (Python + Package Manager)"
# Check if UV is installed
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Success "UV is already installed."
} else {
    Write-Info "UV not found. Installing using official script..."
    # Install UV (official method)
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    Read-Host "Press Enter after the UV installation completes..."
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        Write-Success "UV installed successfully."
    } else {
        Write-ErrorMsg "UV installation not detected. Please try again or ask for help."
    }
}

# --- VS Code ---
Write-Section "Visual Studio Code"
# Check if VS Code is installed
if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Success "VS Code is already installed."
} else {
    Write-Info "VS Code not found or at least its alias 'code' is not available."
    Write-Info "Please download and install VS Code from: https://code.visualstudio.com/download"
    Read-Host "Press Enter after you have installed VS Code..."
    if (Get-Command code -ErrorAction SilentlyContinue) {
        Write-Success "VS Code installed successfully."
    } else {
        Write-ErrorMsg "VS Code installation failed or 'code' command is not available. Check if you can open VS Code."
    }
}

# --- Chromium-Based Browser ---
Write-Section "Chromium-Based Browser"
$chromiumFound = $false
$chromePaths = @(
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
)
$bravePaths = @(
    "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\Application\brave.exe",
    "$env:ProgramFiles\BraveSoftware\Brave-Browser\Application\brave.exe"
)
$edgePaths = @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
)
$chromiumPaths = @(
    "$env:LOCALAPPDATA\Chromium\Application\chrome.exe"
)
foreach ($path in $chromePaths) { if (Test-Path $path) { $chromiumFound = $true; Write-Success "Google Chrome is installed."; break } }
if (-not $chromiumFound) { foreach ($path in $bravePaths)   { if (Test-Path $path) { $chromiumFound = $true; Write-Success "Brave Browser is installed."; break } } }
if (-not $chromiumFound) { foreach ($path in $edgePaths)    { if (Test-Path $path) { $chromiumFound = $true; Write-Success "Microsoft Edge is installed."; break } } }
if (-not $chromiumFound -and (Get-Command msedge -ErrorAction SilentlyContinue)) { $chromiumFound = $true; Write-Success "Microsoft Edge is installed." }
if (-not $chromiumFound) { foreach ($path in $chromiumPaths) { if (Test-Path $path) { $chromiumFound = $true; Write-Success "Chromium is installed."; break } } }
if (-not $chromiumFound) {
    Write-ErrorMsg "No Chromium-based browser found. OpenClaw requires one of: Chrome, Brave, Edge, or Chromium."
    Write-Info "Please install one of:"
    Write-Info "  • Google Chrome: https://www.google.com/chrome/"
    Write-Info "  • Brave: https://brave.com/"
    Write-Info "  • Microsoft Edge: https://www.microsoft.com/edge"
    Write-Info "  • Chromium: https://www.chromium.org/getting-involved/download-chromium/"
}

# --- OpenClaw ---
Write-Section "OpenClaw"
# Check if OpenClaw is installed
if (Get-Command openclaw -ErrorAction SilentlyContinue) {
    Write-Success "OpenClaw is already installed."
} else {
    Write-Info "OpenClaw not found. Installing using the official script..."
    # Install OpenClaw (official method)
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
    if (Get-Command openclaw -ErrorAction SilentlyContinue) {
        Write-Success "OpenClaw installed successfully."
    } else {
        Write-ErrorMsg "OpenClaw installation not detected. Please try again or ask for help."
    }
}

# --- Done ---
Write-Section "Setup Complete!"
Write-Host "If you saw all green check marks, you are ready for the workshop!"
Write-Host "If you had any issues, please ask for help during the workshop setup session."
