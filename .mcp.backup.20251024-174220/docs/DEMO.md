# ZeroServe MCP Server Demo

This document demonstrates the working ZeroServe MCP Server implementation.

## Quick Start

### 1. Build the Project

```bash
npm install
npm run build
```

### 2. Test CLI Help

```bash
node dist/cli.js help
```

### 3. Start HTTP Server

```bash
node dist/cli.js http 3000
```

### 4. Test MCP Tools

#### Echo Tool

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "echo",
      "arguments": {
        "message": "Hello ZeroServe!"
      }
    },
    "id": 1
  }'
```

#### Domain Validation Tool

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "validate-domain",
      "arguments": {
        "domain": "example.com"
      }
    },
    "id": 2
  }'
```

## Expected Results

### Echo Tool Response
```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Echo: Hello ZeroServe!"
      }
    ]
  },
  "jsonrpc": "2.0",
  "id": 1
}
```

### Domain Validation Response
```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Domain \"example.com\" is valid"
      }
    ]
  },
  "jsonrpc": "2.0",
  "id": 2
}
```

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zeroserve": {
      "command": "node",
      "args": ["/path/to/zeroserve-mcp/dist/cli.js", "stdio"]
    }
  }
}
```

## VS Code Integration

Add to your VS Code MCP configuration:

```json
{
  "mcp": {
    "servers": {
      "zeroserve": {
        "command": "node",
        "args": ["/path/to/zeroserve-mcp/dist/cli.js", "http"]
      }
    }
  }
}
```

## Features Demonstrated

1. ✅ MCP Protocol Compliance
2. ✅ Multi-Transport Support (STDIO + HTTP)
3. ✅ Tool Registration and Execution
4. ✅ Resource Management
5. ✅ Prompt System
6. ✅ Zod Input Validation
7. ✅ TypeScript Implementation
8. ✅ CORS Support for Web Clients
9. ✅ Health Check Endpoints
10. ✅ CLI Interface
11. ✅ Docker Support (Dockerfile included)
12. ✅ NPM Package Configuration

The current implementation provides a solid foundation that's fully compatible with Claude Desktop, VS Code, and other MCP clients.
