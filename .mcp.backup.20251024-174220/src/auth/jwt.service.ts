/**
 * JWT authentication service for enterprise ZeroServe MCP Server
 */

import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { getAuthConfig, UserRole, defaultRoles } from '../config/auth';

export interface JWTPayload {
  userId: string;
  email: string;
  role: string;
  permissions: string[];
  iat?: number;
  exp?: number;
  iss?: string;
  aud?: string;
}

export interface User {
  id: string;
  email: string;
  password?: string;
  role: string;
  isActive: boolean;
  lastLogin?: Date;
  createdAt: Date;
  updatedAt: Date;
  apiKeys?: APIKey[];
}

export interface APIKey {
  id: string;
  name: string;
  key: string;
  userId: string;
  permissions: string[];
  isActive: boolean;
  expiresAt?: Date;
  createdAt: Date;
  lastUsed?: Date;
}

export class JWTService {
  private config = getAuthConfig();

  /**
   * Generate JWT token for user
   */
  generateToken(user: User): string {
    const role = defaultRoles.find(r => r.id === user.role) || defaultRoles.find(r => r.id === 'viewer')!;
    const permissions = role.permissions.map(p => `${p.resource}:${p.action}`);

    const payload: JWTPayload = {
      userId: user.id,
      email: user.email,
      role: user.role,
      permissions,
    };

    return jwt.sign(payload, this.config.jwt.secret, {
      expiresIn: this.config.jwt.expiresIn,
      issuer: this.config.jwt.issuer,
      audience: this.config.jwt.audience,
    } as jwt.SignOptions);
  }

  /**
   * Verify JWT token
   */
  verifyToken(token: string): JWTPayload {
    try {
      return jwt.verify(token, this.config.jwt.secret, {
        issuer: this.config.jwt.issuer,
        audience: this.config.jwt.audience,
      } as jwt.VerifyOptions) as JWTPayload;
    } catch (error) {
      throw new Error('Invalid or expired token');
    }
  }

  /**
   * Generate API key
   */
  generateAPIKey(userId: string, name: string, permissions: string[]): string {
    const apiKey = `zs_${this.generateRandomString(32)}`;
    const hashedKey = bcrypt.hashSync(apiKey, 10);

    // Store API key in database
    // This is a placeholder - in production, store in your database
    console.log(`Generated API key for user ${userId}: ${apiKey}`);
    
    return apiKey;
  }

  /**
   * Verify API key
   */
  async verifyAPIKey(apiKey: string): Promise<{ user: User; permissions: string[] } | null> {
    if (!apiKey.startsWith('zs_')) {
      return null;
    }

    // In production, verify against database
    // For now, return a mock user
    const mockUser: User = {
      id: 'api-user',
      email: 'api@zeroserve.com',
      role: 'analyst',
      isActive: true,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    const role = defaultRoles.find(r => r.id === mockUser.role)!;
    const permissions = role.permissions.map(p => `${p.resource}:${p.action}`);

    return {
      user: mockUser,
      permissions,
    };
  }

  /**
   * Hash password
   */
  async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 10);
  }

  /**
   * Verify password
   */
  async verifyPassword(password: string, hashedPassword: string): Promise<boolean> {
    return bcrypt.compare(password, hashedPassword);
  }

  /**
   * Check if user has permission
   */
  hasPermission(userPermissions: string[], resource: string, action: string): boolean {
    // Check for wildcard permission
    if (userPermissions.includes('*:*')) {
      return true;
    }

    // Check for specific permission
    const permission = `${resource}:${action}`;
    if (userPermissions.includes(permission)) {
      return true;
    }

    // Check for resource wildcard
    const resourceWildcard = `${resource}:*`;
    if (userPermissions.includes(resourceWildcard)) {
      return true;
    }

    // Check for action wildcard
    const actionWildcard = `*:${action}`;
    if (userPermissions.includes(actionWildcard)) {
      return true;
    }

    return false;
  }

  /**
   * Get user role with rate limits
   */
  getUserRole(roleId: string): UserRole | null {
    return defaultRoles.find(r => r.id === roleId) || null;
  }

  /**
   * Generate random string for API keys
   */
  private generateRandomString(length: number): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  /**
   * Refresh token
   */
  refreshToken(refreshToken: string): string {
    try {
      const decoded = jwt.verify(refreshToken, this.config.jwt.secret + '_refresh') as any;
      const mockUser: User = {
        id: decoded.userId,
        email: decoded.email,
        role: decoded.role,
        isActive: true,
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      return this.generateToken(mockUser);
    } catch (error) {
      throw new Error('Invalid refresh token');
    }
  }

  /**
   * Generate refresh token
   */
  generateRefreshToken(user: User): string {
    const payload = {
      userId: user.id,
      email: user.email,
      role: user.role,
      type: 'refresh',
    };

    return jwt.sign(payload, this.config.jwt.secret + '_refresh', {
      expiresIn: '7d',
      issuer: this.config.jwt.issuer,
      audience: this.config.jwt.audience,
    } as jwt.SignOptions);
  }
}
