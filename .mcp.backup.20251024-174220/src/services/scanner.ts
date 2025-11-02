import axios from 'axios';
import * as whois from 'whois';
import * as ping from 'ping';
import { load } from 'cheerio';
import { DomainScanResult, ScanProgress, CachedResult, ScanConfig } from '../types';
import { ValidationError, NetworkError, RateLimitError } from '../utils/validation';

/**
 * Domain scanning service
 */
export class DomainScanner {
  private cache = new Map<string, CachedResult>();
  private rateLimitMap = new Map<string, number>();
  private config: ScanConfig;

  constructor(config: ScanConfig = {
    defaultScanDepth: 'standard',
    maxConcurrentScans: 5,
    cacheTimeoutMs: 5 * 60 * 1000, // 5 minutes
    rateLimitPerMinute: 30
  }) {
    this.config = config;
  }

  /**
   * Generate unique scan ID
   */
  private generateScanId(): string {
    return `scan_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Check cache for existing results
   */
  private getCachedResult(domain: string): DomainScanResult | null {
    const cached = this.cache.get(domain);
    if (cached && (Date.now() - cached.timestamp) < this.config.cacheTimeoutMs) {
      return cached.data;
    }
    return null;
  }

  /**
   * Store result in cache
   */
  private setCachedResult(domain: string, result: DomainScanResult): void {
    this.cache.set(domain, {
      data: result,
      timestamp: Date.now()
    });
  }

  /**
   * Check rate limiting
   */
  private checkRateLimit(): void {
    const now = Date.now();
    const minuteAgo = now - 60000;
    
    // Clean old entries
    for (const timestamp of this.rateLimitMap.keys()) {
      if (timestamp < minuteAgo) {
        this.rateLimitMap.delete(timestamp as string);
      }
    }
    
    // Check current rate
    if (this.rateLimitMap.size >= this.config.rateLimitPerMinute) {
      throw new RateLimitError(`Rate limit exceeded. Max ${this.config.rateLimitPerMinute} scans per minute.`);
    }
    
    // Add current request
    this.rateLimitMap.set(now.toString(), now);
  }

  /**
   * Perform DNS lookup
   */
  private async performDNSLookup(domain: string): Promise<any[]> {
    try {
      // Using system's dig command for more comprehensive DNS info
      const { exec } = require('child_process');
      const { promisify } = require('util');
      const execAsync = promisify(exec);
      
      const { stdout } = await execAsync(`dig +noall +answer ${domain} ANY`);
      const lines = stdout.trim().split('\n');
      
      const dnsRecords: any[] = [];
      for (const line of lines) {
        const parts = line.trim().split(/\s+/);
        if (parts.length >= 4) {
          dnsRecords.push({
            type: parts[3],
            records: [parts.slice(4).join(' ')]
          });
        }
      }
      
      return dnsRecords;
    } catch (error) {
      console.warn(`DNS lookup failed for ${domain}:`, error);
      return [];
    }
  }

  /**
   * Scan single domain
   */
  async scanDomain(
    domain: string, 
    scanDepth: 'basic' | 'standard' | 'comprehensive' = 'standard',
    onProgress?: (progress: ScanProgress) => void
  ): Promise<DomainScanResult> {
    const scanId = this.generateScanId();
    const sanitizedDomain = domain.toLowerCase().trim();

    // Check rate limit
    this.checkRateLimit();

    // Check cache first
    const cached = this.getCachedResult(sanitizedDomain);
    if (cached) {
      return cached;
    }

    // Send initial progress
    onProgress?.({
      scanId,
      domain: sanitizedDomain,
      status: 'started',
      progress: 0
    });

    try {
      // Start scanning
      onProgress?.({
        scanId,
        domain: sanitizedDomain,
        status: 'scanning',
        progress: 10
      });

      const result: DomainScanResult = {
        scanId,
        domain: sanitizedDomain,
        timestamp: new Date().toISOString(),
        scanDepth,
        infrastructure: {
          dns: [],
          technologies: [],
          security: {
            ssl: { enabled: false },
            headers: {},
            vulnerabilities: []
          },
          performance: {
            responseTime: 0,
            uptime: 0,
            size: 0,
            loadTime: 0
          }
        },
        analysis: {
          riskLevel: 'low',
          recommendations: [],
          insights: []
        }
      };

      // DNS Analysis
      onProgress?.({
        scanId,
        domain: sanitizedDomain,
        status: 'scanning',
        progress: 30
      });

      result.infrastructure.dns = await this.performDNSLookup(sanitizedDomain);

      // Whois analysis
      onProgress?.({
        scanId,
        domain: sanitizedDomain,
        status: 'scanning',
        progress: 50
      });

      if (scanDepth !== 'basic') {
        try {
          const whoisData = await this.performWhois(sanitizedDomain);
          // Process whois data and add to analysis
          result.analysis.insights.push(`Domain registered: ${whoisData.creationDate || 'Unknown'}`);
        } catch (error) {
          console.warn(`Whois failed for ${sanitizedDomain}:`, error);
        }
      }

      // Web crawling and analysis
      onProgress?.({
        scanId,
        domain: sanitizedDomain,
        status: 'scanning',
        progress: 70
      });

      if (scanDepth === 'comprehensive') {
        const webData = await this.performWebCrawl(sanitizedDomain);
        result.webData = webData;
        
        // Technology detection
        result.infrastructure.technologies = this.detectTechnologies(webData);
      }

      // Performance testing
      onProgress?.({
        scanId,
        domain: sanitizedDomain,
        status: 'scanning',
        progress: 85
      });

      result.infrastructure.performance = await this.performPerformanceTest(sanitizedDomain);

      // Security analysis
      result.infrastructure.security = await this.performSecurityAnalysis(sanitizedDomain);

      // Generate recommendations
      onProgress?.({
        scanId,
        domain: sanitizedDomain,
        status: 'scanning',
        progress: 95
      });

      result.analysis = this.generateAnalysis(result);

      // Cache result
      this.setCachedResult(sanitizedDomain, result);

      // Send final progress
      onProgress?.({
        scanId,
        domain: sanitizedDomain,
        status: 'completed',
        progress: 100
      });

      return result;

    } catch (error) {
      onProgress?.({
        scanId,
        domain: sanitizedDomain,
        status: 'error',
        progress: 0,
        message: error instanceof Error ? error.message : 'Unknown error'
      });
      
      throw error;
    }
  }

  /**
   * Perform whois lookup
   */
  private async performWhois(domain: string): Promise<any> {
    return new Promise((resolve, reject) => {
      whois.lookup(domain, (error: any, data: any) => {
        if (error) {
          reject(error);
        } else {
          resolve(data);
        }
      });
    });
  }

  /**
   * Perform web crawling
   */
  private async performWebCrawl(domain: string): Promise<any> {
    try {
      const response = await axios.get(`https://${domain}`, {
        timeout: 10000,
        headers: {
          'User-Agent': 'ZeroServe-MCP/1.0 (Domain Scanner)'
        }
      });

      const $ = load(response.data);
      
      return {
        title: $('title').text() || '',
        description: $('meta[name="description"]').attr('content') || '',
        headings: $('h1, h2, h3').map((_, el) => $(el).text()).get(),
        links: $('a').length,
        images: $('img').length,
        statusCode: response.status,
        size: response.data.length
      };
    } catch (error) {
      throw new NetworkError(`Failed to crawl ${domain}: ${error}`);
    }
  }

  /**
   * Detect technologies from web data
   */
  private detectTechnologies(webData: any): string[] {
    const technologies: string[] = [];
    
    // Basic detection based on patterns
    if (webData.title) {
      const title = webData.title.toLowerCase();
      if (title.includes('wordpress')) technologies.push('WordPress');
      if (title.includes('shopify')) technologies.push('Shopify');
      if (title.includes('drupal')) technologies.push('Drupal');
      if (title.includes('joomla')) technologies.push('Joomla');
    }
    
    // Add more sophisticated detection logic here
    return technologies;
  }

  /**
   * Perform performance test
   */
  private async performPerformanceTest(domain: string): Promise<any> {
    try {
      const startTime = Date.now();
      const pingResult = await ping.promise.probe(domain);
      const responseTime = Date.now() - startTime;
      
      return {
        responseTime: pingResult.time || responseTime,
        uptime: pingResult.alive ? 100 : 0,
        size: 0,
        loadTime: responseTime
      };
    } catch (error) {
      return {
        responseTime: 9999,
        uptime: 0,
        size: 0,
        loadTime: 9999
      };
    }
  }

  /**
   * Perform security analysis
   */
  private async performSecurityAnalysis(domain: string): Promise<any> {
    try {
      const response = await axios.get(`https://${domain}`, {
        timeout: 5000,
        validateStatus: () => true
      });

      const headers: any = response.headers;
      const securityInfo = {
        ssl: {
          enabled: response.request.socket?.encrypted || false,
          issuer: '', // Would need SSL cert parsing
          expires: '', // Would need SSL cert parsing
          valid: response.request.socket?.encrypted || false
        },
        headers: {},
        vulnerabilities: [] as string[]
      };

      // Check security headers
      const securityHeaders = [
        'strict-transport-security',
        'x-frame-options',
        'x-content-type-options',
        'x-xss-protection',
        'content-security-policy'
      ];

      for (const header of securityHeaders) {
        if (headers[header]) {
          securityInfo.headers[header] = headers[header];
        } else {
          securityInfo.vulnerabilities.push(`Missing ${header} header`);
        }
      }

      return securityInfo;
    } catch (error) {
      return {
        ssl: { enabled: false },
        headers: {},
        vulnerabilities: ['Failed to perform security analysis']
      };
    }
  }

  /**
   * Generate analysis and recommendations
   */
  private generateAnalysis(result: DomainScanResult): any {
    const recommendations: string[] = [];
    const insights: string[] = [];
    let riskLevel: 'low' | 'medium' | 'high' = 'low';

    // DNS analysis
    if (result.infrastructure.dns.length === 0) {
      riskLevel = 'high';
      recommendations.push('No DNS records found - domain may be misconfigured');
    }

    // Security analysis
    if (!result.infrastructure.security.ssl.enabled) {
      riskLevel = 'medium';
      recommendations.push('Enable SSL/TLS encryption');
    }

    if (result.infrastructure.security.vulnerabilities.length > 0) {
      riskLevel = 'medium';
      recommendations.push('Address security header vulnerabilities');
    }

    // Performance analysis
    if (result.infrastructure.performance.responseTime > 1000) {
      riskLevel = 'medium';
      recommendations.push('Optimize server response time');
    }

    // Technology insights
    if (result.infrastructure.technologies.length > 0) {
      insights.push(`Detected technologies: ${result.infrastructure.technologies.join(', ')}`);
    }

    if (result.webData) {
      insights.push(`Website has ${result.webData.links} links and ${result.webData.images} images`);
    }

    return {
      riskLevel,
      recommendations,
      insights
    };
  }

  /**
   * Batch scan multiple domains
   */
  async batchScan(
    domains: string[],
    options: {
      concurrent?: number;
      scanDepth?: 'basic' | 'standard' | 'comprehensive';
    } = {},
    onProgress?: (progress: ScanProgress) => void
  ): Promise<DomainScanResult[]> {
    const concurrent = Math.min(options.concurrent || 3, this.config.maxConcurrentScans);
    const scanDepth = options.scanDepth || 'standard';
    
    const results: DomainScanResult[] = [];
    const chunks = this.chunkArray(domains, concurrent);
    
    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      const chunkPromises = chunk.map(domain => 
        this.scanDomain(domain, scanDepth, onProgress)
      );
      
      const chunkResults = await Promise.all(chunkPromises);
      results.push(...chunkResults);
    }
    
    return results;
  }

  /**
   * Helper function to chunk array
   */
  private chunkArray<T>(array: T[], chunkSize: number): T[][] {
    const chunks: T[][] = [];
    for (let i = 0; i < array.length; i += chunkSize) {
      chunks.push(array.slice(i, i + chunkSize));
    }
    return chunks;
  }
}
