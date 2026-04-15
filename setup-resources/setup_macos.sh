#!/bin/bash
# =========================================
# 🚀 Sinfo 2026 Workshop Setup Script (macOS)
# =========================================

# --- Styling helpers ---
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

print_section() {
  echo -e "${BLUE}\n=============================================================="
  echo -e "$1"
  echo -e "==============================================================${NC}"
}

print_success() {
  echo -e "${GREEN}✔ $1${NC}"
}

print_error() {
  echo -e "${RED}✖ $1${NC}"
}

print_info() {
  echo -e "${YELLOW}➜ $1${NC}"
}

# --- Welcome ---
print_section "🚀 Sinfo 2026 Workshop Setup (macOS)"
echo "This script will check and help you install the required tools for the workshop."
echo "You may be prompted for your password during installations."

# --- Check for Homebrew ---
print_section "🍺 Checking Homebrew"
if ! command -v brew &> /dev/null; then
  print_error "Homebrew is not installed."
  read -p "Would you like to install Homebrew now? (y/n): " install_brew
  if [[ "$install_brew" =~ ^[Yy]$ ]]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if command -v brew &> /dev/null; then
      print_success "Homebrew installed successfully."
    else
      print_error "Homebrew installation failed. Please install manually from https://brew.sh/"
      exit 1
    fi
  else
    print_info "Please install Homebrew manually from https://brew.sh/ and re-run this script."
    exit 1
  fi
else
  print_success "Homebrew is installed."
fi

# --- Git ---
print_section "🐙 Git"
# Check if Git is installed
if command -v git &> /dev/null; then
  print_success "Git is already installed."
else
  print_info "Git not found. Installing with Homebrew..."
  # Install Git (update this command if needed)
  brew install git
  # Check again
  if command -v git &> /dev/null; then
    print_success "Git installed successfully."
  else
    print_error "Git installation failed. Please install manually."
  fi
fi

# --- Docker ---
print_section "🐳 Docker"
# Check if Docker is installed
if command -v docker &> /dev/null; then
  print_success "Docker is already installed."
else
  print_info "Docker not found. Please download and install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
  read -p "Press Enter after you have installed Docker Desktop..."
  # Check again
  if command -v docker &> /dev/null; then
    print_success "Docker installed successfully."
  else
    print_error "Docker installation not detected. Please try again or ask for help."
  fi
fi

# --- UV ---
print_section "🐍 UV (Python + Package Manager)"
# Check if UV is installed
if command -v uv &> /dev/null; then
  print_success "UV is already installed."
else
  print_info "UV not found. Installing using the official script..."
  # Install UV (official method)
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Check again
  if command -v uv &> /dev/null; then
    print_success "UV installed successfully."
  else
    print_error "UV installation failed. Please install manually."
  fi
fi

# --- VS Code ---
print_section "📝 Visual Studio Code"
# Check if VS Code is installed
if command -v code &> /dev/null; then
  print_success "VS Code is already installed."
else
  print_info "VS Code not found or at least its alias 'code' is not available."
  print_info "Please download and install VS Code from: https://code.visualstudio.com/download"
  read -p "Press Enter after you have installed VS Code..."
  # Check again
  if command -v code &> /dev/null; then
    print_success "VS Code installed successfully."
  else
    print_error "VS Code installation failed or 'code' command is not available. Check if you can open VS Code."
  fi
fi

# --- Chromium-Based Browser ---
print_section "🌐 Chromium-Based Browser"
CHROMIUM_FOUND=false
if [ -d "/Applications/Google Chrome.app" ] || command -v google-chrome &> /dev/null || command -v google-chrome-stable &> /dev/null; then
  print_success "Google Chrome is installed."
  CHROMIUM_FOUND=true
elif [ -d "/Applications/Brave Browser.app" ] || command -v brave-browser &> /dev/null; then
  print_success "Brave Browser is installed."
  CHROMIUM_FOUND=true
elif [ -d "/Applications/Microsoft Edge.app" ] || command -v microsoft-edge &> /dev/null; then
  print_success "Microsoft Edge is installed."
  CHROMIUM_FOUND=true
elif [ -d "/Applications/Chromium.app" ] || command -v chromium &> /dev/null || command -v chromium-browser &> /dev/null; then
  print_success "Chromium is installed."
  CHROMIUM_FOUND=true
fi
if [ "$CHROMIUM_FOUND" = false ]; then
  print_error "No Chromium-based browser found. OpenClaw requires one of: Chrome, Brave, Edge, or Chromium."
  print_info "Please install one of:"
  print_info "  • Google Chrome: https://www.google.com/chrome/"
  print_info "  • Brave: https://brave.com/"
  print_info "  • Microsoft Edge: https://www.microsoft.com/edge"
  print_info "  • Chromium: https://www.chromium.org/getting-involved/download-chromium/"
fi

# --- OpenClaw ---
print_section "🦞 OpenClaw"
# Check if OpenClaw is installed
if command -v openclaw &> /dev/null; then
  print_success "OpenClaw is already installed."
else
  print_info "OpenClaw not found. Installing using the official script..."
  # Install OpenClaw (official method)
  curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
  # Check again
  if command -v openclaw &> /dev/null; then
    print_success "OpenClaw installed successfully."
  else
    print_error "OpenClaw installation not detected. Please try again or ask for help."
  fi
fi

# --- Done ---
print_section "✅ Setup Complete!"
echo "If you saw all green check marks, you are ready for the workshop!"
echo "If you had any issues, please ask for help during the workshop setup session."
