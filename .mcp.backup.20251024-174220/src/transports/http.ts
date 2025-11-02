import express from 'express';
import cors from 'cors';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { ZeroServeMCPServer } from '../mcp/server-simple';

/**
 * Start ZeroServe MCP Server with HTTP transport
 * For use with web clients, VS Code, etc.
 */
export async function startHTTPServer(port: number = 3000): Promise<void> {
  const zeroserveServer = new ZeroServeMCPServer();
  const server = zeroserveServer.getServer();
  
  const app = express();
  
  // Enable CORS for all routes
  app.use(cors({
    origin: '*', // Allow any origin (use with caution in production)
    methods: ['GET', 'POST', 'DELETE'],
    allowedHeaders: ['Content-Type', 'X-Requested-With'],
    exposedHeaders: ['Content-Type', 'X-Protocol-Version']
  }));
  
  app.use(express.json({ limit: '10mb' }));
  
  // Health check endpoint
  app.get('/health', (req, res) => {
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      transport: 'http'
    });
  });
  
  // MCP endpoint
  app.post('/mcp', async (req, res) => {
    // Create new transport for each request to prevent session conflicts
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true
    });
    
    // Clean up transport when connection closes
    res.on('close', () => {
      transport.close();
    });
    
    try {
      // Connect server to transport
      await server.connect(transport);
      
      // Handle the MCP request
      await transport.handleRequest(req, res, req.body);
    } catch (error) {
      console.error('Error handling MCP request:', error);
      res.status(500).json({
        error: 'Internal server error',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  });
  
  // Root endpoint with server info
  app.get('/', (req, res) => {
    res.json({
      name: 'ZeroServe MCP Server',
      version: '1.0.0',
      description: 'AI-native domain scanning and infrastructure analysis',
      transport: 'Streamable HTTP',
      endpoints: {
        mcp: '/mcp',
        health: '/health'
      },
      documentation: 'https://github.com/zeroserve/mcp-server'
    });
  });
  
  return new Promise((resolve, reject) => {
    const httpServer = app.listen(port, () => {
      console.log(`ZeroServe MCP Server started with HTTP transport on port ${port}`);
      console.log(`MCP endpoint: http://localhost:${port}/mcp`);
      console.log(`Health check: http://localhost:${port}/health`);
      console.log(`Server info: http://localhost:${port}/`);
      resolve();
    });
    
    httpServer.on('error', (error: any) => {
      if (error.code === 'EADDRINUSE') {
        console.error(`Port ${port} is already in use`);
        reject(new Error(`Port ${port} is already in use`));
      } else {
        reject(error);
      }
    });
  });
}
