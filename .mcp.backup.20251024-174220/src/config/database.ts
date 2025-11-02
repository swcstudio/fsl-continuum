/**
 * Database configuration for enterprise ZeroServe MCP Server
 */

export interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
  ssl: boolean;
  maxConnections: number;
  connectionTimeout: number;
}

export interface RedisConfig {
  host: string;
  port: number;
  password?: string;
  db: number;
  maxRetriesPerRequest: number;
  retryDelayOnFailover: number;
}

export interface MongoDBConfig {
  uri: string;
  database: string;
  maxPoolSize: number;
  minPoolSize: number;
  maxIdleTimeMS: number;
  serverSelectionTimeoutMS: number;
}

export const getDatabaseConfig = (): DatabaseConfig => ({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'zeroserve',
  username: process.env.DB_USER || 'zeroserve',
  password: process.env.DB_PASSWORD || 'password',
  ssl: process.env.DB_SSL === 'true',
  maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS || '20'),
  connectionTimeout: parseInt(process.env.DB_CONNECTION_TIMEOUT || '60000'),
});

export const getRedisConfig = (): RedisConfig => ({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  db: parseInt(process.env.REDIS_DB || '0'),
  maxRetriesPerRequest: parseInt(process.env.REDIS_MAX_RETRIES || '3'),
  retryDelayOnFailover: parseInt(process.env.REDIS_RETRY_DELAY || '100'),
});

export const getMongoConfig = (): MongoDBConfig => ({
  uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/zeroserve',
  database: process.env.MONGODB_DB || 'zeroserve',
  maxPoolSize: parseInt(process.env.MONGO_MAX_POOL_SIZE || '10'),
  minPoolSize: parseInt(process.env.MONGO_MIN_POOL_SIZE || '2'),
  maxIdleTimeMS: parseInt(process.env.MONGO_MAX_IDLE_TIME || '30000'),
  serverSelectionTimeoutMS: parseInt(process.env.MONGO_SERVER_SELECTION_TIMEOUT || '5000'),
});
