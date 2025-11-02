/**
 * Core type definitions for ZeroServe MCP Server
 */

export interface DomainScanResult {
  scanId: string;
  domain: string;
  timestamp: string;
  scanDepth: 'basic' | 'standard' | 'comprehensive';
  infrastructure: {
    dns: DNSRecord[];
    technologies: string[];
    security: SecurityInfo;
    performance: PerformanceInfo;
  };
  webData?: {
    title: string;
    description: string;
    headings: string[];
    links: number;
    images: number;
  };
  analysis: {
    riskLevel: 'low' | 'medium' | 'high';
    recommendations: string[];
    insights: string[];
  };
}

export interface DNSRecord {
  type: string;
  records: string[];
  ttl?: number;
}

export interface SecurityInfo {
  ssl: {
    enabled: boolean;
    issuer?: string;
    expires?: string;
    valid?: boolean;
  };
  headers: Record<string, string>;
  vulnerabilities: string[];
}

export interface PerformanceInfo {
  responseTime: number;
  uptime: number;
  size: number;
  loadTime: number;
}

export interface BatchScanOptions {
  concurrent: number;
  scanDepth: 'basic' | 'standard' | 'comprehensive';
  includeSubdomains: boolean;
}

export interface ScanProgress {
  scanId: string;
  domain: string;
  status: 'started' | 'scanning' | 'completed' | 'error';
  progress: number;
  message?: string;
}

export interface CachedResult {
  data: DomainScanResult;
  timestamp: number;
}

export interface APIKeys {
  zeroserve?: string;
  parallel?: string;
  jina?: string;
}

export interface ScanConfig {
  defaultScanDepth: 'basic' | 'standard' | 'comprehensive';
  maxConcurrentScans: number;
  cacheTimeoutMs: number;
  rateLimitPerMinute: number;
}
