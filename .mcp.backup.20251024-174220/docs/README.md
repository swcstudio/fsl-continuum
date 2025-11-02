# ZeroServe MCP Server

AI-native domain scanning and infrastructure analysis built with the Model Context Protocol (MCP).

## Features

- **Domain Intelligence Scanning**: Comprehensive domain infrastructure analysis
- **Batch Processing**: Efficient scanning of multiple domains with concurrency control
- **Real-time Progress Notifications**: Live updates during long-running scans
- **AI-Powered Analysis**: Intelligent insights and recommendations
- **Multi-Transport Support**: STDIO for Claude Desktop, HTTP for web clients
- **Caching & Performance**: Built-in caching with configurable TTL
- **Security Analysis**: SSL/TLS checks, security headers, vulnerability detection
- **Technology Detection**: Identify underlying technologies and frameworks

## Quick Start

### Installation

```bash
# Install globally
npm install -g @zeroserve/mcp-server

# Or use with npx (no installation required)
npx @zeroserve/mcp-server
```

### Usage

#### Claude Desktop (STDIO Transport)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zeroserve": {
      "command": "npx",
      "args": ["-y", "@zeroserve/mcp-server", "stdio"],
      "env": {
        "ZEROSERVE_CACHE_TTL": "300000",
        "ZEROSERVE_RATE_LIMIT": "30"
      }
    }
  }
}
```

#### VS Code (HTTP Transport)

Install via VS Code Marketplace or configure manually:

```json
{
  "mcp": {
    "servers": {
      "zeroserve": {
        "command": "npx",
        "args": ["-y", "@zeroserve/mcp-server", "http"],
        "env": {
          "PORT": "3000"
        }
      }
    }
  }
}
```

#### Command Line

```bash
# Start with STDIO transport (default)
zeroserve-mcp stdio

# Start with HTTP transport on port 3000
zeroserve-mcp http 3000

# Show help
zeroserve-mcp help
```

## Available Tools

### `scan-domain`
Scan a single domain for infrastructure analysis.

**Parameters:**
- `domain` (string, required): Domain to scan
- `scanDepth` (enum): `basic` | `standard` | `comprehensive` (default: `standard`)
- `includeSubdomains` (boolean): Include subdomain analysis (default: `false`)

**Example:**
```
Scan the domain example.com with comprehensive analysis
```

### `batch-scan`
Scan multiple domains efficiently with concurrency control.

**Parameters:**
- `domains` (array, required): List of domains to scan (max: 100)
- `options.concurrent` (number): Concurrent scans (min: 1, max: 10, default: 3)
- `options.scanDepth` (enum): Scan depth (default: `standard`)
- `options.includeSubdomains` (boolean): Include subdomains (default: `false`)

**Example:**
```
Batch scan the domains ["example.com", "test.com", "demo.com"] with 5 concurrent scans
```

### `list-cached-scans`
List all cached domain scans with timestamps.

### `clear-cache`
Clear all cached scan results.

## Resources

### `domain://{domain}/data`
Complete domain infrastructure analysis data.

### `scans://{scanId}`
Detailed scan results and recommendations in markdown format.

## Prompts

### `analyze-domain`
AI-powered domain infrastructure analysis and recommendations.

**Parameters:**
- `domain` (string, required): Domain to analyze
- `focus` (enum): `security` | `performance` | `technologies` | `compliance`

### `security-audit`
Comprehensive security audit and vulnerability assessment.

**Parameters:**
- `domain` (string, required): Domain to audit
- `depth` (enum): `basic` | `comprehensive`

## Scan Results

Each scan provides:

```typescript
interface DomainScanResult {
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
```

## Configuration

### Environment Variables

- `PORT`: HTTP transport port (default: 3000)
- `NODE_ENV`: Environment (development/production)
- `ZEROSERVE_CACHE_TTL`: Cache TTL in milliseconds (default: 300000)
- `ZEROSERVE_RATE_LIMIT`: Rate limit per minute (default: 30)
- `ZEROSERVE_MAX_CONCURRENT`: Maximum concurrent scans (default: 5)

### Scan Depths

- **Basic**: DNS lookup and basic connectivity
- **Standard**: Basic + whois information and security headers
- **Comprehensive**: Standard + web crawling, technology detection, and performance analysis

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/zeroserve/mcp-server.git
cd mcp-server

# Install dependencies
npm install

# Build TypeScript
npm run build

# Run in development mode
npm run dev stdio
npm run dev http
```

### Testing

```bash
# Run tests
npm test

# Lint code
npm run lint
```

### Build

```bash
# Build for production
npm run build

# Create package
npm pack
```

## Integration Examples

### Python Client

```python
import requests
import json

# HTTP endpoint
url = "http://localhost:3000/mcp"

# Scan domain
payload = {
    "method": "tools/call",
    "params": {
        "name": "scan-domain",
        "arguments": {
            "domain": "example.com",
            "scanDepth": "comprehensive"
        }
    }
}

response = requests.post(url, json=payload)
result = response.json()
print(json.dumps(result, indent=2))
```

### JavaScript Client

```javascript
const response = await fetch('http://localhost:3000/mcp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    method: 'tools/call',
    params: {
      name: 'scan-domain',
      arguments: {
        domain: 'example.com',
        scanDepth: 'standard'
      }
    }
  })
});

const result = await response.json();
console.log(result);
```

## API Reference

### HTTP Endpoints

- `POST /mcp`: Main MCP protocol endpoint
- `GET /health`: Health check and server status
- `GET /`: Server information and documentation

### STDIO Protocol

Implements the full Model Context Protocol specification for integration with Claude Desktop and other MCP clients.

## Security & Privacy

- **Input Validation**: All inputs are validated using Zod schemas
- **Rate Limiting**: Configurable rate limiting to prevent abuse
- **Secure Defaults**: Security-focused default configurations
- **No Data Storage**: Results are cached in memory only
- **Privacy-First**: No personal data collected or transmitted

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/zeroserve/mcp-server/issues)
- **Discussions**: [Community discussions](https://github.com/zeroserve/mcp-server/discussions)
- **Documentation**: [Full documentation](https://zeroserve.github.io/mcp-server)

---

*Built with ❤️ using the Model Context Protocol*
