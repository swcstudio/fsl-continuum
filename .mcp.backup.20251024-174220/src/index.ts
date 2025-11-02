import { ZeroServeMCPServer } from './mcp/server-simple';
import { ZeroServeEnterpriseMCPServer } from './mcp/server-enterprise';
import { startStdioServer } from './transports/stdio';
import { startHTTPServer } from './transports/http';

// Export both server classes
export { ZeroServeMCPServer, ZeroServeEnterpriseMCPServer };

// Export transport starters
export { startStdioServer, startHTTPServer };

// Auto-start based on command line arguments
export async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const transport = args[0] || 'stdio';
  const enterprise = args.includes('--enterprise') || process.env.ZEROSERVE_ENTERPRISE === 'true';
  
  console.error('ZeroServe MCP Server v2.0.0 (Enterprise Edition)');
  console.error(`Enterprise Features: ${enterprise ? 'ENABLED' : 'DISABLED'}`);
  console.error(`Starting with ${transport.toUpperCase()} transport...`);
  
  try {
    if (enterprise) {
      // Use enterprise server
      switch (transport) {
        case 'stdio':
        case '--stdio':
          console.error('STDIO transport not yet available for enterprise server. Use HTTP transport.');
          process.exit(1);
          
        case 'http':
        case '--http':
          const port = parseInt(args[1] || process.env.PORT || '3000');
          const enterpriseServer = new ZeroServeEnterpriseMCPServer(port);
          await enterpriseServer.start();
          break;
          
        default:
          throw new Error(`Unknown transport: ${transport}`);
      }
    } else {
      // Use simple server
      switch (transport) {
        case 'stdio':
        case '--stdio':
          await startStdioServer();
          break;
          
        case 'http':
        case '--http':
          const port = parseInt(args[1] || process.env.PORT || '3000');
          await startHTTPServer(port);
          break;
          
        case 'help':
        case '--help':
        case '-h':
          console.log(`
ZeroServe Enterprise MCP Server - AI-native domain scanning and infrastructure analysis

USAGE:
  zeroserve-mcp [transport] [options]

TRANSPORTS:
  stdio                    STDIO transport (default, for Claude Desktop)
  http [port]              HTTP transport (for web clients, VS Code)
  
OPTIONS:
  --enterprise               Enable enterprise features (authentication, monitoring, etc.)

EXAMPLES:
  zeroserve-mcp stdio                           # Start with STDIO transport
  zeroserve-mcp http 3000                       # Start with HTTP transport on port 3000
  zeroserve-mcp http 3000 --enterprise          # Start with enterprise features enabled
  ZEROSERVE_ENTERPRISE=true zeroserve-mcp http   # Start with enterprise features via environment variable

FOR Claude Desktop:
  Add to claude_desktop_config.json:
  {
    "mcpServers": {
      "zeroserve": {
        "command": "npx",
        "args": ["-y", "@zeroserve/mcp-server", "stdio"]
      }
    }
  }

FOR VS Code with Enterprise Features:
  Install from VS Code Marketplace or configure manually:
  {
    "mcp": {
      "servers": {
        "zeroserve": {
          "command": "npx",
          "args": ["-y", "@zeroserve/mcp-server", "http", "--enterprise"]
        }
      }
    }
  }

ENTERPRISE FEATURES:
  ✅ JWT Authentication & API Keys
  ✅ Role-Based Access Control (RBAC)
  ✅ Rate Limiting & Throttling
  ✅ Advanced Monitoring & Metrics
  ✅ Security Headers & CORS
  ✅ Request Logging & Audit Trails
  ✅ Health Checks & Performance Tracking
  ✅ Prometheus Metrics Integration
  ✅ Enterprise-Grade Error Handling

ENVIRONMENT VARIABLES:
  PORT                      Port for HTTP transport (default: 3000)
  NODE_ENV                  Environment (development/production)
  ZEROSERVE_ENTERPRISE      Enable enterprise features (true/false)
  JWT_SECRET                 JWT secret key (required for enterprise)
  LOG_LEVEL                  Logging level (info, debug, warn, error)
  RATE_LIMIT_MAX             Global rate limit per minute
  DB_HOST                   Database host (for enterprise database)
  DB_USER                   Database username
  DB_PASSWORD               Database password
  REDIS_HOST                Redis host
  ELASTICSEARCH_URL          Elasticsearch URL for logging
        `);
          process.exit(0);
          
        default:
          throw new Error(`Unknown transport: ${transport}`);
      }
    }
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Start server if this file is run directly
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}
