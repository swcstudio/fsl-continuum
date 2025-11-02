/**
 * Metrics and monitoring service for enterprise ZeroServe MCP Server
 */

import client from 'prom-client';
import { Request, Response } from 'express';

// Create a Registry to register the metrics
const register = new client.Registry();

// Add a default label which can be used to identify metrics
register.setDefaultLabels({
  app: 'zeroserve-mcp-server',
  version: process.env.npm_package_version || '2.0.0',
});

// Enable the collection of default metrics
client.collectDefaultMetrics({ register });

// Custom metrics
export class MetricsService {
  // HTTP request metrics
  private httpRequestDuration = new client.Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status_code'],
    registers: [register],
  });

  private httpRequestTotal = new client.Counter({
    name: 'http_requests_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'status_code'],
    registers: [register],
  });

  // MCP operation metrics
  private mcpOperationDuration = new client.Histogram({
    name: 'mcp_operation_duration_seconds',
    help: 'Duration of MCP operations in seconds',
    labelNames: ['operation', 'tool', 'status'],
    buckets: [0.1, 0.5, 1, 2, 5, 10, 30, 60, 300],
    registers: [register],
  });

  private mcpOperationTotal = new client.Counter({
    name: 'mcp_operations_total',
    help: 'Total number of MCP operations',
    labelNames: ['operation', 'tool', 'status'],
    registers: [register],
  });

  // Domain scanning metrics
  private domainScanDuration = new client.Histogram({
    name: 'domain_scan_duration_seconds',
    help: 'Duration of domain scans in seconds',
    labelNames: ['scan_depth', 'status'],
    buckets: [1, 5, 10, 30, 60, 300, 600, 1800],
    registers: [register],
  });

  private domainScanTotal = new client.Counter({
    name: 'domain_scans_total',
    help: 'Total number of domain scans',
    labelNames: ['scan_depth', 'status'],
    registers: [register],
  });

  // Authentication metrics
  private authenticationTotal = new client.Counter({
    name: 'authentications_total',
    help: 'Total number of authentication attempts',
    labelNames: ['method', 'status'],
    registers: [register],
  });

  private authenticationDuration = new client.Histogram({
    name: 'authentication_duration_seconds',
    help: 'Duration of authentication in seconds',
    labelNames: ['method'],
    registers: [register],
  });

  // Cache metrics
  private cacheHits = new client.Counter({
    name: 'cache_hits_total',
    help: 'Total number of cache hits',
    labelNames: ['cache_type'],
    registers: [register],
  });

  private cacheMisses = new client.Counter({
    name: 'cache_misses_total',
    help: 'Total number of cache misses',
    labelNames: ['cache_type'],
    registers: [register],
  });

  // Rate limiting metrics
  private rateLimitHits = new client.Counter({
    name: 'rate_limit_hits_total',
    help: 'Total number of rate limit violations',
    labelNames: ['user_type', 'limit_type'],
    registers: [register],
  });

  // System metrics
  private memoryUsage = new client.Gauge({
    name: 'memory_usage_bytes',
    help: 'Memory usage in bytes',
    labelNames: ['type'],
    registers: [register],
  });

  private cpuUsage = new client.Gauge({
    name: 'cpu_usage_percent',
    help: 'CPU usage percentage',
    registers: [register],
  });

  // Active connections
  private activeConnections = new client.Gauge({
    name: 'active_connections',
    help: 'Number of active connections',
    registers: [register],
  });

  /**
   * Middleware to track HTTP request metrics
   */
  httpMetricsMiddleware = (req: Request, res: Response, next: () => void) => {
    const start = Date.now();
    
    res.on('finish', () => {
      const duration = (Date.now() - start) / 1000;
      const route = req.route?.path || req.path || 'unknown';
      
      this.httpRequestDuration
        .labels(req.method, route, res.statusCode.toString())
        .observe(duration);
        
      this.httpRequestTotal
        .labels(req.method, route, res.statusCode.toString())
        .inc();
    });
    
    next();
  };

  /**
   * Track MCP operation
   */
  trackMCPOperation(operation: string, tool: string, status: string, duration: number) {
    this.mcpOperationDuration
      .labels(operation, tool, status)
      .observe(duration);
      
    this.mcpOperationTotal
      .labels(operation, tool, status)
      .inc();
  }

  /**
   * Track domain scan
   */
  trackDomainScan(scanDepth: string, status: string, duration: number) {
    this.domainScanDuration
      .labels(scanDepth, status)
      .observe(duration);
      
    this.domainScanTotal
      .labels(scanDepth, status)
      .inc();
  }

  /**
   * Track authentication attempt
   */
  trackAuthentication(method: string, status: string, duration?: number) {
    this.authenticationTotal
      .labels(method, status)
      .inc();
      
    if (duration !== undefined) {
      this.authenticationDuration
        .labels(method)
        .observe(duration);
    }
  }

  /**
   * Track cache hit
   */
  trackCacheHit(cacheType: string) {
    this.cacheHits.labels(cacheType).inc();
  }

  /**
   * Track cache miss
   */
  trackCacheMiss(cacheType: string) {
    this.cacheMisses.labels(cacheType).inc();
  }

  /**
   * Track rate limit hit
   */
  trackRateLimitHit(userType: string, limitType: string) {
    this.rateLimitHits.labels(userType, limitType).inc();
  }

  /**
   * Update memory usage
   */
  updateMemoryUsage() {
    const memUsage = process.memoryUsage();
    this.memoryUsage.labels('rss').set(memUsage.rss);
    this.memoryUsage.labels('heapUsed').set(memUsage.heapUsed);
    this.memoryUsage.labels('heapTotal').set(memUsage.heapTotal);
    this.memoryUsage.labels('external').set(memUsage.external);
  }

  /**
   * Update CPU usage
   */
  updateCPUUsage(cpuPercent: number) {
    this.cpuUsage.set(cpuPercent);
  }

  /**
   * Update active connections
   */
  updateActiveConnections(count: number) {
    this.activeConnections.set(count);
  }

  /**
   * Increment active connections
   */
  incrementActiveConnections() {
    this.activeConnections.inc();
  }

  /**
   * Decrement active connections
   */
  decrementActiveConnections() {
    this.activeConnections.dec();
  }

  /**
   * Get metrics for Prometheus
   */
  async getMetrics(): Promise<string> {
    return register.metrics();
  }

  /**
   * Get custom metrics summary
   */
  getMetricsSummary() {
    const httpRequests = this.httpRequestTotal.get();
    const mcpOperations = this.mcpOperationTotal.get();
    const domainScans = this.domainScanTotal.get();
    const authentications = this.authenticationTotal.get();
    const cacheHits = this.cacheHits.get();
    const cacheMisses = this.cacheMisses.get();
    const rateLimitHits = this.rateLimitHits.get();
    const memoryUsage = this.memoryUsage.get();
    const cpuUsage = this.cpuUsage.get();
    const activeConnections = this.activeConnections.get();

    return {
      httpRequests,
      mcpOperations,
      domainScans,
      authentications,
      cacheHits,
      cacheMisses,
      rateLimitHits,
      memoryUsage,
      cpuUsage,
      activeConnections,
    };
  }

  /**
   * Create a timer for tracking operation duration
   */
  startTimer(operation: string, tool: string) {
    const start = Date.now();
    
    return {
      end: (status: string = 'success') => {
        const duration = (Date.now() - start) / 1000;
        this.trackMCPOperation(operation, tool, status, duration);
        return duration;
      }
    };
  }

  /**
   * Create a timer for domain scan tracking
   */
  startScanTimer(scanDepth: string) {
    const start = Date.now();
    
    return {
      end: (status: string = 'success') => {
        const duration = (Date.now() - start) / 1000;
        this.trackDomainScan(scanDepth, status, duration);
        return duration;
      }
    };
  }

  /**
   * Reset all metrics (useful for testing)
   */
  reset() {
    register.clear();
    client.collectDefaultMetrics({ register });
  }

  /**
   * Get health status based on metrics
   */
  getHealthStatus() {
    const memUsage = process.memoryUsage();
    const memUsageMB = Math.round(memUsage.heapUsed / 1024 / 1024);
    
    // Simple health checks
    const health = {
      status: 'healthy' as 'healthy' | 'degraded' | 'unhealthy',
      checks: {
        memory: memUsage.heapUsed < 1000 * 1000 * 1000, // Less than 1GB
        connections: true, // Simplified - assume healthy
      },
      metrics: {
        memoryUsageMB: memUsageMB,
        activeConnections: 0, // Simplified
      }
    };
    
    // Determine overall health status
    const failedChecks = Object.values(health.checks).filter(check => !check).length;
    if (failedChecks === 0) {
      health.status = 'healthy';
    } else if (failedChecks <= 1) {
      health.status = 'degraded';
    } else {
      health.status = 'unhealthy';
    }
    
    return health;
  }
}

export const metrics = new MetricsService();
