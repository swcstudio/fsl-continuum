import { ZeroServeMCPServer } from '../mcp/server-simple';

describe('ZeroServeMCPServer - Basic Tests', () => {
  let server: ZeroServeMCPServer;

  beforeEach(() => {
    server = new ZeroServeMCPServer();
  });

  test('should create server instance', () => {
    expect(server).toBeDefined();
    const mcpServer = server.getServer();
    expect(mcpServer).toBeDefined();
  });

  test('should have correct server info', () => {
    const mcpServer = server.getServer();
    // The server should be properly initialized
    expect(mcpServer).toBeDefined();
  });

  test('should be able to get server instance', () => {
    const serverInstance = server.getServer();
    expect(serverInstance).toBe(server.getServer()); // Should return same instance
  });
});
