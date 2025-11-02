import { z } from 'zod';

/**
 * Domain validation utilities
 */
export const domainSchema = z.string().refine(
  (val) => {
    // Basic domain validation regex
    const domainRegex = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    return domainRegex.test(val) && val.length <= 253;
  },
  { message: "Invalid domain format" }
);

export const scanDepthSchema = z.enum(['basic', 'standard', 'comprehensive']);

export const batchScanSchema = z.object({
  domains: z.array(domainSchema).min(1).max(100),
  options: z.object({
    concurrent: z.number().min(1).max(10).default(3),
    scanDepth: scanDepthSchema.default('standard'),
    includeSubdomains: z.boolean().default(false)
  }).default({})
});

export const scanDomainSchema = z.object({
  domain: domainSchema,
  scanDepth: scanDepthSchema.default('standard'),
  includeSubdomains: z.boolean().default(false)
});

/**
 * Input validation functions
 */
export function isValidDomain(domain: string): boolean {
  try {
    domainSchema.parse(domain);
    return true;
  } catch {
    return false;
  }
}

/**
 * Sanitization utilities
 */
export function sanitizeDomain(domain: string): string {
  return domain.toLowerCase().trim();
}

/**
 * Error handling utilities
 */
export class ValidationError extends Error {
  constructor(message: string, public field?: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export class NetworkError extends Error {
  constructor(message: string, public code?: string) {
    super(message);
    this.name = 'NetworkError';
  }
}

export class RateLimitError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RateLimitError';
  }
}
