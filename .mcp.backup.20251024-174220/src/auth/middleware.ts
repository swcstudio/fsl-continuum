/**
 * Authentication middleware for Express.js
 */

import { Request, Response, NextFunction } from 'express';
import { JWTService, User, JWTPayload } from './jwt.service';
import { getAuthConfig } from '../config/auth';

export interface AuthenticatedRequest extends Request {
  user?: User;
  permissions?: string[];
  apiKey?: string;
}

export class AuthMiddleware {
  private jwtService = new JWTService();
  private config = getAuthConfig();

  /**
   * JWT authentication middleware
   */
  authenticate = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    try {
      const authHeader = req.headers.authorization;
      
      if (!authHeader) {
        return res.status(401).json({ error: 'No authorization header provided' });
      }

      const token = authHeader.replace('Bearer ', '');
      const payload = this.jwtService.verifyToken(token);

      // Mock user - in production, fetch from database
      const mockUser: User = {
        id: payload.userId,
        email: payload.email,
        role: payload.role,
        isActive: true,
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      req.user = mockUser;
      req.permissions = payload.permissions;

      next();
    } catch (error) {
      return res.status(401).json({ error: 'Invalid or expired token' });
    }
  };

  /**
   * API key authentication middleware
   */
  authenticateAPIKey = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    try {
      if (!this.config.apiKeys.enabled) {
        return res.status(401).json({ error: 'API key authentication is disabled' });
      }

      const apiKey = req.headers[this.config.apiKeys.headerName.toLowerCase()] as string || 
                      req.query[this.config.apiKeys.queryParam] as string;

      if (!apiKey) {
        return res.status(401).json({ error: 'No API key provided' });
      }

      const result = await this.jwtService.verifyAPIKey(apiKey as string);
      
      if (!result) {
        return res.status(401).json({ error: 'Invalid API key' });
      }

      req.user = result.user;
      req.permissions = result.permissions;
      req.apiKey = apiKey as string;

      next();
    } catch (error) {
      return res.status(401).json({ error: 'API key authentication failed' });
    }
  };

  /**
   * Flexible authentication - accepts JWT or API key
   */
  authenticateAny = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;
    const apiKey = req.headers[this.config.apiKeys.headerName.toLowerCase()] as string || 
                   req.query[this.config.apiKeys.queryParam] as string;

    // Try JWT authentication first
    if (authHeader) {
      try {
        const token = authHeader.replace('Bearer ', '');
        const payload = this.jwtService.verifyToken(token);

        const mockUser: User = {
          id: payload.userId,
          email: payload.email,
          role: payload.role,
          isActive: true,
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        req.user = mockUser;
        req.permissions = payload.permissions;

        return next();
      } catch (error) {
        // JWT failed, try API key
      }
    }

    // Try API key authentication
    if (apiKey && this.config.apiKeys.enabled) {
      try {
        const result = await this.jwtService.verifyAPIKey(apiKey as string);
        
        if (result) {
          req.user = result.user;
          req.permissions = result.permissions;
          req.apiKey = apiKey as string;

          return next();
        }
      } catch (error) {
        // API key failed
      }
    }

    return res.status(401).json({ 
      error: 'Authentication required',
      message: 'Please provide a valid JWT token or API key'
    });
  };

  /**
   * Permission check middleware factory
   */
  requirePermission = (resource: string, action: string) => {
    return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
      if (!req.permissions || !req.user) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      if (!this.jwtService.hasPermission(req.permissions, resource, action)) {
        return res.status(403).json({ 
          error: 'Insufficient permissions',
          required: `${resource}:${action}`,
          message: `You don't have permission to ${action} ${resource}`
        });
      }

      next();
    };
  };

  /**
   * Role check middleware factory
   */
  requireRole = (roles: string | string[]) => {
    const allowedRoles = Array.isArray(roles) ? roles : [roles];

    return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
      if (!req.user) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      if (!allowedRoles.includes(req.user.role)) {
        return res.status(403).json({ 
          error: 'Insufficient role',
          required: allowedRoles,
          current: req.user.role
        });
      }

      next();
    };
  };

  /**
   * Admin check middleware
   */
  requireAdmin = this.requireRole(this.config.rbac.adminRoles);

  /**
   * Optional authentication - doesn't fail if no auth provided
   */
  optionalAuth = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;
    const apiKey = req.headers[this.config.apiKeys.headerName.toLowerCase()] as string || 
                   req.query[this.config.apiKeys.queryParam] as string;

    // Try JWT authentication
    if (authHeader) {
      try {
        const token = authHeader.replace('Bearer ', '');
        const payload = this.jwtService.verifyToken(token);

        const mockUser: User = {
          id: payload.userId,
          email: payload.email,
          role: payload.role,
          isActive: true,
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        req.user = mockUser;
        req.permissions = payload.permissions;
      } catch (error) {
        // JWT failed, continue without auth
      }
    }

    // Try API key authentication
    if (apiKey && this.config.apiKeys.enabled && !req.user) {
      try {
        const result = await this.jwtService.verifyAPIKey(apiKey as string);
        
        if (result) {
          req.user = result.user;
          req.permissions = result.permissions;
          req.apiKey = apiKey as string;
        }
      } catch (error) {
        // API key failed, continue without auth
      }
    }

    next();
  };
}
