/**
 * Logging service for enterprise ZeroServe MCP Server
 */

import winston from 'winston';
import pino from 'pino';
import { Request } from 'express';

// Define log levels
export enum LogLevel {
  ERROR = 'error',
  WARN = 'warn',
  INFO = 'info',
  DEBUG = 'debug',
  TRACE = 'trace',
}

export interface LogContext {
  userId?: string;
  requestId?: string;
  operation?: string;
  tool?: string;
  domain?: string;
  scanId?: string;
  ip?: string;
  userAgent?: string;
  duration?: number;
  errorCode?: string;
  [key: string]: any;
}

export class LoggingService {
  private logger: winston.Logger;
  private pinoLogger: pino.Logger;

  constructor() {
    // Initialize Winston logger
    this.logger = winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json(),
        winston.format.prettyPrint()
      ),
      defaultMeta: {
        service: 'zeroserve-mcp-server',
        version: process.env.npm_package_version || '2.0.0',
      },
      transports: [
        // Console transport for development
        new winston.transports.Console({
          format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple(),
            winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' })
          ),
        }),
        // File transport for production
        new winston.transports.File({
          filename: 'logs/error.log',
          level: 'error',
          format: winston.format.json(),
        }),
        new winston.transports.File({
          filename: 'logs/combined.log',
          format: winston.format.json(),
        }),
        // Rotating file for audit logs
        new winston.transports.File({
          filename: 'logs/audit.log',
          level: 'info',
          format: winston.format.json(),
          maxsize: 100 * 1024 * 1024, // 100MB
          maxFiles: 10,
        }),
      ],
    });

    // Initialize Pino logger (for high-performance logging)
    this.pinoLogger = pino({
      level: process.env.LOG_LEVEL || 'info',
      formatters: {
        level: (label) => {
          return { level: label };
        },
      },
      timestamp: pino.stdTimeFunctions.isoTime,
    });
  }

  /**
   * Error logging
   */
  error(message: string, context?: LogContext, error?: Error) {
    const logData = {
      level: 'error',
      message,
      timestamp: new Date().toISOString(),
      ...context,
      error: error ? {
        message: error.message,
        stack: error.stack,
        name: error.name,
      } : undefined,
    };

    this.logger.error(logData);
    this.pinoLogger.error(logData);
  }

  /**
   * Warning logging
   */
  warn(message: string, context?: LogContext) {
    const logData = {
      level: 'warn',
      message,
      timestamp: new Date().toISOString(),
      ...context,
    };

    this.logger.warn(logData);
    this.pinoLogger.warn(logData);
  }

  /**
   * Info logging
   */
  info(message: string, context?: LogContext) {
    const logData = {
      level: 'info',
      message,
      timestamp: new Date().toISOString(),
      ...context,
    };

    this.logger.info(logData);
    this.pinoLogger.info(logData);
  }

  /**
   * Debug logging
   */
  debug(message: string, context?: LogContext) {
    const logData = {
      level: 'debug',
      message,
      timestamp: new Date().toISOString(),
      ...context,
    };

    this.logger.debug(logData);
    this.pinoLogger.debug(logData);
  }

  /**
   * Audit logging (for compliance)
   */
  audit(action: string, userId: string, resource: string, details?: any, success: boolean = true) {
    const auditData = {
      type: 'audit',
      action,
      userId,
      resource,
      details,
      success,
      timestamp: new Date().toISOString(),
      ip: details?.ip,
      userAgent: details?.userAgent,
    };

    this.logger.info(auditData);
    this.pinoLogger.info(auditData);
  }

  /**
   * Security event logging
   */
  security(event: string, details: any) {
    const securityData = {
      type: 'security',
      event,
      details,
      timestamp: new Date().toISOString(),
      severity: this.determineSeverity(event),
    };

    this.logger.warn(securityData);
    this.pinoLogger.warn(securityData);
  }

  /**
   * Performance logging
   */
  performance(operation: string, duration: number, context?: LogContext) {
    const perfData = {
      type: 'performance',
      operation,
      duration,
      timestamp: new Date().toISOString(),
      ...context,
    };

    if (duration > 5000) { // Log as warning if > 5 seconds
      this.logger.warn(perfData);
      this.pinoLogger.warn(perfData);
    } else {
      this.logger.info(perfData);
      this.pinoLogger.info(perfData);
    }
  }

  /**
   * MCP operation logging
   */
  mcpOperation(operation: string, tool: string, userId: string, duration: number, status: string, details?: any) {
    const mcpData = {
      type: 'mcp_operation',
      operation,
      tool,
      userId,
      duration,
      status,
      details,
      timestamp: new Date().toISOString(),
    };

    this.logger.info(mcpData);
    this.pinoLogger.info(mcpData);
  }

  /**
   * Request logging middleware
   */
  requestLogger = (req: Request, res: any, next: () => void) => {
    const start = Date.now();
    const requestId = this.generateRequestId();

    // Add request ID to request
    (req as any).requestId = requestId;

    // Log request start
    this.info('Request started', {
      requestId,
      method: req.method,
      url: req.url,
      ip: req.ip,
      userAgent: req.get('User-Agent'),
      userId: (req as any).user?.id,
    });

    // Log response when it finishes
    res.on('finish', () => {
      const duration = Date.now() - start;
      
      this.info('Request completed', {
        requestId,
        method: req.method,
        url: req.url,
        statusCode: res.statusCode,
        duration,
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        userId: (req as any).user?.id,
      });
    });

    next();
  };

  /**
   * Generate unique request ID
   */
  private generateRequestId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Determine security event severity
   */
  private determineSeverity(event: string): 'low' | 'medium' | 'high' | 'critical' {
    const highSeverityEvents = [
      'brute_force_attempt',
      'sql_injection_attempt',
      'xss_attempt',
      'privilege_escalation',
      'data_breach',
    ];

    const mediumSeverityEvents = [
      'failed_login',
      'rate_limit_exceeded',
      'invalid_api_key',
      'unauthorized_access',
    ];

    if (highSeverityEvents.includes(event)) {
      return 'critical';
    } else if (mediumSeverityEvents.includes(event)) {
      return 'medium';
    } else {
      return 'low';
    }
  }

  /**
   * Health check for logging service
   */
  healthCheck() {
    return {
      status: 'healthy',
      transports: this.logger.transports.length,
      pinoEnabled: !!this.pinoLogger,
      level: process.env.LOG_LEVEL || 'info',
      timestamp: new Date().toISOString(),
    };
  }
}

export const logger = new LoggingService();
