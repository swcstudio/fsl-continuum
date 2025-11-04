#!/bin/bash
# FSL Continuum UVX Test Execution Script
# Complete test execution using UVX virtual environments

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

log_test() {
    echo -e "${CYAN}[TEST]${NC} $1"
}

# Configuration
PYTHON_VERSION="3.11"
PROJECT_NAME="fsl-continuum"
TEST_OUTPUT_DIR="test_results"
COVERAGE_DIR="htmlcov"

# Test execution counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# Function to run UVX test
run_uvx_test() {
    local test_name="$1"
    local test_command="$2"
    local test_description="$3"
    local test_type="$4"
    
    log_step "Running ${test_name} tests..."
    log_info "${test_description}"
    
    # Create output directory
    mkdir -p "${TEST_OUTPUT_DIR}/${test_type}"
    
    # Set environment variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    export PYTEST_CURRENT_TEST="${test_name}"
    export PYTEST_PLUGINS="pytest-cov pytest-mock pytest-benchmark"
    
    # Execute test
    if uvx run --python "${PYTHON_VERSION}" --test "${PROJECT_NAME}" ${test_command} 2>&1 | \
       tee "${TEST_OUTPUT_DIR}/${test_type}/${test_name}.log"; then
        
        log_success "${test_name} tests passed!"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        
        # Check if coverage was generated
        if [ -f "coverage.xml" ]; then
            cp coverage.xml "${TEST_OUTPUT_DIR}/${test_type}/${test_name}_coverage.xml"
        fi
        
        # Check if benchmarks were generated
        if [ -f "benchmark.json" ]; then
            cp benchmark.json "${TEST_OUTPUT_DIR}/${test_type}/${test_name}_benchmark.json"
        fi
        
        return 0
    else
        log_error "${test_name} tests failed!"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Function to run tests with specific markers
run_marked_tests() {
    local test_name="$1"
    local markers="$2"
    local test_description="$3"
    
    run_uvx_test "${test_name}" "pytest src/tests/ -v -m '${markers}' --cov=src --cov-report=html --cov-report=xml --cov-report=term-missing --junitxml=${TEST_OUTPUT_DIR}/${test_name}.xml" "${test_description}" "${test_name}"
}

# Function to run specific test files
run_test_files() {
    local test_name="$1"
    local test_files="$2"
    local test_description="$3"
    
    run_uvx_test "${test_name}" "pytest ${test_files} -v --cov=src --cov-report=html --cov-report=xml --cov-report=term-missing --junitxml=${TEST_OUTPUT_DIR}/${test_name}.xml" "${test_description}" "${test_name}"
}

# Function to run performance tests
run_performance_tests() {
    local test_name="$1"
    local test_files="$2"
    local test_description="$3"
    
    run_uvx_test "${test_name}" "pytest ${test_files} -v -m performance --benchmark-only --benchmark-json=${TEST_OUTPUT_DIR}/performance/${test_name}_benchmark.json --benchmark-sort=min" "${test_description}" "performance"
}

# Check UVX installation
check_uvx() {
    log_info "Checking UVX installation..."
    
    if ! command -v uvx &> /dev/null; then
        log_error "UVX is not installed. Please install UVX first:"
        log_error "pip install uvx"
        exit 1
    fi
    
    UVX_VERSION=$(uvx --version)
    log_success "UVX installed: ${UVX_VERSION}"
}

# Check UVX environment
check_uvx_environment() {
    log_info "Checking UVX environment..."
    
    # Check if test environment exists
    if ! uvx list "${PROJECT_NAME}-test" &> /dev/null; then
        log_warning "UVX test environment not found. Creating..."
        uvx create "${PROJECT_NAME}-test" --python "${PYTHON_VERSION}" --test --description "FSL Continuum Testing Environment"
        uvx install "${PROJECT_NAME}" --python "${PYTHON_VERSION}" --test --environment "${PROJECT_NAME}-test"
    fi
    
    # Check if test package is installed
    if ! uvx run --python "${PYTHON_VERSION}" --test "${PROJECT_NAME}" python -c "import fsl_continuum" &> /dev/null; then
        log_warning "FSL Continuum not installed in test environment. Installing..."
        uvx install "${PROJECT_NAME}" --python "${PYTHON_VERSION}" --test --environment "${PROJECT_NAME}-test"
    fi
    
    log_success "UVX test environment ready"
}

# Set up test environment
setup_test_environment() {
    log_step "Setting up test environment..."
    
    # Create test output directories
    mkdir -p "${TEST_OUTPUT_DIR}"
    mkdir -p "${TEST_OUTPUT_DIR}/unit"
    mkdir -p "${TEST_OUTPUT_DIR}/integration"
    mkdir -p "${TEST_OUTPUT_DIR}/performance"
    mkdir -p "${TEST_OUTPUT_DIR}/ai_processing"
    mkdir -p "${TEST_OUTPUT_DIR}/xml_transformation"
    mkdir -p "${TEST_OUTPUT_DIR}/semantic_languages"
    
    # Set environment variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    export PYTEST_CURRENT_TEST="fsl_continuum"
    export PYTEST_PLUGINS="pytest-cov pytest-mock pytest-benchmark"
    
    # Create pytest configuration
    if [ ! -f "pytest.ini" ]; then
        log_warning "pytest.ini not found. Using default configuration."
    fi
    
    log_success "Test environment setup complete"
}

# Run unit tests
run_unit_tests() {
    log_step "Running unit tests..."
    
    run_marked_tests "unit" "unit" "Running unit tests for individual components"
    
    # Run specific unit test categories
    run_test_files "baml_unit" "src/tests/unit/semantic_languages/test_baml_*.py" "Running BAML unit tests"
    run_test_files "pareto_lang_unit" "src/tests/unit/semantic_languages/test_pareto_lang_*.py" "Running Pareto-Lang unit tests"
    run_test_files "xml_processing_unit" "src/tests/unit/xml_processing/test_*.py" "Running XML processing unit tests"
    run_test_files "ai_integration_unit" "src/tests/unit/ai_integration/test_*.py" "Running AI integration unit tests"
}

# Run integration tests
run_integration_tests() {
    log_step "Running integration tests..."
    
    run_marked_tests "integration" "integration" "Running integration tests for component interactions"
    
    # Run specific integration test categories
    run_test_files "semantic_language_integration" "src/tests/integration/test_semantic_language_integration.py" "Running semantic language integration tests"
    run_test_files "xml_integration" "src/tests/integration/test_xml_integration.py" "Running XML integration tests"
    run_test_files "ai_integration" "src/tests/integration/test_ai_integration.py" "Running AI integration tests"
}

# Run performance tests
run_performance_tests_all() {
    log_step "Running performance tests..."
    
    run_performance_tests "semantic_language_performance" "src/tests/performance/test_semantic_language_performance.py" "Running semantic language performance tests"
    run_performance_tests "xml_performance" "src/tests/performance/test_xml_performance.py" "Running XML transformation performance tests"
    run_performance_tests "ai_performance" "src/tests/performance/test_ai_performance.py" "Running AI processing performance tests"
}

# Run AI processing tests
run_ai_processing_tests() {
    log_step "Running AI processing tests..."
    
    run_marked_tests "ai_processing" "ai_processing" "Running AI processing and validation tests"
    
    # Run specific AI test categories
    run_test_files "semantic_ai_processing" "src/tests/ai_processing/test_semantic_ai_processor.py" "Running semantic AI processing tests"
    run_test_files "ai_optimization" "src/tests/ai_processing/test_ai_optimizer.py" "Running AI optimization tests"
}

# Run XML transformation tests
run_xml_transformation_tests() {
    log_step "Running XML transformation tests..."
    
    run_marked_tests "xml_transformation" "xml_transformation" "Running XML transformation tests"
    
    # Run specific XML test categories
    run_test_files "xml_processor" "src/tests/xml_transformation/test_xml_processor.py" "Running XML processor tests"
    run_test_files "xml_validator" "src/tests/xml_transformation/test_xml_validator.py" "Running XML validator tests"
    run_test_files "xml_transformer" "src/tests/xml_transformation/test_xml_transformer.py" "Running XML transformer tests"
}

# Run semantic language tests
run_semantic_language_tests() {
    log_step "Running semantic language tests..."
    
    run_marked_tests "semantic_languages" "semantic_languages" "Running semantic language integration tests"
    
    # Run specific semantic language test categories
    run_test_files "baml_tests" "src/tests/semantic_languages/test_baml_*.py" "Running BAML tests"
    run_test_files "pareto_lang_tests" "src/tests/semantic_languages/test_pareto_lang_*.py" "Running Pareto-Lang tests"
    run_test_files "semantic_bridge" "src/tests/semantic_languages/test_semantic_bridge.py" "Running semantic bridge tests"
}

# Run smoke tests
run_smoke_tests() {
    log_step "Running smoke tests..."
    
    run_marked_tests "smoke" "smoke" "Running smoke tests for basic functionality"
    
    # Run basic smoke tests
    run_test_files "basic_smoke" "src/tests/smoke/test_basic_smoke.py" "Running basic smoke tests"
}

# Run regression tests
run_regression_tests() {
    log_step "Running regression tests..."
    
    run_marked_tests "regression" "regression" "Running regression tests"
    
    # Run specific regression tests
    run_test_files "semantic_regression" "src/tests/regression/test_semantic_regression.py" "Running semantic regression tests"
}

# Generate coverage report
generate_coverage_report() {
    log_step "Generating combined coverage report..."
    
    # Combine coverage data
    if uvx run --python "${PYTHON_VERSION}" --test "${PROJECT_NAME}" coverage combine 2>/dev/null; then
        log_success "Coverage data combined"
    else
        log_warning "Failed to combine coverage data"
    fi
    
    # Generate HTML coverage report
    if uvx run --python "${PYTHON_VERSION}" --test "${PROJECT_NAME}" coverage html --directory="${COVERAGE_DIR}" 2>/dev/null; then
        log_success "HTML coverage report generated: ${COVERAGE_DIR}/index.html"
    else
        log_warning "Failed to generate HTML coverage report"
    fi
    
    # Generate XML coverage report
    if uvx run --python "${PYTHON_VERSION}" --test "${PROJECT_NAME}" coverage xml 2>/dev/null; then
        log_success "XML coverage report generated: coverage.xml"
    else
        log_warning "Failed to generate XML coverage report"
    fi
    
    # Generate terminal coverage report
    if uvx run --python "${PYTHON_VERSION}" --test "${PROJECT_NAME}" coverage report 2>/dev/null; then
        log_success "Terminal coverage report generated"
    else
        log_warning "Failed to generate terminal coverage report"
    fi
}

# Generate benchmark report
generate_benchmark_report() {
    log_step "Generating benchmark report..."
    
    # Combine benchmark data
    python3 -c "
import json
import glob
import os

benchmarks = {}
benchmark_files = glob.glob('test_results/performance/*_benchmark.json')

for benchmark_file in benchmark_files:
    if os.path.exists(benchmark_file):
        with open(benchmark_file, 'r') as f:
            data = json.load(f)
            test_name = os.path.basename(benchmark_file).replace('_benchmark.json', '')
            benchmarks[test_name] = data

with open('combined_benchmark.json', 'w') as f:
    json.dump(benchmarks, f, indent=2)

print('Combined benchmark report generated: combined_benchmark.json')
print(f'Found {len(benchmarks)} benchmark results')
"
}

# Generate test summary
generate_test_summary() {
    log_step "Generating test summary..."
    
    TOTAL_TESTS=$((PASSED_TESTS + FAILED_TESTS + SKIPPED_TESTS))
    
    echo ""
    echo "=================================="
    echo "🎯 FSL CONTINUUM TEST SUMMARY"
    echo "=================================="
    echo "Total Tests Run: ${TOTAL_TESTS}"
    echo "Passed Tests: ${PASSED_TESTS}"
    echo "Failed Tests: ${FAILED_TESTS}"
    echo "Skipped Tests: ${SKIPPED_TESTS}"
    echo ""
    
    if [ ${FAILED_TESTS} -eq 0 ]; then
        echo "✅ ALL TESTS PASSED!"
        echo "🚀 FSL Continuum is ready for production!"
    else
        echo "❌ SOME TESTS FAILED!"
        echo "🔧 Please review the failed tests and fix the issues."
    fi
    
    echo "=================================="
    echo ""
    
    # Test results location
    echo "📊 Test Results Location:"
    echo "  Test Logs: ${TEST_OUTPUT_DIR}/"
    echo "  Coverage Report: ${COVERAGE_DIR}/index.html"
    echo "  Coverage XML: coverage.xml"
    echo "  Benchmark Report: combined_benchmark.json"
    echo ""
    
    # Coverage summary
    if [ -f "coverage.xml" ]; then
        echo "📈 Coverage Summary:"
        uvx run --python "${PYTHON_VERSION}" --test "${PROJECT_NAME}" coverage report | tail -n 1
        echo ""
    fi
    
    # Performance summary
    if [ -f "combined_benchmark.json" ]; then
        echo "⚡ Performance Summary:"
        python3 -c "
import json
import os

if os.path.exists('combined_benchmark.json'):
    with open('combined_benchmark.json', 'r') as f:
        benchmarks = json.load(f)
    
    print(f'  Benchmarks: {len(benchmarks)}')
    for test_name, data in benchmarks.items():
        if 'benchmarks' in data:
            for benchmark, metrics in data['benchmarks'].items():
                if 'mean' in metrics:
                    print(f'  {test_name}.{benchmark}: {metrics[\"mean\"]:.3f}s')
        elif 'mean' in data:
            print(f'  {test_name}: {data[\"mean\"]:.3f}s')
"
        echo ""
    fi
}

# Cleanup function
cleanup() {
    log_step "Cleaning up test environment..."
    
    # Clean up temporary files
    find "${TEST_OUTPUT_DIR}" -name "*.pyc" -delete 2>/dev/null || true
    find "${TEST_OUTPUT_DIR}" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    log_success "Test environment cleaned up"
}

# Main function
main() {
    local test_type="${1:-all}"
    
    echo "🧪 FSL Continuum UVX Test Execution"
    echo "=================================="
    echo "Python Version: ${PYTHON_VERSION}"
    echo "Project: ${PROJECT_NAME}"
    echo "Test Type: ${test_type}"
    echo ""
    
    # Set up environment
    check_uvx
    check_uvx_environment
    setup_test_environment
    
    # Set up cleanup trap
    trap cleanup EXIT
    
    # Run tests based on type
    case "${test_type}" in
        "unit")
            run_unit_tests
            ;;
        "integration")
            run_integration_tests
            ;;
        "performance")
            run_performance_tests_all
            ;;
        "ai_processing")
            run_ai_processing_tests
            ;;
        "xml_transformation")
            run_xml_transformation_tests
            ;;
        "semantic_languages")
            run_semantic_language_tests
            ;;
        "smoke")
            run_smoke_tests
            ;;
        "regression")
            run_regression_tests
            ;;
        "quick")
            run_smoke_tests
            run_unit_tests
            ;;
        "full")
            run_smoke_tests
            run_unit_tests
            run_integration_tests
            run_ai_processing_tests
            run_xml_transformation_tests
            run_semantic_language_tests
            run_performance_tests_all
            ;;
        "all"|*)
            run_smoke_tests
            run_unit_tests
            run_integration_tests
            run_ai_processing_tests
            run_xml_transformation_tests
            run_semantic_language_tests
            run_performance_tests_all
            run_regression_tests
            ;;
    esac
    
    # Generate reports
    generate_coverage_report
    generate_benchmark_report
    generate_test_summary
    
    # Exit with appropriate code
    if [ ${FAILED_TESTS} -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Show usage
usage() {
    echo "Usage: $0 [test_type]"
    echo ""
    echo "Test Types:"
    echo "  unit              - Run unit tests only"
    echo "  integration       - Run integration tests only"
    echo "  performance       - Run performance tests only"
    echo "  ai_processing     - Run AI processing tests only"
    echo "  xml_transformation - Run XML transformation tests only"
    echo "  semantic_languages - Run semantic language tests only"
    echo "  smoke             - Run smoke tests only"
    echo "  regression        - Run regression tests only"
    echo "  quick             - Run smoke and unit tests"
    echo "  full              - Run all tests except regression"
    echo "  all               - Run all tests (default)"
    echo ""
    echo "Examples:"
    echo "  $0                # Run all tests"
    echo "  $0 unit          # Run unit tests only"
    echo "  $0 performance    # Run performance tests only"
    echo "  $0 quick          # Run quick tests"
}

# Parse command line arguments
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    usage
    exit 0
fi

# Run main function
main "$@"
