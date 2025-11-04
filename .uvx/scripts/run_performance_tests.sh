#!/bin/bash
# FSL Continuum UVX Performance Testing Script
# Complete performance testing using UVX virtual environments

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

log_benchmark() {
    echo -e "${CYAN}[BENCHMARK]${NC} $1"
}

# Configuration
PYTHON_VERSION="3.11"
PROJECT_NAME="fsl-continuum"
PERFORMANCE_OUTPUT_DIR="performance_results"
BENCHMARK_DIR=".benchmark"

# Performance thresholds
BAML_PARSING_THRESHOLD=0.1      # 100ms per document
PARETO_LANG_PARSING_THRESHOLD=0.1 # 100ms per document
XML_TRANSFORMATION_THRESHOLD=0.5  # 500ms per transformation
AI_PROCESSING_THRESHOLD=2.0      # 2 seconds per AI operation

# Memory thresholds
BAML_PARSING_MEMORY_THRESHOLD=50      # 50MB
PARETO_LANG_PARSING_MEMORY_THRESHOLD=50 # 50MB
XML_TRANSFORMATION_MEMORY_THRESHOLD=100 # 100MB
AI_PROCESSING_MEMORY_THRESHOLD=200     # 200MB

# Performance counters
TOTAL_BENCHMARKS=0
PASSED_BENCHMARKS=0
FAILED_BENCHMARKS=0
REGRESSION_DETECTED=0

# Function to run performance benchmark
run_performance_benchmark() {
    local test_name="$1"
    local test_file="$2"
    local test_description="$3"
    local threshold="$4"
    local memory_threshold="$5"
    
    log_benchmark "Running ${test_name} performance benchmark..."
    log_info "${test_description}"
    
    # Create output directory
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/${test_name}"
    
    # Set environment variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    export PYTEST_CURRENT_TEST="${test_name}_performance"
    export PYTEST_BENCHMARK_ENABLED=true
    export PYTEST_PLUGINS="pytest-cov pytest-mock pytest-benchmark"
    
    # Execute benchmark
    if uvx run --python "${PYTHON_VERSION}" --performance "${PROJECT_NAME}" \
       pytest "${test_file}" -v -m performance \
       --benchmark-only \
       --benchmark-json="${PERFORMANCE_OUTPUT_DIR}/${test_name}/${test_name}_benchmark.json" \
       --benchmark-sort=min \
       --benchmark-min-rounds=5 \
       --benchmark-max-time=30 \
       --benchmark-warmup=true \
       --benchmark-warmup-shutdown=true \
       --benchmark-storage="${BENCHMARK_DIR}" \
       2>&1 | \
       tee "${PERFORMANCE_OUTPUT_DIR}/${test_name}/${test_name}_benchmark.log"; then
        
        log_success "${test_name} performance benchmark completed!"
        PASSED_BENCHMARKS=$((PASSED_BENCHMARKS + 1))
        
        # Analyze benchmark results
        analyze_benchmark_results "${test_name}" "${threshold}" "${memory_threshold}"
        
        return 0
    else
        log_error "${test_name} performance benchmark failed!"
        FAILED_BENCHMARKS=$((FAILED_BENCHMARKS + 1))
        return 1
    fi
}

# Function to analyze benchmark results
analyze_benchmark_results() {
    local test_name="$1"
    local threshold="$2"
    local memory_threshold="$3"
    
    local benchmark_file="${PERFORMANCE_OUTPUT_DIR}/${test_name}/${test_name}_benchmark.json"
    
    if [ ! -f "${benchmark_file}" ]; then
        log_warning "Benchmark file not found: ${benchmark_file}"
        return 1
    fi
    
    # Parse benchmark results using Python
    python3 -c "
import json
import sys
import os

try:
    with open('${benchmark_file}', 'r') as f:
        data = json.load(f)
    
    if 'benchmarks' in data:
        benchmarks = data['benchmarks']
    else:
        benchmarks = data
    
    regression_detected = False
    
    for benchmark_name, metrics in benchmarks.items():
        if isinstance(metrics, dict) and 'mean' in metrics:
            mean_time = metrics['mean']
            min_time = metrics.get('min', mean_time)
            max_time = metrics.get('max', mean_time)
            
            print(f'  {benchmark_name}:')
            print(f'    Mean: {mean_time:.6f}s')
            print(f'    Min:  {min_time:.6f}s')
            print(f'    Max:  {max_time:.6f}s')
            
            # Check threshold
            if mean_time > ${threshold}:
                print(f'    ❌ Exceeds threshold (${threshold}s)')
                regression_detected = True
            else:
                print(f'    ✅ Within threshold (${threshold}s)')
            
            # Check memory if available
            if 'memory' in metrics:
                memory_usage = metrics['memory']
                print(f'    Memory: {memory_usage:.2f}MB')
                
                if memory_usage > ${memory_threshold}:
                    print(f'    ❌ Exceeds memory threshold (${memory_threshold}MB)')
                    regression_detected = True
                else:
                    print(f'    ✅ Within memory threshold (${memory_threshold}MB)')
            
            print()
    
    if regression_detected:
        print(f'🚨 REGRESSION DETECTED in ${test_name}!')
        sys.exit(1)
    else:
        print(f'✅ No regressions detected in ${test_name}!')
        sys.exit(0)
        
except Exception as e:
    print(f'❌ Error analyzing benchmark: {e}')
    sys.exit(1)
"
    
    local result=$?
    if [ $result -eq 1 ]; then
        REGRESSION_DETECTED=$((REGRESSION_DETECTED + 1))
        log_warning "Performance regression detected in ${test_name}"
    fi
}

# Function to run memory profiling
run_memory_profiling() {
    local test_name="$1"
    local test_file="$2"
    local test_description="$3"
    
    log_step "Running ${test_name} memory profiling..."
    log_info "${test_description}"
    
    # Create output directory
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/${test_name}/memory"
    
    # Set environment variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    export MEMORY_PROFILER_ENABLED=true
    
    # Execute memory profiling
    if uvx run --python "${PYTHON_VERSION}" --performance "${PROJECT_NAME}" \
       python -m memory_profiler \
       --output-file="${PERFORMANCE_OUTPUT_DIR}/${test_name}/memory/memory_profile.txt" \
       -c "
import sys
sys.path.insert(0, 'src')
from memory_profiler import profile

@profile
def run_memory_test():
    # Import and run test
    exec(open('${test_file}').read())

if __name__ == '__main__':
    run_memory_test()
" 2>&1 | \
       tee "${PERFORMANCE_OUTPUT_DIR}/${test_name}/memory/memory_profiling.log"; then
        
        log_success "${test_name} memory profiling completed!"
        
        # Generate memory profile report
        generate_memory_profile_report "${test_name}"
        
        return 0
    else
        log_error "${test_name} memory profiling failed!"
        return 1
    fi
}

# Function to generate memory profile report
generate_memory_profile_report() {
    local test_name="$1"
    
    local memory_profile_file="${PERFORMANCE_OUTPUT_DIR}/${test_name}/memory/memory_profile.txt"
    
    if [ ! -f "${memory_profile_file}" ]; then
        log_warning "Memory profile file not found: ${memory_profile_file}"
        return 1
    fi
    
    # Parse memory profile and generate report
    python3 -c "
import re
import os

try:
    with open('${memory_profile_file}', 'r') as f:
        content = f.read()
    
    # Extract memory usage information
    lines = content.split('\n')
    memory_usage = []
    
    for line in lines:
        if 'MiB' in line:
            match = re.search(r'(\d+\.\d+)\s+MiB', line)
            if match:
                memory_usage.append(float(match.group(1)))
    
    if memory_usage:
        max_memory = max(memory_usage)
        avg_memory = sum(memory_usage) / len(memory_usage)
        
        print(f'Memory Profile Analysis for ${test_name}:')
        print(f'  Max Memory: {max_memory:.2f} MiB')
        print(f'  Avg Memory: {avg_memory:.2f} MiB')
        print(f'  Samples: {len(memory_usage)}')
        
        # Check memory thresholds
        if test_name == 'baml_parsing' and max_memory > ${BAML_PARSING_MEMORY_THRESHOLD}:
            print(f'  ❌ Exceeds memory threshold (${BAML_PARSING_MEMORY_THRESHOLD} MiB)')
        elif test_name == 'pareto_lang_parsing' and max_memory > ${PARETO_LANG_PARSING_MEMORY_THRESHOLD}:
            print(f'  ❌ Exceeds memory threshold (${PARETO_LANG_PARSING_MEMORY_THRESHOLD} MiB)')
        elif test_name == 'xml_transformation' and max_memory > ${XML_TRANSFORMATION_MEMORY_THRESHOLD}:
            print(f'  ❌ Exceeds memory threshold (${XML_TRANSFORMATION_MEMORY_THRESHOLD} MiB)')
        elif test_name == 'ai_processing' and max_memory > ${AI_PROCESSING_MEMORY_THRESHOLD}:
            print(f'  ❌ Exceeds memory threshold (${AI_PROCESSING_MEMORY_THRESHOLD} MiB)')
        else:
            print(f'  ✅ Within memory thresholds')
        
        # Generate memory profile report
        with open('${PERFORMANCE_OUTPUT_DIR}/${test_name}/memory/memory_report.json', 'w') as f:
            import json
            report = {
                'test_name': '${test_name}',
                'max_memory': max_memory,
                'avg_memory': avg_memory,
                'samples': len(memory_usage)
            }
            json.dump(report, f, indent=2)
        
        print(f'Memory profile report generated: ${PERFORMANCE_OUTPUT_DIR}/${test_name}/memory/memory_report.json')
    
except Exception as e:
    print(f'❌ Error generating memory profile report: {e}')
"
}

# Function to run CPU profiling
run_cpu_profiling() {
    local test_name="$1"
    local test_file="$2"
    local test_description="$3"
    
    log_step "Running ${test_name} CPU profiling..."
    log_info "${test_description}"
    
    # Create output directory
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/${test_name}/cpu"
    
    # Set environment variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    export CPU_PROFILER_ENABLED=true
    
    # Execute CPU profiling
    if uvx run --python "${PYTHON_VERSION}" --performance "${PROJECT_NAME}" \
       python -m cProfile \
       -o "${PERFORMANCE_OUTPUT_DIR}/${test_name}/cpu/cpu_profile.prof" \
       -c "
import sys
sys.path.insert(0, 'src')

# Import and run test
exec(open('${test_file}').read())
" 2>&1 | \
       tee "${PERFORMANCE_OUTPUT_DIR}/${test_name}/cpu/cpu_profiling.log"; then
        
        log_success "${test_name} CPU profiling completed!"
        
        # Generate CPU profile report
        generate_cpu_profile_report "${test_name}"
        
        return 0
    else
        log_error "${test_name} CPU profiling failed!"
        return 1
    fi
}

# Function to generate CPU profile report
generate_cpu_profile_report() {
    local test_name="$1"
    
    local cpu_profile_file="${PERFORMANCE_OUTPUT_DIR}/${test_name}/cpu/cpu_profile.prof"
    
    if [ ! -f "${cpu_profile_file}" ]; then
        log_warning "CPU profile file not found: ${cpu_profile_file}"
        return 1
    fi
    
    # Generate CPU profile report
    if command -v snakeviz &> /dev/null; then
        snakeviz "${cpu_profile_file}" --hostname=0.0.0.0 --port=8080 &
        local snakeviz_pid=$!
        
        # Wait a moment for snakeviz to start
        sleep 2
        
        log_info "CPU profile visualization available at: http://localhost:8080"
        echo "Press Ctrl+C to stop the visualization server"
        
        # Wait for user to stop the server
        wait $snakeviz_pid
    else
        # Fallback to pstats
        uvx run --python "${PYTHON_VERSION}" --performance "${PROJECT_NAME}" \
           python -c "
import pstats
import sys
import json

try:
    stats = pstats.Stats('${cpu_profile_file}')
    stats.sort_stats('cumulative')
    
    # Get top 10 functions by cumulative time
    top_functions = stats.get_stats_profile().func_profiles[:10]
    
    report = {
        'test_name': '${test_name}',
        'top_functions': []
    }
    
    for func, cc, nc, tt, ct, callers in top_functions:
        func_info = {
            'function': func,
            'call_count': cc,
            'cumulative_time': ct,
            'total_time': tt
        }
        report['top_functions'].append(func_info)
    
    with open('${PERFORMANCE_OUTPUT_DIR}/${test_name}/cpu/cpu_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f'CPU profile report generated: ${PERFORMANCE_OUTPUT_DIR}/${test_name}/cpu/cpu_report.json')
    
except Exception as e:
    print(f'❌ Error generating CPU profile report: {e}')
"
    fi
}

# Function to run load testing
run_load_testing() {
    local test_name="$1"
    local test_file="$2"
    local test_description="$3"
    local concurrency="$4"
    local duration="$5"
    
    log_step "Running ${test_name} load testing..."
    log_info "${test_description}"
    log_info "Concurrency: ${concurrency}, Duration: ${duration}s"
    
    # Create output directory
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/${test_name}/load"
    
    # Set environment variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    export LOAD_TESTING_ENABLED=true
    
    # Execute load testing
    if uvx run --python "${PYTHON_VERSION}" --performance "${PROJECT_NAME}" \
       python -c "
import concurrent.futures
import time
import sys
import json
import os
sys.path.insert(0, 'src')

def run_single_test():
    '''Run a single test iteration'''
    try:
        # Import and run test
        with open('${test_file}', 'r') as f:
            exec(f.read())
        return {'success': True, 'timestamp': time.time()}
    except Exception as e:
        return {'success': False, 'error': str(e), 'timestamp': time.time()}

def run_load_test():
    '''Run load test'''
    start_time = time.time()
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=${concurrency}) as executor:
        futures = []
        
        # Submit tasks for the specified duration
        while time.time() - start_time < ${duration}:
            future = executor.submit(run_single_test)
            futures.append(future)
            
            # Limit concurrent tasks
            if len(futures) >= ${concurrency} * 2:
                # Wait for some tasks to complete
                completed_futures = [f for f in futures if f.done()]
                for completed_future in completed_futures:
                    results.append(completed_future.result())
                    futures.remove(completed_future)
        
        # Wait for remaining tasks to complete
        for future in futures:
            results.append(future.result())
    
    end_time = time.time()
    
    # Analyze results
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    total_tests = len(results)
    success_rate = len(successful_tests) / total_tests * 100
    test_rate = total_tests / (end_time - start_time)
    
    print(f'Load Test Results for ${test_name}:')
    print(f'  Total Tests: {total_tests}')
    print(f'  Successful: {len(successful_tests)}')
    print(f'  Failed: {len(failed_tests)}')
    print(f'  Success Rate: {success_rate:.2f}%')
    print(f'  Test Rate: {test_rate:.2f} tests/sec')
    print(f'  Duration: {end_time - start_time:.2f}s')
    print(f'  Concurrency: ${concurrency}')
    
    # Save results
    report = {
        'test_name': '${test_name}',
        'total_tests': total_tests,
        'successful_tests': len(successful_tests),
        'failed_tests': len(failed_tests),
        'success_rate': success_rate,
        'test_rate': test_rate,
        'duration': end_time - start_time,
        'concurrency': ${concurrency}
    }
    
    with open('${PERFORMANCE_OUTPUT_DIR}/${test_name}/load/load_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f'Load test report generated: ${PERFORMANCE_OUTPUT_DIR}/${test_name}/load/load_report.json')
    
    return success_rate >= 95  # Require 95% success rate

if __name__ == '__main__':
    success = run_load_test()
    sys.exit(0 if success else 1)
" 2>&1 | \
       tee "${PERFORMANCE_OUTPUT_DIR}/${test_name}/load/load_testing.log"; then
        
        log_success "${test_name} load testing completed!"
        return 0
    else
        log_error "${test_name} load testing failed!"
        return 1
    fi
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

# Check UVX performance environment
check_uvx_performance_environment() {
    log_info "Checking UVX performance environment..."
    
    # Check if performance environment exists
    if ! uvx list "${PROJECT_NAME}-performance" &> /dev/null; then
        log_warning "UVX performance environment not found. Creating..."
        uvx create "${PROJECT_NAME}-performance" --python "${PYTHON_VERSION}" --performance --description "FSL Continuum Performance Testing Environment"
        uvx install "${PROJECT_NAME}" --python "${PYTHON_VERSION}" --performance --environment "${PROJECT_NAME}-performance"
    fi
    
    log_success "UVX performance environment ready"
}

# Set up performance testing environment
setup_performance_environment() {
    log_step "Setting up performance testing environment..."
    
    # Create performance output directories
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}"
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/baml_parsing"
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/pareto_lang_parsing"
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/xml_transformation"
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/ai_processing"
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/concurrent_processing"
    mkdir -p "${PERFORMANCE_OUTPUT_DIR}/load_testing"
    mkdir -p "${BENCHMARK_DIR}"
    
    # Set environment variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    export PYTEST_CURRENT_TEST="performance"
    export PYTEST_BENCHMARK_ENABLED=true
    export MEMORY_PROFILER_ENABLED=false
    export CPU_PROFILER_ENABLED=false
    export LOAD_TESTING_ENABLED=false
    
    log_success "Performance testing environment setup complete"
}

# Run all performance benchmarks
run_all_performance_benchmarks() {
    log_step "Running all performance benchmarks..."
    
    # BAML parsing performance
    run_performance_benchmark "baml_parsing" "src/tests/performance/test_baml_parsing_performance.py" "BAML parsing performance benchmark" "${BAML_PARSING_THRESHOLD}" "${BAML_PARSING_MEMORY_THRESHOLD}"
    TOTAL_BENCHMARKS=$((TOTAL_BENCHMARKS + 1))
    
    # Pareto-Lang parsing performance
    run_performance_benchmark "pareto_lang_parsing" "src/tests/performance/test_pareto_lang_parsing_performance.py" "Pareto-Lang parsing performance benchmark" "${PARETO_LANG_PARSING_THRESHOLD}" "${PARETO_LANG_PARSING_MEMORY_THRESHOLD}"
    TOTAL_BENCHMARKS=$((TOTAL_BENCHMARKS + 1))
    
    # XML transformation performance
    run_performance_benchmark "xml_transformation" "src/tests/performance/test_xml_transformation_performance.py" "XML transformation performance benchmark" "${XML_TRANSFORMATION_THRESHOLD}" "${XML_TRANSFORMATION_MEMORY_THRESHOLD}"
    TOTAL_BENCHMARKS=$((TOTAL_BENCHMARKS + 1))
    
    # AI processing performance
    run_performance_benchmark "ai_processing" "src/tests/performance/test_ai_processing_performance.py" "AI processing performance benchmark" "${AI_PROCESSING_THRESHOLD}" "${AI_PROCESSING_MEMORY_THRESHOLD}"
    TOTAL_BENCHMARKS=$((TOTAL_BENCHMARKS + 1))
    
    # Concurrent processing performance
    run_performance_benchmark "concurrent_processing" "src/tests/performance/test_concurrent_processing_performance.py" "Concurrent processing performance benchmark" "1.0" "150"
    TOTAL_BENCHMARKS=$((TOTAL_BENCHMARKS + 1))
}

# Run memory profiling
run_all_memory_profiling() {
    log_step "Running memory profiling..."
    
    # BAML parsing memory profiling
    run_memory_profiling "baml_parsing" "src/tests/performance/test_baml_parsing_performance.py" "BAML parsing memory profiling"
    
    # Pareto-Lang parsing memory profiling
    run_memory_profiling "pareto_lang_parsing" "src/tests/performance/test_pareto_lang_parsing_performance.py" "Pareto-Lang parsing memory profiling"
    
    # XML transformation memory profiling
    run_memory_profiling "xml_transformation" "src/tests/performance/test_xml_transformation_performance.py" "XML transformation memory profiling"
    
    # AI processing memory profiling
    run_memory_profiling "ai_processing" "src/tests/performance/test_ai_processing_performance.py" "AI processing memory profiling"
}

# Run CPU profiling
run_all_cpu_profiling() {
    log_step "Running CPU profiling..."
    
    # BAML parsing CPU profiling
    run_cpu_profiling "baml_parsing" "src/tests/performance/test_baml_parsing_performance.py" "BAML parsing CPU profiling"
    
    # Pareto-Lang parsing CPU profiling
    run_cpu_profiling "pareto_lang_parsing" "src/tests/performance/test_pareto_lang_parsing_performance.py" "Pareto-Lang parsing CPU profiling"
    
    # XML transformation CPU profiling
    run_cpu_profiling "xml_transformation" "src/tests/performance/test_xml_transformation_performance.py" "XML transformation CPU profiling"
    
    # AI processing CPU profiling
    run_cpu_profiling "ai_processing" "src/tests/performance/test_ai_processing_performance.py" "AI processing CPU profiling"
}

# Run load testing
run_all_load_testing() {
    log_step "Running load testing..."
    
    # BAML parsing load testing
    run_load_testing "baml_parsing" "src/tests/performance/test_baml_parsing_performance.py" "BAML parsing load testing" 10 30
    
    # Pareto-Lang parsing load testing
    run_load_testing "pareto_lang_parsing" "src/tests/performance/test_pareto_lang_parsing_performance.py" "Pareto-Lang parsing load testing" 10 30
    
    # XML transformation load testing
    run_load_testing "xml_transformation" "src/tests/performance/test_xml_transformation_performance.py" "XML transformation load testing" 5 30
    
    # AI processing load testing
    run_load_testing "ai_processing" "src/tests/performance/test_ai_processing_performance.py" "AI processing load testing" 3 30
}

# Generate combined performance report
generate_performance_report() {
    log_step "Generating combined performance report..."
    
    # Combine benchmark results
    python3 -c "
import json
import glob
import os
import statistics

benchmarks = {}
benchmark_files = glob.glob('${PERFORMANCE_OUTPUT_DIR}/*/*_benchmark.json')

for benchmark_file in benchmark_files:
    if os.path.exists(benchmark_file):
        with open(benchmark_file, 'r') as f:
            data = json.load(f)
            test_name = os.path.basename(benchmark_file).replace('_benchmark.json', '')
            benchmarks[test_name] = data

# Generate combined report
combined_report = {
    'timestamp': os.path.getmtime('${PERFORMANCE_OUTPUT_DIR}'),
    'benchmarks': benchmarks,
    'summary': {
        'total_benchmarks': len(benchmarks),
        'passed_benchmarks': ${PASSED_BENCHMARKS},
        'failed_benchmarks': ${FAILED_BENCHMARKS},
        'regressions_detected': ${REGRESSION_DETECTED}
    }
}

# Save combined report
with open('${PERFORMANCE_OUTPUT_DIR}/combined_performance_report.json', 'w') as f:
    json.dump(combined_report, f, indent=2)

# Generate performance summary
print('📊 Combined Performance Report:')
print('=' * 60)
print(f'Total Benchmarks: {len(benchmarks)}')
print(f'Passed Benchmarks: ${PASSED_BENCHMARKS}')
print(f'Failed Benchmarks: ${FAILED_BENCHMARKS}')
print(f'Regressions Detected: ${REGRESSION_DETECTED}')
print()

print('Performance Results:')
for test_name, data in benchmarks.items():
    if 'benchmarks' in data:
        for benchmark_name, metrics in data['benchmarks'].items():
            if isinstance(metrics, dict) and 'mean' in metrics:
                print(f'  {test_name}.{benchmark_name}: {metrics[\"mean\"]:.6f}s')
    elif 'mean' in data:
        print(f'  {test_name}: {data[\"mean\"]:.6f}s')

print()
print('Performance Summary Report:')
print('  Generated: ${PERFORMANCE_OUTPUT_DIR}/combined_performance_report.json')
print('  Benchmarks: ${len(benchmarks)}')
"
    
    log_success "Combined performance report generated: ${PERFORMANCE_OUTPUT_DIR}/combined_performance_report.json"
}

# Generate performance summary
generate_performance_summary() {
    log_step "Generating performance summary..."
    
    TOTAL_TESTS=$((PASSED_BENCHMARKS + FAILED_BENCHMARKS))
    
    echo ""
    echo "=================================="
    echo "🚀 FSL CONTINUUM PERFORMANCE SUMMARY"
    echo "=================================="
    echo "Total Benchmarks: ${TOTAL_TESTS}"
    echo "Passed Benchmarks: ${PASSED_BENCHMARKS}"
    echo "Failed Benchmarks: ${FAILED_BENCHMARKS}"
    echo "Regressions Detected: ${REGRESSION_DETECTED}"
    echo ""
    
    if [ ${FAILED_BENCHMARKS} -eq 0 ] && [ ${REGRESSION_DETECTED} -eq 0 ]; then
        echo "✅ ALL PERFORMANCE BENCHMARKS PASSED!"
        echo "🚀 FSL Continuum performance is optimal!"
    elif [ ${FAILED_BENCHMARKS} -eq 0 ] && [ ${REGRESSION_DETECTED} -gt 0 ]; then
        echo "⚠️  PERFORMANCE REGRESSIONS DETECTED!"
        echo "🔧 Please review regressions and optimize performance."
    else
        echo "❌ SOME PERFORMANCE BENCHMARKS FAILED!"
        echo "🔧 Please review failed benchmarks and fix issues."
    fi
    
    echo "=================================="
    echo ""
    
    # Performance results location
    echo "📊 Performance Results Location:"
    echo "  Performance Logs: ${PERFORMANCE_OUTPUT_DIR}/"
    echo "  Benchmark Results: ${PERFORMANCE_OUTPUT_DIR}/*_benchmark.json"
    echo "  Memory Profiles: ${PERFORMANCE_OUTPUT_DIR}/*/memory/"
    echo "  CPU Profiles: ${PERFORMANCE_OUTPUT_DIR}/*/cpu/"
    echo "  Load Tests: ${PERFORMANCE_OUTPUT_DIR}/*/load/"
    echo "  Combined Report: ${PERFORMANCE_OUTPUT_DIR}/combined_performance_report.json"
    echo ""
    
    # Performance thresholds status
    echo "📈 Performance Thresholds Status:"
    echo "  BAML Parsing Threshold: ${BAML_PARSING_THRESHOLD}s"
    echo "  Pareto-Lang Parsing Threshold: ${PARETO_LANG_PARSING_THRESHOLD}s"
    echo "  XML Transformation Threshold: ${XML_TRANSFORMATION_THRESHOLD}s"
    echo "  AI Processing Threshold: ${AI_PROCESSING_THRESHOLD}s"
    echo ""
    
    echo "🧠 Memory Thresholds Status:"
    echo "  BAML Parsing Memory Threshold: ${BAML_PARSING_MEMORY_THRESHOLD}MB"
    echo "  Pareto-Lang Parsing Memory Threshold: ${PARETO_LANG_PARSING_MEMORY_THRESHOLD}MB"
    echo "  XML Transformation Memory Threshold: ${XML_TRANSFORMATION_MEMORY_THRESHOLD}MB"
    echo "  AI Processing Memory Threshold: ${AI_PROCESSING_MEMORY_THRESHOLD}MB"
    echo ""
}

# Cleanup function
cleanup() {
    log_step "Cleaning up performance testing environment..."
    
    # Clean up temporary files
    find "${PERFORMANCE_OUTPUT_DIR}" -name "*.pyc" -delete 2>/dev/null || true
    find "${PERFORMANCE_OUTPUT_DIR}" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    log_success "Performance testing environment cleaned up"
}

# Main function
main() {
    local test_type="${1:-all}"
    
    echo "⚡ FSL Continuum UVX Performance Testing"
    echo "==================================="
    echo "Python Version: ${PYTHON_VERSION}"
    echo "Project: ${PROJECT_NAME}"
    echo "Test Type: ${test_type}"
    echo ""
    
    # Set up environment
    check_uvx
    check_uvx_performance_environment
    setup_performance_environment
    
    # Set up cleanup trap
    trap cleanup EXIT
    
    # Run performance tests based on type
    case "${test_type}" in
        "benchmarks")
            run_all_performance_benchmarks
            ;;
        "memory")
            run_all_memory_profiling
            ;;
        "cpu")
            run_all_cpu_profiling
            ;;
        "load")
            run_all_load_testing
            ;;
        "quick")
            run_performance_benchmark "baml_parsing" "src/tests/performance/test_baml_parsing_performance.py" "Quick BAML parsing benchmark" "${BAML_PARSING_THRESHOLD}" "${BAML_PARSING_MEMORY_THRESHOLD}"
            TOTAL_BENCHMARKS=1
            ;;
        "all"|*)
            run_all_performance_benchmarks
            run_all_memory_profiling
            run_all_cpu_profiling
            run_all_load_testing
            ;;
    esac
    
    # Generate reports
    generate_performance_report
    generate_performance_summary
    
    # Exit with appropriate code
    if [ ${FAILED_BENCHMARKS} -eq 0 ] && [ ${REGRESSION_DETECTED} -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Show usage
usage() {
    echo "Usage: $0 [test_type]"
    echo ""
    echo "Performance Test Types:"
    echo "  benchmarks   - Run performance benchmarks only"
    echo "  memory       - Run memory profiling only"
    echo "  cpu          - Run CPU profiling only"
    echo "  load         - Run load testing only"
    echo "  quick        - Run quick performance test"
    echo "  all          - Run all performance tests (default)"
    echo ""
    echo "Examples:"
    echo "  $0                # Run all performance tests"
    echo "  $0 benchmarks     # Run performance benchmarks only"
    echo "  $0 memory         # Run memory profiling only"
    echo "  $0 quick          # Run quick performance test"
}

# Parse command line arguments
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    usage
    exit 0
fi

# Run main function
main "$@"
