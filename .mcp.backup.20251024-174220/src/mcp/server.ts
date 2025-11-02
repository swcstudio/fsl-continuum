import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { DomainScanner } from '../services/scanner';
import { ScanCache } from '../services/cache';
import { DomainScanResult, ScanProgress } from '../types';
import { 
  scanDomainSchema, 
  batchScanSchema, 
  ValidationError,
  NetworkError,
  RateLimitError 
} from '../utils/validation';

/**
 * ZeroServe MCP Server implementation
 */
export class ZeroServeMCPServer {
  private server: McpServer;
  private scanner: DomainScanner;
  private cache: ScanCache;

  constructor() {
    this.server = new McpServer({
      name: 'zeroserve',
      version: '1.0.0'
    });

    this.scanner = new DomainScanner();
    this.cache = new ScanCache();

    this.setupTools();
    this.setupResources();
    this.setupPrompts();
  }

  /**
   * Setup MCP tools
   */
  private setupTools(): void {
    // Domain scanning tool
    this.server.registerTool(
      'scan-domain',
      {
        title: 'Domain Infrastructure Scanner',
        description: 'Comprehensive domain and infrastructure analysis',
        inputSchema: {
          domain: z.string().refine(
            (val) => {
              const domainRegex = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
              return domainRegex.test(val) && val.length <= 253;
            },
            { message: "Invalid domain format" }
          ),
          scanDepth: z.enum(['basic', 'standard', 'comprehensive']).default('standard'),
          includeSubdomains: z.boolean().default(false)
        },
        outputSchema: {
          scanId: z.string(),
          domain: z.string(),
          timestamp: z.string(),
          scanDepth: z.enum(['basic', 'standard', 'comprehensive']),
          infrastructure: z.object({
            dns: z.array(z.object({
              type: z.string(),
              records: z.array(z.string())
            })),
            technologies: z.array(z.string()),
            security: z.object({
              ssl: z.object({
                enabled: z.boolean(),
                issuer: z.string().optional(),
                expires: z.string().optional(),
                valid: z.boolean().optional()
              }),
              headers: z.record(z.string()),
              vulnerabilities: z.array(z.string())
            }),
            performance: z.object({
              responseTime: z.number(),
              uptime: z.number(),
              size: z.number(),
              loadTime: z.number()
            })
          }),
          analysis: z.object({
            riskLevel: z.enum(['low', 'medium', 'high']),
            recommendations: z.array(z.string()),
            insights: z.array(z.string())
          })
        }
      },
      async ({ domain, scanDepth, includeSubdomains }) => {
        try {
          const result = await this.scanner.scanDomain(
            domain, 
            scanDepth,
            (progress: ScanProgress) => {
              // Send progress notification
              this.server.sendNotification?.('notifications/progress', {
                scanId: progress.scanId,
                domain: progress.domain,
                status: progress.status,
                progress: progress.progress,
                message: progress.message
              });
            }
          );

          return {
            content: [{
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }],
            structuredContent: result as any
          };
        } catch (error) {
          if (error instanceof ValidationError) {
            throw new Error(`Validation error: ${error.message}${error.field ? ` (field: ${error.field})` : ''}`);
          } else if (error instanceof RateLimitError) {
            throw new Error(`Rate limit exceeded: ${error.message}`);
          } else if (error instanceof NetworkError) {
            throw new Error(`Network error scanning ${domain}: ${error.message}`);
          } else {
            throw new Error(`Unexpected error scanning ${domain}: ${error instanceof Error ? error.message : 'Unknown error'}`);
          }
        }
      }
    );

    // Batch scanning tool
    this.server.registerTool(
      'batch-scan',
      {
        title: 'Batch Domain Scanner',
        description: 'Scan multiple domains efficiently with concurrency control',
        inputSchema: {
          domains: z.array(z.string()).min(1).max(100),
          options: z.object({
            concurrent: z.number().min(1).max(10).default(3),
            scanDepth: z.enum(['basic', 'standard', 'comprehensive']).default('standard'),
            includeSubdomains: z.boolean().default(false)
          }).default({})
        },
        outputSchema: {
          results: z.array(z.object({
            scanId: z.string(),
            domain: z.string(),
            timestamp: z.string(),
            scanDepth: z.enum(['basic', 'standard', 'comprehensive']),
            infrastructure: z.object({
              dns: z.array(z.object({
                type: z.string(),
                records: z.array(z.string())
              })),
              technologies: z.array(z.string()),
              security: z.object({
                ssl: z.object({
                  enabled: z.boolean(),
                  issuer: z.string().optional(),
                  expires: z.string().optional(),
                  valid: z.boolean().optional()
                }),
                headers: z.record(z.string()),
                vulnerabilities: z.array(z.string())
              }),
              performance: z.object({
                responseTime: z.number(),
                uptime: z.number(),
                size: z.number(),
                loadTime: z.number()
              })
            }),
            analysis: z.object({
              riskLevel: z.enum(['low', 'medium', 'high']),
              recommendations: z.array(z.string()),
              insights: z.array(z.string())
            })
          })),
          summary: z.object({
            total: z.number(),
            completed: z.number(),
            errors: z.number()
          })
        }
      },
      async ({ domains, options }) => {
        try {
          const results = await this.scanner.batchScan(
            domains,
            {
              concurrent: options.concurrent,
              scanDepth: options.scanDepth
            },
            (progress: ScanProgress) => {
              // Send progress notification
              this.server.sendNotification?.('notifications/progress', {
                scanId: progress.scanId,
                domain: progress.domain,
                status: progress.status,
                progress: progress.progress,
                message: progress.message
              });
            }
          );

          const summary = {
            total: domains.length,
            completed: results.length,
            errors: domains.length - results.length
          };

          return {
            content: [{
              type: 'text',
              text: JSON.stringify({ results, summary }, null, 2)
            }],
            structuredContent: { results, summary } as any
          };
        } catch (error) {
          if (error instanceof RateLimitError) {
            throw new Error(`Rate limit exceeded: ${error.message}`);
          } else {
            throw new Error(`Batch scan error: ${error instanceof Error ? error.message : 'Unknown error'}`);
          }
        }
      }
    );

    // List cached scans tool
    this.server.registerTool(
      'list-cached-scans',
      {
        title: 'List Cached Scans',
        description: 'List all cached domain scans with timestamps',
        inputSchema: {},
        outputSchema: {
          cached: z.array(z.object({
            domain: z.string(),
            timestamp: z.string(),
            scanId: z.string()
          }))
        }
      },
      async () => {
        const stats = this.cache.getStats();
        const cached = stats.keys.map(domain => {
          const result = this.cache.get(domain);
          return {
            domain,
            timestamp: result?.timestamp || '',
            scanId: result?.scanId || ''
          };
        });

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ cached, total: cached.length }, null, 2)
          }],
          structuredContent: { cached, total: cached.length }
        };
      }
    );

    // Clear cache tool
    this.server.registerTool(
      'clear-cache',
      {
        title: 'Clear Scan Cache',
        description: 'Clear all cached scan results',
        inputSchema: {},
        outputSchema: {
          message: z.string()
        }
      },
      async () => {
        this.cache.clear();
        return {
          content: [{
            type: 'text',
            text: 'Cache cleared successfully'
          }],
          structuredContent: { message: 'Cache cleared successfully' } as any
        };
      }
    );
  }

  /**
   * Setup MCP resources
   */
  private setupResources(): void {
    // Domain data resources
    this.server.registerResource(
      'domain-data',
      new ResourceTemplate('domain://{domain}/data', {
        list: undefined,
        complete: {
          domain: async (value, context) => {
            // Return recently scanned domains for completion
            const stats = this.cache.getStats();
            return stats.keys
              .filter(domain => domain.toLowerCase().includes(value.toLowerCase()))
              .slice(0, 10);
          }
        }
      }),
      {
        title: 'Domain Analysis Data',
        description: 'Complete domain infrastructure analysis data'
      },
      async (uri, { domain }) => {
        try {
          // Check cache first
          const cached = this.cache.get(domain);
          if (cached) {
            return {
              contents: [{
                uri: uri.href,
                text: JSON.stringify(cached, null, 2),
                mimeType: 'application/json'
              }]
            };
          }

          // If not in cache, perform quick scan
          const result = await this.scanner.scanDomain(domain, 'basic');
          return {
            contents: [{
              uri: uri.href,
              text: JSON.stringify(result, null, 2),
              mimeType: 'application/json'
            }]
          };
        } catch (error) {
          return {
            contents: [{
              uri: uri.href,
              text: `Error retrieving domain data for ${domain}: ${error instanceof Error ? error.message : 'Unknown error'}`,
              mimeType: 'text/plain'
            }]
          };
        }
      }
    );

    // Scan results resources
    this.server.registerResource(
      'scan-results',
      new ResourceTemplate('scans://{scanId}', { list: undefined }),
      {
        title: 'Scan Results',
        description: 'Detailed scan results and recommendations'
      },
      async (uri, { scanId }) => {
        try {
          // Look for scan result in cache
          const stats = this.cache.getStats();
          for (const domain of stats.keys) {
            const result = this.cache.get(domain);
            if (result && result.scanId === scanId) {
              const report = await this.generateScanReport(result);
              return {
                contents: [{
                  uri: uri.href,
                  text: report,
                  mimeType: 'text/markdown'
                }]
              };
            }
          }

          return {
            contents: [{
              uri: uri.href,
              text: `Scan results not found for scan ID: ${scanId}`,
              mimeType: 'text/plain'
            }]
          };
        } catch (error) {
          return {
            contents: [{
              uri: uri.href,
              text: `Error retrieving scan results: ${error instanceof Error ? error.message : 'Unknown error'}`,
              mimeType: 'text/plain'
            }]
          };
        }
      }
    );
  }

  /**
   * Setup MCP prompts
   */
  private setupPrompts(): void {
    // Domain analysis prompt
    this.server.registerPrompt(
      'analyze-domain',
      {
        title: 'Domain Analysis Assistant',
        description: 'AI-powered domain infrastructure analysis and recommendations',
        argsSchema: {
          domain: {
            type: 'string',
            description: 'Domain to analyze',
            required: true
          },
          focus: {
            type: 'string',
            enum: ['security', 'performance', 'technologies', 'compliance'],
            description: 'Analysis focus area',
            required: false
          }
        }
      },
      async ({ domain, focus }) => {
        const focusText = focus ? ` with special focus on ${focus}` : '';
        const systemPrompt = `You are a domain infrastructure analysis expert. Analyze the provided domain data and give comprehensive insights${focusText}.`;

        // Try to get domain data
        let domainData = '';
        try {
          const cached = this.cache.get(domain);
          if (cached) {
            domainData = `\n\nDomain Analysis Data:\n${JSON.stringify(cached, null, 2)}`;
          }
        } catch (error) {
          console.warn(`Failed to get domain data for prompt: ${error}`);
        }

        return {
          messages: [
            {
              role: 'system',
              content: {
                type: 'text',
                text: systemPrompt
              }
            },
            {
              role: 'user',
              content: {
                type: 'text',
                text: `Analyze the domain ${domain}${focusText}. Provide comprehensive insights about infrastructure, security posture, performance, and actionable recommendations.${domainData}`
              }
            }
          ]
        };
      }
    );

    // Security audit prompt
    this.server.registerPrompt(
      'security-audit',
      {
        title: 'Security Audit Assistant',
        description: 'Comprehensive security audit and vulnerability assessment',
        argsSchema: {
          domain: {
            type: 'string',
            description: 'Domain to audit for security',
            required: true
          },
          depth: {
            type: 'string',
            enum: ['basic', 'comprehensive'],
            description: 'Security audit depth',
            required: false
          }
        }
      },
      async ({ domain, depth = 'basic' }) => {
        const systemPrompt = `You are a cybersecurity expert specializing in domain and infrastructure security audits. Conduct a thorough security analysis and provide detailed recommendations.`;

        let domainData = '';
        try {
          const cached = this.cache.get(domain);
          if (cached) {
            domainData = `\n\nSecurity Analysis Data:\n${JSON.stringify(cached.infrastructure.security, null, 2)}`;
            domainData += `\n\nDNS Records:\n${JSON.stringify(cached.infrastructure.dns, null, 2)}`;
          }
        } catch (error) {
          console.warn(`Failed to get domain data for security audit: ${error}`);
        }

        return {
          messages: [
            {
              role: 'system',
              content: {
                type: 'text',
                text: systemPrompt
              }
            },
            {
              role: 'user',
              content: {
                type: 'text',
                text: `Perform a ${depth} security audit for domain ${domain}. Identify vulnerabilities, assess security controls, and provide prioritized remediation recommendations.${domainData}`
              }
            }
          ]
        };
      }
    );
  }

  /**
   * Generate detailed scan report
   */
  private async generateScanReport(result: DomainScanResult): Promise<string> {
    const report = [
      `# Domain Analysis Report`,
      `**Domain:** ${result.domain}`,
      `**Scan ID:** ${result.scanId}`,
      `**Timestamp:** ${result.timestamp}`,
      `**Scan Depth:** ${result.scanDepth}`,
      `**Risk Level:** ${result.analysis.riskLevel.toUpperCase()}`,
      '',
      '## Infrastructure Analysis',
      '',
      '### DNS Records',
      result.infrastructure.dns.map(record => 
        `- **${record.type}:** ${record.records.join(', ')}`
      ).join('\n'),
      '',
      '### Technologies Detected',
      result.infrastructure.technologies.length > 0 
        ? result.infrastructure.technologies.map(tech => `- ${tech}`).join('\n')
        : 'No specific technologies detected',
      '',
      '### Security Analysis',
      `- **SSL/TLS:** ${result.infrastructure.security.ssl.enabled ? 'Enabled' : 'Disabled'}`,
      `- **Security Headers:** ${Object.keys(result.infrastructure.security.headers).length} configured`,
      `- **Vulnerabilities:** ${result.infrastructure.security.vulnerabilities.length} identified`,
      '',
      result.infrastructure.security.vulnerabilities.length > 0 
        ? '#### Identified Vulnerabilities:\n' + 
          result.infrastructure.security.vulnerabilities.map(vuln => `- ${vuln}`).join('\n')
        : '',
      '',
      '### Performance Metrics',
      `- **Response Time:** ${result.infrastructure.performance.responseTime}ms`,
      `- **Uptime:** ${result.infrastructure.performance.uptime}%`,
      `- **Load Time:** ${result.infrastructure.performance.loadTime}ms`,
      '',
      result.webData ? '## Web Analysis' : '',
      result.webData ? `- **Title:** ${result.webData.title}` : '',
      result.webData ? `- **Description:** ${result.webData.description}` : '',
      result.webData ? `- **Links:** ${result.webData.links}` : '',
      result.webData ? `- **Images:** ${result.webData.images}` : '',
      result.webData ? '' : '',
      '## Insights',
      result.analysis.insights.map(insight => `- ${insight}`).join('\n'),
      '',
      '## Recommendations',
      result.analysis.recommendations.map(rec => `- ${rec}`).join('\n'),
      '',
      '---',
      `*Report generated by ZeroServe MCP Server*`
    ];

    return report.join('\n');
  }

  /**
   * Get the MCP server instance
   */
  getServer(): McpServer {
    return this.server;
  }
}
