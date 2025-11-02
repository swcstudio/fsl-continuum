// Type declarations for external packages without TypeScript definitions

declare module 'whois' {
  interface WhoisOptions {
    server?: string;
    timeout?: number;
    follow?: number;
  }

  interface WhoisResult {
    domain: string;
    creationDate?: string;
    expirationDate?: string;
    updatedDate?: string;
    registrar?: string;
    nameServers?: string[];
    status?: string[];
    [key: string]: any;
  }

  function lookup(domain: string, options?: WhoisOptions, callback?: (error: any, data: any) => void): Promise<WhoisResult>;
  function lookup(domain: string, callback?: (error: any, data: any) => void): Promise<WhoisResult>;
  export = lookup;
}

declare module 'ping' {
  interface PingConfig {
    timeout?: number;
    extra?: string[];
    minReply?: number;
    v6?: boolean;
  }

  interface PingResult {
    alive: boolean;
    output?: string;
    time?: number;
    packetLoss?: number;
    host?: string;
  }

  export const promise: {
    probe(addr: string, config?: PingConfig): Promise<PingResult>;
  };
}
