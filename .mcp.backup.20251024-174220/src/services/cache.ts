import { DomainScanResult, CachedResult } from '../types';

/**
 * Simple in-memory cache with TTL support
 */
export class ScanCache {
  private cache = new Map<string, CachedResult>();
  private defaultTTL: number;

  constructor(defaultTTL: number = 5 * 60 * 1000) { // 5 minutes default
    this.defaultTTL = defaultTTL;
  }

  /**
   * Get cached result if not expired
   */
  get(domain: string): DomainScanResult | null {
    const cached = this.cache.get(domain);
    if (!cached) {
      return null;
    }

    if (this.isExpired(cached)) {
      this.cache.delete(domain);
      return null;
    }

    return cached.data;
  }

  /**
   * Store result in cache
   */
  set(domain: string, result: DomainScanResult, customTTL?: number): void {
    this.cache.set(domain, {
      data: result,
      timestamp: Date.now()
    });

    // Auto-expire after custom TTL
    const ttl = customTTL || this.defaultTTL;
    setTimeout(() => {
      this.cache.delete(domain);
    }, ttl);
  }

  /**
   * Check if cached result is expired
   */
  private isExpired(cached: CachedResult, ttl?: number): boolean {
    const maxAge = ttl || this.defaultTTL;
    return (Date.now() - cached.timestamp) > maxAge;
  }

  /**
   * Clear cache
   */
  clear(): void {
    this.cache.clear();
  }

  /**
   * Get cache statistics
   */
  getStats(): { size: number; keys: string[] } {
    return {
      size: this.cache.size,
      keys: Array.from(this.cache.keys())
    };
  }

  /**
   * Delete specific entry
   */
  delete(domain: string): boolean {
    return this.cache.delete(domain);
  }

  /**
   * Check if domain exists in cache
   */
  has(domain: string): boolean {
    const cached = this.cache.get(domain);
    if (!cached) {
      return false;
    }
    
    if (this.isExpired(cached)) {
      this.cache.delete(domain);
      return false;
    }
    
    return true;
  }
}
