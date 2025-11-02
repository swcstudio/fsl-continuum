/**
 * Authentication and authorization configuration
 */

export interface AuthConfig {
  jwt: {
    secret: string;
    expiresIn: string;
    issuer: string;
    audience: string;
  };
  oauth: {
    google: {
      clientId: string;
      clientSecret: string;
      callbackURL: string;
    };
    microsoft: {
      clientId: string;
      clientSecret: string;
      callbackURL: string;
      tenantId?: string;
    };
  };
  rbac: {
    enabled: boolean;
    adminRoles: string[];
    defaultRole: string;
  };
  apiKeys: {
    enabled: boolean;
    headerName: string;
    queryParam: string;
  };
}

export interface UserRole {
  id: string;
  name: string;
  permissions: Permission[];
  rateLimit: {
    requestsPerMinute: number;
    requestsPerHour: number;
    requestsPerDay: number;
  };
}

export interface Permission {
  id: string;
  name: string;
  resource: string;
  action: string;
  description: string;
}

export const getAuthConfig = (): AuthConfig => ({
  jwt: {
    secret: process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-in-production',
    expiresIn: process.env.JWT_EXPIRES_IN || '24h',
    issuer: process.env.JWT_ISSUER || 'zeroserve-mcp',
    audience: process.env.JWT_AUDIENCE || 'zeroserve-users',
  },
  oauth: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
      callbackURL: process.env.GOOGLE_CALLBACK_URL || 'http://localhost:3000/auth/google/callback',
    },
    microsoft: {
      clientId: process.env.MICROSOFT_CLIENT_ID || '',
      clientSecret: process.env.MICROSOFT_CLIENT_SECRET || '',
      callbackURL: process.env.MICROSOFT_CALLBACK_URL || 'http://localhost:3000/auth/microsoft/callback',
      tenantId: process.env.MICROSOFT_TENANT_ID,
    },
  },
  rbac: {
    enabled: process.env.RBAC_ENABLED === 'true',
    adminRoles: (process.env.ADMIN_ROLES || 'admin,superadmin').split(','),
    defaultRole: process.env.DEFAULT_ROLE || 'viewer',
  },
  apiKeys: {
    enabled: process.env.API_KEYS_ENABLED === 'true',
    headerName: process.env.API_KEY_HEADER || 'X-API-Key',
    queryParam: process.env.API_KEY_PARAM || 'apiKey',
  },
});

export const defaultRoles: UserRole[] = [
  {
    id: 'admin',
    name: 'Administrator',
    permissions: [
      { id: 'all', name: 'All Permissions', resource: '*', action: '*', description: 'Full system access' }
    ],
    rateLimit: {
      requestsPerMinute: 1000,
      requestsPerHour: 60000,
      requestsPerDay: 1000000,
    },
  },
  {
    id: 'analyst',
    name: 'Domain Analyst',
    permissions: [
      { id: 'scan:read', name: 'Read Scan Results', resource: 'scans', action: 'read', description: 'View scan results and reports' },
      { id: 'scan:create', name: 'Create Scans', resource: 'scans', action: 'create', description: 'Create new domain scans' },
      { id: 'scan:batch', name: 'Batch Scanning', resource: 'scans', action: 'batch', description: 'Perform batch domain scans' },
      { id: 'tools:read', name: 'Use Tools', resource: 'tools', action: 'read', description: 'Access MCP tools' },
    ],
    rateLimit: {
      requestsPerMinute: 100,
      requestsPerHour: 6000,
      requestsPerDay: 50000,
    },
  },
  {
    id: 'viewer',
    name: 'Read Only User',
    permissions: [
      { id: 'scan:read', name: 'Read Scan Results', resource: 'scans', action: 'read', description: 'View scan results and reports' },
      { id: 'tools:read', name: 'Use Basic Tools', resource: 'tools', action: 'read', description: 'Access basic MCP tools' },
    ],
    rateLimit: {
      requestsPerMinute: 30,
      requestsPerHour: 1000,
      requestsPerDay: 5000,
    },
  },
];

export const rateLimitConfig = {
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000'), // 1 minute
  max: parseInt(process.env.RATE_LIMIT_MAX || '100'), // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
};

export const apiRateLimits = {
  'scan-domain': {
    requestsPerMinute: 10,
    requestsPerHour: 200,
    requestsPerDay: 1000,
  },
  'batch-scan': {
    requestsPerMinute: 2,
    requestsPerHour: 20,
    requestsPerDay: 100,
  },
  'list-cached-scans': {
    requestsPerMinute: 60,
    requestsPerHour: 1000,
    requestsPerDay: 10000,
  },
};
