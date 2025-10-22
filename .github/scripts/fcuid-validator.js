#!/usr/bin/env node
/**
 * FCUID Validator
 * 
 * Validates FCUID format and enforces security policies
 * - Rate limiting
 * - Access control
 * - Format validation
 */

const crypto = require('crypto');

class FCUIDValidator {
  constructor() {
    // In-memory rate limit store (in production, use Redis)
    this.rateLimitStore = new Map();
    
    // Configuration
    this.config = {
      rateLimitWindow: 60000, // 60 seconds
      maxLookupsPerWindow: 10,
      maxLookupsPerIP: 100 // per hour
    };
  }
  
  /**
   * Validate FCUID format
   */
  validateFormat(fcuid) {
    if (typeof fcuid !== 'string') {
      return { valid: false, error: 'FCUID must be a string' };
    }
    
    // Standard format: FSL-xxxx-xxxx-xxxx-xxxx
    const standardPattern = /^FSL-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}$/i;
    
    // Short format: FSL-xxxxxxxx
    const shortPattern = /^FSL-[0-9a-f]{8}$/i;
    
    if (standardPattern.test(fcuid)) {
      return { valid: true, format: 'standard' };
    }
    
    if (shortPattern.test(fcuid)) {
      return { valid: true, format: 'short' };
    }
    
    return { valid: false, error: 'Invalid FCUID format' };
  }
  
  /**
   * Check rate limit for requester
   */
  checkRateLimit(requesterId, type = 'lookup') {
    const now = Date.now();
    const key = `${requesterId}:${type}`;
    
    // Get or create rate limit entry
    let entry = this.rateLimitStore.get(key);
    
    if (!entry) {
      entry = {
        count: 0,
        windowStart: now,
        resetAt: now + this.config.rateLimitWindow
      };
      this.rateLimitStore.set(key, entry);
    }
    
    // Check if window has expired
    if (now > entry.resetAt) {
      entry.count = 0;
      entry.windowStart = now;
      entry.resetAt = now + this.config.rateLimitWindow;
    }
    
    // Increment counter
    entry.count++;
    
    // Check if limit exceeded
    if (entry.count > this.config.maxLookupsPerWindow) {
      const remainingTime = Math.ceil((entry.resetAt - now) / 1000);
      
      return {
        allowed: false,
        error: 'Rate limit exceeded',
        retryAfter: remainingTime,
        limit: this.config.maxLookupsPerWindow,
        remaining: 0
      };
    }
    
    return {
      allowed: true,
      limit: this.config.maxLookupsPerWindow,
      remaining: this.config.maxLookupsPerWindow - entry.count,
      resetAt: entry.resetAt
    };
  }
  
  /**
   * Validate access permissions
   */
  validateAccess(fcuid, requester, fcuidData) {
    // Basic access control (expand as needed)
    
    // Public access: Anyone can validate format
    if (!fcuidData) {
      return { allowed: true };
    }
    
    // Check if requester has access to this FCUID
    // In production, implement proper ACL based on:
    // - GitHub org membership
    // - Linear team membership
    // - Project access
    
    // For now, allow all authenticated requests
    if (requester && requester.authenticated) {
      return { allowed: true };
    }
    
    // Deny by default for sensitive data
    return {
      allowed: false,
      error: 'Access denied. Authentication required.'
    };
  }
  
  /**
   * Comprehensive validation
   */
  validate(fcuid, requester = {}) {
    const results = {
      fcuid,
      valid: false,
      errors: [],
      warnings: []
    };
    
    // 1. Format validation
    const formatCheck = this.validateFormat(fcuid);
    if (!formatCheck.valid) {
      results.errors.push(formatCheck.error);
      return results;
    }
    results.format = formatCheck.format;
    
    // 2. Rate limiting
    const requesterId = requester.id || requester.ip || 'anonymous';
    const rateLimit = this.checkRateLimit(requesterId);
    
    results.rateLimit = rateLimit;
    
    if (!rateLimit.allowed) {
      results.errors.push(rateLimit.error);
      return results;
    }
    
    // 3. Security checks
    
    // Check for suspicious patterns
    if (this.isSuspiciousPattern(fcuid)) {
      results.warnings.push('Suspicious pattern detected');
    }
    
    // Check for timing attacks
    if (this.isPotentialTimingAttack(requesterId)) {
      results.warnings.push('Potential timing attack detected');
    }
    
    results.valid = true;
    return results;
  }
  
  /**
   * Detect suspicious patterns
   */
  isSuspiciousPattern(fcuid) {
    // Check for overly simple patterns
    const hex = fcuid.replace(/FSL-/g, '').replace(/-/g, '');
    
    // All zeros
    if (/^0+$/.test(hex)) return true;
    
    // Repeating patterns
    if (/^(.)\1+$/.test(hex)) return true;
    
    // Sequential patterns
    if (/^0123456789abcdef/.test(hex)) return true;
    
    return false;
  }
  
  /**
   * Detect potential timing attacks
   */
  isPotentialTimingAttack(requesterId) {
    // Check for rapid sequential requests
    const recentRequests = this.getRecentRequests(requesterId);
    
    if (recentRequests.length > 5) {
      // Check if requests are coming too fast (< 100ms apart)
      const intervals = [];
      for (let i = 1; i < recentRequests.length; i++) {
        intervals.push(recentRequests[i] - recentRequests[i - 1]);
      }
      
      const avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
      
      // If average interval < 100ms, might be timing attack
      if (avgInterval < 100) {
        return true;
      }
    }
    
    return false;
  }
  
  /**
   * Get recent requests for requester
   */
  getRecentRequests(requesterId) {
    const key = `${requesterId}:requests`;
    const requests = this.rateLimitStore.get(key) || [];
    const now = Date.now();
    
    // Filter to last 10 seconds
    const recent = requests.filter(t => now - t < 10000);
    
    // Add current request
    recent.push(now);
    
    // Store back
    this.rateLimitStore.set(key, recent);
    
    return recent;
  }
  
  /**
   * Generate security report
   */
  generateSecurityReport() {
    const report = {
      timestamp: new Date().toISOString(),
      total_requests: 0,
      unique_requesters: 0,
      rate_limited: 0,
      suspicious_patterns: 0,
      timing_attacks: 0
    };
    
    // Analyze rate limit store
    for (const [key, value] of this.rateLimitStore.entries()) {
      if (key.includes(':lookup')) {
        report.total_requests += value.count;
      }
    }
    
    return report;
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  const validator = new FCUIDValidator();
  
  switch (command) {
    case 'validate':
      const fcuid = args[1];
      const result = validator.validate(fcuid, { id: 'cli', authenticated: true });
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.valid ? 0 : 1);
      break;
      
    case 'check-rate-limit':
      const requesterId = args[1];
      const rateLimit = validator.checkRateLimit(requesterId);
      console.log(JSON.stringify(rateLimit, null, 2));
      break;
      
    case 'report':
      const securityReport = validator.generateSecurityReport();
      console.log(JSON.stringify(securityReport, null, 2));
      break;
      
    default:
      console.error(`Unknown command: ${command}`);
      console.log('Usage:');
      console.log('  fcuid-validator.js validate FCUID');
      console.log('  fcuid-validator.js check-rate-limit REQUESTER_ID');
      console.log('  fcuid-validator.js report');
      process.exit(1);
  }
}

module.exports = FCUIDValidator;
