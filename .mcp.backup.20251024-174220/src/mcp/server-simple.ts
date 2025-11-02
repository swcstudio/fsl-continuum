import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

/**
 * Simplified ZeroServe MCP Server implementation for testing
 */
export class ZeroServeMCPServer {
  private server: McpServer;

  constructor() {
    this.server = new McpServer({
      name: 'zeroserve',
      version: '1.0.0'
    });

    this.setupBasicTools();
    this.setupBasicResources();
    this.setupBasicPrompts();
  }

  private setupBasicTools(): void {
    // Simple echo tool for testing
    this.server.registerTool(
      'echo',
      {
        title: 'Echo Tool',
        description: 'Echo back input messages',
        inputSchema: {
          message: z.string()
        }
      },
      async ({ message }) => {
        return {
          content: [{
            type: 'text',
            text: `Echo: ${message}`
          }]
        };
      }
    );

    // Simple domain validation tool
    this.server.registerTool(
      'validate-domain',
      {
        title: 'Domain Validator',
        description: 'Validate domain format',
        inputSchema: {
          domain: z.string()
        }
      },
      async ({ domain }) => {
        const domainRegex = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        const isValid = domainRegex.test(domain) && domain.length <= 253;
        
        return {
          content: [{
            type: 'text',
            text: `Domain "${domain}" is ${isValid ? 'valid' : 'invalid'}`
          }]
        };
      }
    );
  }

  private setupBasicResources(): void {
    this.server.registerResource(
      'test-data',
      new ResourceTemplate('test://{name}', { list: undefined }),
      {
        title: 'Test Resource',
        description: 'Test resource for demonstration'
      },
      async (uri, { name }) => ({
        contents: [{
          uri: uri.href,
          text: `Test data for: ${name}`,
          mimeType: 'text/plain'
        }]
      })
    );
  }

  private setupBasicPrompts(): void {
    this.server.registerPrompt(
      'test-prompt',
      {
        title: 'Test Prompt',
        description: 'A simple test prompt',
        argsSchema: {
          topic: z.string().optional()
        }
      },
      async ({ topic }) => {
        const topicText = topic ? ` about ${topic}` : '';
        return {
          messages: [{
            role: 'user',
            content: {
              type: 'text',
              text: `Please provide information${topicText}.`
            }
          }]
        };
      }
    );
  }

  getServer(): McpServer {
    return this.server;
  }
}
