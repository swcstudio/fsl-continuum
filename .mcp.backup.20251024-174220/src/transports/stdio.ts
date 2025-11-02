import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { ZeroServeMCPServer } from '../mcp/server-simple';

/**
 * Start ZeroServe MCP Server with STDIO transport
 * For use with Claude Desktop and similar clients
 */
export async function startStdioServer(): Promise<void> {
  const zeroserveServer = new ZeroServeMCPServer();
  const server = zeroserveServer.getServer();
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error('ZeroServe MCP Server started with STDIO transport');
}
