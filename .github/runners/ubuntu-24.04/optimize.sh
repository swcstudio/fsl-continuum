#!/bin/bash

# FSL Continuum - Ubuntu 24.04 LTS Runtime Optimization
# SPEC:000-EXPANDED - Advanced Performance Tuning
#
# Real-time optimization script for GitHub Actions runner:
# - Dynamic resource allocation
# - Performance monitoring
# - Auto-tuning based on workload
# - Cache optimization
# - Network optimization
#
# Multi-Market Performance Standards:
# - US: Innovation speed (parallel builds, fast compilation)
# - CN: Scale efficiency (resource pooling, batch processing)
# - IN: Quality assurance (stable performance, error prevention)
# - JP: Reliability (predictable performance, Kaizen)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FSL_RUNNER_HOME="${FSL_RUNNER_HOME:-/opt/fsl-runner}"
METRICS_FILE="${FSL_RUNNER_HOME}/logs/runtime-metrics.log"
CONFIG_FILE="${FSL_RUNNER_HOME}/config/optimization.json"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$METRICS_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1" >> "$METRICS_FILE"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$METRICS_FILE"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1" >> "$METRICS_FILE"
}

# Initialize configuration
init_config() {
    mkdir -p "$(dirname "$CONFIG_FILE")"
    mkdir -p "$(dirname "$METRICS_FILE")"
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE" << 'EOF'
{
  "optimization": {
    "cpu_threshold": 80,
    "memory_threshold": 80,
    "disk_threshold": 85,
    "network_threshold": 90,
    "auto_tune": true,
    "tune_interval": 300
  },
  "workload": {
    "type": "mixed",
    "parallel_jobs": 4,
    "cache_size_gb": 10,
    "build_optimization": true
  },
  "performance": {
    "target_build_time": 300,
    "max_memory_per_job": 2048,
    "network_concurrency": 10
  },
  "last_optimized": null
}
EOF
    fi
}

# Get system metrics
get_metrics() {
    local cpu_usage memory_usage disk_usage network_io load_avg
    local temp_file
    
    temp_file=$(mktemp)
    
    # CPU Usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')
    
    # Memory Usage
    memory_usage=$(free | grep Mem | awk '{printf("%.1f", ($3/$2) * 100.0)}')
    
    # Disk Usage
    disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    # Network I/O (simplified)
    network_io=$(cat /proc/net/dev | grep -E "(eth|ens|enp)" | awk '{sum += $2 + $10} END {print sum}' || echo "0")
    
    # Load Average
    load_avg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    
    # Temperature (if available)
    local cpu_temp="N/A"
    if command -v sensors &> /dev/null; then
        cpu_temp=$(sensors | grep -E "(Core|Package)" | awk '{print $3}' | head -1 | sed 's/+//' || echo "N/A")
    fi
    
    cat > "$temp_file" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "cpu": {
    "usage_percent": "$cpu_usage",
    "load_average": "$load_avg",
    "temperature": "$cpu_temp"
  },
  "memory": {
    "usage_percent": "$memory_usage",
    "available_gb": "$(free -g | grep Mem | awk '{print $7}')"
  },
  "disk": {
    "usage_percent": "$disk_usage",
    "available_gb": "$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')"
  },
  "network": {
    "io_bytes": "$network_io"
  }
}
EOF
    
    cat "$temp_file"
    rm "$temp_file"
}

# Optimize CPU performance
optimize_cpu() {
    local cpu_threshold current_cpu
    cpu_threshold=$(jq -r '.optimization.cpu_threshold' "$CONFIG_FILE")
    current_cpu=$(get_metrics | jq -r '.cpu.usage_percent' | sed 's/%//')
    
    info "CPU Optimization - Current: ${current_cpu}%, Threshold: ${cpu_threshold}%"
    
    if (( $(echo "$current_cpu > $cpu_threshold" | bc -l) )); then
        warn "High CPU usage detected, applying optimizations..."
        
        # Adjust CPU governor for performance
        if command -v cpupower &> /dev/null; then
            cpupower frequency-set -g performance 2>/dev/null || true
        fi
        
        # Reduce background processes
        renice +5 -p $(pgrep -f "systemd-journald") 2>/dev/null || true
        
        # Optimize process scheduling
        echo 1000000 > /proc/sys/kernel/sched_rt_runtime_us 2>/dev/null || true
        
        log "CPU optimizations applied"
    else
        # Set balanced governor for normal usage
        if command -v cpupower &> /dev/null; then
            cpupower frequency-set -g ondemand 2>/dev/null || true
        fi
        
        info "CPU usage normal, balanced governor set"
    fi
}

# Optimize memory usage
optimize_memory() {
    local mem_threshold current_mem
    mem_threshold=$(jq -r '.optimization.memory_threshold' "$CONFIG_FILE")
    current_mem=$(get_metrics | jq -r '.memory.usage_percent' | sed 's/%//')
    
    info "Memory Optimization - Current: ${current_mem}%, Threshold: ${mem_threshold}%"
    
    if (( $(echo "$current_mem > $mem_threshold" | bc -l) )); then
        warn "High memory usage detected, applying optimizations..."
        
        # Clear system caches
        sync && echo 3 > /proc/sys/vm/drop_caches
        
        # Compress memory pages
        echo 1 > /proc/sys/vm/compact_memory 2>/dev/null || true
        
        # Adjust swappiness for better memory management
        echo 10 > /proc/sys/vm/swappiness
        
        # Trigger garbage collection for Node.js processes
        pkill -SIGUSR2 node 2>/dev/null || true
        
        log "Memory optimizations applied"
    else
        info "Memory usage normal"
    fi
}

# Optimize disk I/O
optimize_disk() {
    local disk_threshold current_disk
    disk_threshold=$(jq -r '.optimization.disk_threshold' "$CONFIG_FILE")
    current_disk=$(get_metrics | jq -r '.disk.usage_percent')
    
    info "Disk Optimization - Current: ${current_disk}%, Threshold: ${disk_threshold}%"
    
    if (( current_disk > disk_threshold )); then
        warn "High disk usage detected, applying optimizations..."
        
        # Clean temporary files
        find /tmp -type f -mtime +1 -delete 2>/dev/null || true
        find /var/tmp -type f -mtime +1 -delete 2>/dev/null || true
        
        # Clean package caches
        apt-get clean 2>/dev/null || true
        
        # Clean Docker unused resources
        docker system prune -f 2>/dev/null || true
        
        # Clean old logs
        find /var/log -name "*.log" -mtime +7 -delete 2>/dev/null || true
        journalctl --vacuum-time=7d 2>/dev/null || true
        
        # Compress old log files
        find /var/log -name "*.log" -mtime +1 -exec gzip {} \; 2>/dev/null || true
        
        log "Disk optimizations applied"
    else
        info "Disk usage normal"
    fi
}

# Optimize network performance
optimize_network() {
    info "Network Optimization"
    
    # Adjust TCP window scaling
    echo 1 > /proc/sys/net/ipv4/tcp_window_scaling 2>/dev/null || true
    
    # Adjust TCP buffer sizes
    echo 4194304 > /proc/sys/net/core/rmem_max 2>/dev/null || true
    echo 4194304 > /proc/sys/net/core/wmem_max 2>/dev/null || true
    
    # Enable TCP BBR congestion control if available
    if modinfo tcp_bbr &>/dev/null; then
        echo bbr > /proc/sys/net/ipv4/tcp_congestion_control 2>/dev/null || true
    fi
    
    # Optimize network queue
    echo 5000 > /proc/sys/net/core.netdev_max_backlog 2>/dev/null || true
    
    info "Network optimizations applied"
}

# Optimize caching
optimize_caching() {
    info "Cache Optimization"
    
    # Optimize file system cache
    echo 20 > /proc/sys/vm/vfs_cache_pressure 2>/dev/null || true
    
    # Optimize dirty pages
    echo 5 > /proc/sys/vm/dirty_background_ratio 2>/dev/null || true
    echo 10 > /proc/sys/vm/dirty_ratio 2>/dev/null || true
    
    # Prefetch commonly used files
    if [[ -d "/usr/local/bin" ]]; then
        find /usr/local/bin -type f -executable -exec cat {} \; > /dev/null 2>&1 || true
    fi
    
    info "Cache optimizations applied"
}

# Optimize Docker performance
optimize_docker() {
    info "Docker Optimization"
    
    if command -v docker &> /dev/null; then
        # Prune unused Docker resources
        docker system prune -f 2>/dev/null || true
        
        # Optimize Docker daemon settings
        if [[ -f "/etc/docker/daemon.json" ]]; then
            # Reload Docker configuration
            systemctl reload docker 2>/dev/null || true
        fi
        
        # Set Docker container limits
        local max_containers
        max_containers=$(($(nproc) * 2))
        
        # Update Docker daemon config for better performance
        cat > /etc/docker/daemon.json.tmp << 'EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "max-concurrent-downloads": 10,
  "max-concurrent-uploads": 10,
  "live-restore": true,
  "userland-proxy": false,
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 1048576,
      "Soft": 1048576
    }
  }
}
EOF
        
        # Apply if changed
        if ! diff -q /etc/docker/daemon.json.tmp /etc/docker/daemon.json &>/dev/null; then
            mv /etc/docker/daemon.json.tmp /etc/docker/daemon.json
            systemctl restart docker
            log "Docker configuration updated and restarted"
        else
            rm /etc/docker/daemon.json.tmp
        fi
    fi
    
    info "Docker optimizations completed"
}

# Auto-tune based on workload patterns
auto_tune() {
    local auto_tune_enabled
    auto_tune_enabled=$(jq -r '.optimization.auto_tune' "$CONFIG_FILE")
    
    if [[ "$auto_tune_enabled" != "true" ]]; then
        info "Auto-tune disabled in configuration"
        return
    fi
    
    info "Starting auto-tune analysis..."
    
    # Analyze recent workload patterns
    local recent_metrics avg_cpu avg_mem avg_disk
    recent_metrics=$(tail -60 "$METRICS_FILE" 2>/dev/null | grep -E "(CPU|Memory|Disk)" || echo "")
    
    if [[ -n "$recent_metrics" ]]; then
        # Calculate averages from recent metrics
        avg_cpu=$(echo "$recent_metrics" | grep "CPU" | awk '{sum+=$3} END {print sum/NR}' 2>/dev/null || echo "50")
        avg_mem=$(echo "$recent_metrics" | grep "Memory" | awk '{sum+=$3} END {print sum/NR}' 2>/dev/null || echo "50")
        avg_disk=$(echo "$recent_metrics" | grep "Disk" | awk '{sum+=$3} END {print sum/NR}' 2>/dev/null || echo "50")
        
        info "Workload analysis - Avg CPU: ${avg_cpu}%, Memory: ${avg_mem}%, Disk: ${avg_disk}%"
        
        # Adjust configuration based on patterns
        local new_parallel_jobs new_cache_size
        new_parallel_jobs=$(jq '.workload.parallel_jobs' "$CONFIG_FILE")
        new_cache_size=$(jq '.workload.cache_size_gb' "$CONFIG_FILE")
        
        # Increase parallel jobs if CPU is underutilized
        if (( $(echo "$avg_cpu < 60" | bc -l) )); then
            new_parallel_jobs=$((new_parallel_jobs + 1))
            new_parallel_jobs=$((new_parallel_jobs > 8 ? 8 : new_parallel_jobs))
            info "Increasing parallel jobs to $new_parallel_jobs due to low CPU usage"
        fi
        
        # Decrease parallel jobs if CPU is overutilized
        if (( $(echo "$avg_cpu > 85" | bc -l) )); then
            new_parallel_jobs=$((new_parallel_jobs - 1))
            new_parallel_jobs=$((new_parallel_jobs < 2 ? 2 : new_parallel_jobs))
            info "Decreasing parallel jobs to $new_parallel_jobs due to high CPU usage"
        fi
        
        # Adjust cache size based on memory usage
        if (( $(echo "$avg_mem < 60" | bc -l) )); then
            new_cache_size=$((new_cache_size + 2))
            new_cache_size=$((new_cache_size > 20 ? 20 : new_cache_size))
            info "Increasing cache size to ${new_cache_size}GB due to low memory usage"
        fi
        
        # Update configuration
        jq --arg parallel_jobs "$new_parallel_jobs" \
           --arg cache_size "$new_cache_size" \
           '.workload.parallel_jobs = ($parallel_jobs | tonumber) |
            .workload.cache_size_gb = ($cache_size | tonumber) |
            .last_optimized = "$(date -u +%Y-%m-%dT%H:%M:%SZ)"' \
           "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        
        log "Auto-tune completed - New parallel jobs: $new_parallel_jobs, Cache: ${new_cache_size}GB"
    else
        info "Insufficient metrics for auto-tune analysis"
    fi
}

# Generate performance report
generate_report() {
    local report_file
    report_file="${FSL_RUNNER_HOME}/reports/performance-$(date +%Y%m%d-%H%M%S).html"
    
    mkdir -p "$(dirname "$report_file")"
    
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>FSL Runner Performance Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .metric { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
        .good { background-color: #d4edda; }
        .warning { background-color: #fff3cd; }
        .critical { background-color: #f8d7da; }
        .chart { width: 100%; height: 300px; }
    </style>
</head>
<body>
    <h1>FSL Continuum Runner Performance Report</h1>
    <p>Generated: $(date)</p>
    
    <div class="metric">
        <h3>Current System Metrics</h3>
        <pre>$(get_metrics)</pre>
    </div>
    
    <div class="metric">
        <h3>Optimization Configuration</h3>
        <pre>$(cat "$CONFIG_FILE")</pre>
    </div>
    
    <div class="metric">
        <h3>Recent Performance History</h3>
        <pre>$(tail -20 "$METRICS_FILE" 2>/dev/null || echo "No history available")</pre>
    </div>
</body>
</html>
EOF
    
    log "Performance report generated: $report_file"
}

# Main optimization function
main() {
    local action="${1:-optimize}"
    
    # Initialize
    init_config
    
    case "$action" in
        "optimize")
            log "Starting FSL Runner optimization..."
            optimize_cpu
            optimize_memory
            optimize_disk
            optimize_network
            optimize_caching
            optimize_docker
            auto_tune
            generate_report
            log "Optimization completed"
            ;;
        "cpu")
            optimize_cpu
            ;;
        "memory")
            optimize_memory
            ;;
        "disk")
            optimize_disk
            ;;
        "network")
            optimize_network
            ;;
        "docker")
            optimize_docker
            ;;
        "cache")
            optimize_caching
            ;;
        "autotune")
            auto_tune
            ;;
        "report")
            generate_report
            ;;
        "metrics")
            get_metrics
            ;;
        "help")
            echo "Usage: $0 [action]"
            echo "Actions: optimize, cpu, memory, disk, network, docker, cache, autotune, report, metrics, help"
            ;;
        *)
            error "Unknown action: $action"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
