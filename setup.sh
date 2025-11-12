#!/bin/bash

# Mazoon Platform - Automated Setup Script
# مزون - برنامج الإعداد التلقائي

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  Mazoon Platform - Setup Script | مزون - برنامج الإعداد ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main setup
print_header

# Step 1: Check Python
print_step "Checking Python installation..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed"
    print_info "Please install Python 3.7 or higher"
    exit 1
fi

# Step 2: Check pip
print_step "Checking pip installation..."
if command_exists pip3; then
    print_success "pip found"
else
    print_error "pip is not installed"
    print_info "Installing pip..."
    python3 -m ensurepip --default-pip
fi

# Step 3: Create virtual environment (optional)
read -p "Create virtual environment? (recommended) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    print_step "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    print_success "Virtual environment created and activated"
fi

# Step 4: Install dependencies
print_step "Installing dependencies..."
pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt
print_success "Dependencies installed"

# Step 5: Initialize database
print_step "Initializing database..."
python3 init_database.py
print_success "Database initialized"

# Step 6: Verify database
print_step "Verifying database..."
python3 verify_database.py > /dev/null 2>&1
print_success "Database verified"

# Step 7: Run tests
read -p "Run tests? [y/N]: " run_tests
if [[ $run_tests =~ ^[Yy]$ ]]; then
    print_step "Running tests..."
    python3 test_all_crud.py
    print_success "Tests completed"
fi

# Final message
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         ✅ Setup Complete! | الإعداد مكتمل! ✅           ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
print_info "To start the API server, run:"
echo -e "  ${BLUE}python3 api.py${NC}"
echo ""
print_info "To test the API, open in your browser:"
echo -e "  ${BLUE}test_api.html${NC}"
echo ""
print_info "API will be available at:"
echo -e "  ${BLUE}http://localhost:5000${NC}"
echo ""
print_info "Health check:"
echo -e "  ${BLUE}curl http://localhost:5000/health${NC}"
echo ""
echo -e "${YELLOW}For more information, see README.md${NC}"
echo ""
