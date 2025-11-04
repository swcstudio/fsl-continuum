#!/bin/bash
# FSL Continuum UVX Environment Setup Script
# Complete UVX virtual environment setup for testing and development

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if UVX is installed
check_uvx() {
    log_info "Checking UVX installation..."
    
    if ! command -v uvx &> /dev/null; then
        log_error "UVX is not installed. Please install UVX first:"
        log_error "pip install uvx"
        exit 1
    fi
    
    UVX_VERSION=$(uvx --version)
    log_success "UVX installed: $UVX_VERSION"
}

# Create UVX directory structure
create_directories() {
    log_info "Creating UVX directory structure..."
    
    directories=(
        ".uvx"
        ".uvx/cache"
        ".uvx/environments"
        ".uvx/logs"
        ".uvx/scripts"
        ".uvx/artifacts"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_success "Created directory: $dir"
        else
            log_info "Directory already exists: $dir"
        fi
    done
}

# Create UVX environments
create_environments() {
    log_info "Creating UVX environments..."
    
    # Create production environment
    log_info "Creating fsl-continuum production environment..."
    if ! uvx list fsl-continuum &> /dev/null; then
        uvx create fsl-continuum --python 3.11 --description "FSL Continuum Production Environment"
        log_success "Created fsl-continuum production environment"
    else
        log_info "fsl-continuum production environment already exists"
    fi
    
    # Create development environment
    log_info "Creating fsl-continuum-dev development environment..."
    if ! uvx list fsl-continuum-dev &> /dev/null; then
        uvx create fsl-continuum-dev --python 3.11 --dev --description "FSL Continuum Development Environment"
        log_success "Created fsl-continuum-dev development environment"
    else
        log_info "fsl-continuum-dev development environment already exists"
    fi
    
    # Create testing environment
    log_info "Creating fsl-continuum-test testing environment..."
    if ! uvx list fsl-continuum-test &> /dev/null; then
        uvx create fsl-continuum-test --python 3.11 --test --description "FSL Continuum Testing Environment"
        log_success "Created fsl-continuum-test testing environment"
    else
        log_info "fsl-continuum-test testing environment already exists"
    fi
    
    # Create coverage environment
    log_info "Creating fsl-continuum-coverage coverage environment..."
    if ! uvx list fsl-continuum-coverage &> /dev/null; then
        uvx create fsl-continuum-coverage --python 3.11 --coverage --description "FSL Continuum Coverage Testing Environment"
        log_success "Created fsl-continuum-coverage coverage environment"
    else
        log_info "fsl-continuum-coverage coverage environment already exists"
    fi
    
    # Create performance environment
    log_info "Creating fsl-continuum-performance performance environment..."
    if ! uvx list fsl-continuum-performance &> /dev/null; then
        uvx create fsl-continuum-performance --python 3.11 --performance --description "FSL Continuum Performance Testing Environment"
        log_success "Created fsl-continuum-performance performance environment"
    else
        log_info "fsl-continuum-performance performance environment already exists"
    fi
}

# Install FSL Continuum in environments
install_fsl_continuum() {
    log_info "Installing FSL Continuum in UVX environments..."
    
    # Install in production environment
    log_info "Installing FSL Continuum in production environment..."
    uvx install fsl-continuum --python 3.11 --environment fsl-continuum
    log_success "Installed FSL Continuum in production environment"
    
    # Install in development environment
    log_info "Installing FSL Continuum in development environment..."
    uvx install fsl-continuum --python 3.11 --dev --environment fsl-continuum-dev
    log_success "Installed FSL Continuum in development environment"
    
    # Install in testing environment
    log_info "Installing FSL Continuum in testing environment..."
    uvx install fsl-continuum --python 3.11 --test --environment fsl-continuum-test
    log_success "Installed FSL Continuum in testing environment"
    
    # Install in coverage environment
    log_info "Installing FSL Continuum in coverage environment..."
    uvx install fsl-continuum --python 3.11 --coverage --environment fsl-continuum-coverage
    log_success "Installed FSL Continuum in coverage environment"
    
    # Install in performance environment
    log_info "Installing FSL Continuum in performance environment..."
    uvx install fsl-continuum --python 3.11 --performance --environment fsl-continuum-performance
    log_success "Installed FSL Continuum in performance environment"
}

# Validate UVX setup
validate_setup() {
    log_info "Validating UVX setup..."
    
    # Check if all environments exist
    environments=("fsl-continuum" "fsl-continuum-dev" "fsl-continuum-test" "fsl-continuum-coverage" "fsl-continuum-performance")
    
    for env in "${environments[@]}"; do
        if uvx list "$env" &> /dev/null; then
            log_success "Environment $env exists"
        else
            log_error "Environment $env does not exist"
            exit 1
        fi
    done
    
    # Test import in production environment
    log_info "Testing FSL Continuum import in production environment..."
    if uvx run --python 3.11 fsl-continuum python -c "import fsl_continuum; print(fsl_continuum.get_version())" &> /dev/null; then
        log_success "FSL Continuum import works in production environment"
    else
        log_error "FSL Continuum import failed in production environment"
        exit 1
    fi
    
    # Test import in testing environment
    log_info "Testing FSL Continuum import in testing environment..."
    if uvx run --python 3.11 --test fsl-continuum python -c "import fsl_continuum; print('Testing import successful')" &> /dev/null; then
        log_success "FSL Continuum import works in testing environment"
    else
        log_error "FSL Continuum import failed in testing environment"
        exit 1
    fi
}

# Create UVX scripts
create_scripts() {
    log_info "Creating UVX scripts..."
    
    # Make scripts executable
    chmod +x .uvx/scripts/*.sh
    
    log_success "Created UVX scripts"
}

# Main function
main() {
    echo "🔧 FSL Continuum UVX Environment Setup"
    echo "=================================="
    
    # Change to project root
    cd "$(dirname "$0")/../.."
    
    log_info "Setting up UVX environments for FSL Continuum..."
    
    check_uvx
    create_directories
    create_environments
    install_fsl_continuum
    validate_setup
    create_scripts
    
    echo "=================================="
    log_success "UVX environment setup complete!"
    echo ""
    log_info "Available UVX environments:"
    uvx list
    
    echo ""
    log_info "Usage examples:"
    echo "  uvx run --python 3.11 fsl-continuum                    # Production environment"
    echo "  uvx run --python 3.11 --dev fsl-continuum             # Development environment"
    echo "  uvx run --python 3.11 --test fsl-continuum            # Testing environment"
    echo "  uvx run --python 3.11 --coverage fsl-continuum       # Coverage environment"
    echo "  uvx run --python 3.11 --performance fsl-continuum    # Performance environment"
    echo ""
    echo "  .uvx/scripts/run_tests.sh                              # Run all tests"
    echo "  .uvx/scripts/run_performance_tests.sh                  # Run performance tests"
    echo "  .uvx/scripts/run_coverage_tests.sh                      # Run coverage tests"
    
    echo ""
    log_success "Ready to run tests with UVX!"
}

# Run main function
main "$@"
