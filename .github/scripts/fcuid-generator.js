#!/usr/bin/env node
/**
 * FSL Continuum Universal Identifier (FCUID) Generator
 * 
 * Generates cryptographically random, unpredictable identifiers
 * for secure cross-platform tracking
 * 
 * Format: FSL-{4hex}-{4hex}-{4hex}-{4hex}
 * Entropy: 96 bits (collision probability: ~1 in 79 octillion)
 */

const crypto = require('crypto');

class FCUIDGenerator {
  /**
   * Generate FSL Continuum Universal Identifier
   * 
   * @param {Object} options - Generation options
   * @param {boolean} options.timeSortable - Encode timestamp for sorting (default: true)
   * @param {string} options.entityType - Entity type (epic, pr, issue, etc.)
   * @returns {string} FCUID in format FSL-xxxx-xxxx-xxxx-xxxx
   */
  static generate(options = {}) {
    const { timeSortable = true, entityType = 'unknown' } = options;
    
    // Generate 12 bytes (96 bits) of cryptographically secure random data
    const randomBytes = crypto.randomBytes(12);
    
    // Optional: Encode timestamp in first 4 bytes for sortability
    if (timeSortable) {
      const timestamp = Date.now();
      // Write timestamp as big-endian 32-bit integer
      randomBytes.writeUInt32BE(timestamp & 0xFFFFFFFF, 0);
    }
    
    // Convert to hex and format
    const hex = randomBytes.toString('hex');
    const parts = [
      hex.slice(0, 4),
      hex.slice(4, 8),
      hex.slice(8, 12),
      hex.slice(12, 16),
      hex.slice(16, 20),
      hex.slice(20, 24)
    ];
    
    // Format: FSL-xxxx-xxxx-xxxx-xxxx
    const fcuid = `FSL-${parts[0]}-${parts[1]}-${parts[2]}-${parts[3]}`;
    
    return fcuid;
  }
  
  /**
   * Generate short FCUID for resource-constrained platforms
   * Format: FSL-{8hex}
   * 
   * @returns {string} Short FCUID
   */
  static generateShort() {
    const randomBytes = crypto.randomBytes(4); // 32 bits
    return `FSL-${randomBytes.toString('hex')}`;
  }
  
  /**
   * Extract timestamp from FCUID (if time-sortable)
   * 
   * @param {string} fcuid - FCUID to extract timestamp from
   * @returns {number|null} Unix timestamp or null if not encoded
   */
  static extractTimestamp(fcuid) {
    if (!this.isValid(fcuid)) return null;
    
    try {
      // Extract first part (timestamp if encoded)
      const hex = fcuid.replace(/FSL-/g, '').replace(/-/g, '');
      const timestampHex = hex.slice(0, 8);
      const timestamp = parseInt(timestampHex, 16);
      
      // Validate it's a reasonable timestamp (after 2020, before 2100)
      const year2020 = 1577836800000;
      const year2100 = 4102444800000;
      
      if (timestamp > year2020 && timestamp < year2100) {
        return timestamp;
      }
      
      return null;
    } catch (e) {
      return null;
    }
  }
  
  /**
   * Validate FCUID format
   * 
   * @param {string} fcuid - FCUID to validate
   * @returns {boolean} True if valid format
   */
  static isValid(fcuid) {
    if (typeof fcuid !== 'string') return false;
    
    // Standard format: FSL-xxxx-xxxx-xxxx-xxxx
    const standardPattern = /^FSL-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}$/i;
    
    // Short format: FSL-xxxxxxxx
    const shortPattern = /^FSL-[0-9a-f]{8}$/i;
    
    return standardPattern.test(fcuid) || shortPattern.test(fcuid);
  }
  
  /**
   * Extract suffix for blockchain TX correlation
   * 
   * @param {string} fcuid - FCUID to extract suffix from
   * @returns {string} Last 8 hex characters
   */
  static extractSuffix(fcuid) {
    if (!this.isValid(fcuid)) {
      throw new Error('Invalid FCUID format');
    }
    
    // Remove FSL- prefix and dashes
    const hex = fcuid.replace(/FSL-/g, '').replace(/-/g, '');
    
    // Return last 8 characters
    return hex.slice(-8);
  }
  
  /**
   * Find FCUID by suffix (for blockchain TX lookup)
   * 
   * @param {string} suffix - 8-character hex suffix
   * @param {Object} registry - FCUID registry from state
   * @returns {string|null} Matching FCUID or null
   */
  static findBySuffix(suffix, registry) {
    if (!registry) return null;
    
    for (const [fcuid, data] of Object.entries(registry)) {
      try {
        const fcuidSuffix = this.extractSuffix(fcuid);
        if (fcuidSuffix.toLowerCase() === suffix.toLowerCase()) {
          return fcuid;
        }
      } catch (e) {
        continue;
      }
    }
    
    return null;
  }
  
  /**
   * Generate metadata for FCUID
   * 
   * @param {string} fcuid - Generated FCUID
   * @param {Object} context - Context information
   * @returns {Object} FCUID metadata
   */
  static generateMetadata(fcuid, context = {}) {
    const timestamp = this.extractTimestamp(fcuid);
    const suffix = this.extractSuffix(fcuid);
    
    return {
      fcuid,
      created_at: new Date().toISOString(),
      timestamp_encoded: timestamp,
      suffix,
      entity_type: context.entityType || 'unknown',
      github_issue: context.githubIssue || null,
      github_pr: context.githubPR || null,
      linear_epic: context.linearEpic || null,
      linear_issue: context.linearIssue || null,
      kanban_card: context.kanbanCard || null,
      blockchain_txs: {},
      status: 'active',
      metadata: context.metadata || {}
    };
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0] || 'generate';
  
  switch (command) {
    case 'generate':
      const options = {};
      
      // Parse options
      for (let i = 1; i < args.length; i += 2) {
        const key = args[i].replace(/^--/, '');
        const value = args[i + 1];
        
        if (key === 'time-sortable') {
          options.timeSortable = value === 'true';
        } else if (key === 'entity-type') {
          options.entityType = value;
        }
      }
      
      const fcuid = FCUIDGenerator.generate(options);
      console.log(fcuid);
      break;
      
    case 'generate-short':
      console.log(FCUIDGenerator.generateShort());
      break;
      
    case 'validate':
      const fcuidToValidate = args[1];
      const isValid = FCUIDGenerator.isValid(fcuidToValidate);
      console.log(JSON.stringify({ valid: isValid }));
      process.exit(isValid ? 0 : 1);
      break;
      
    case 'extract-timestamp':
      const fcuidForTimestamp = args[1];
      const timestamp = FCUIDGenerator.extractTimestamp(fcuidForTimestamp);
      console.log(JSON.stringify({ timestamp, date: timestamp ? new Date(timestamp).toISOString() : null }));
      break;
      
    case 'extract-suffix':
      const fcuidForSuffix = args[1];
      try {
        const suffix = FCUIDGenerator.extractSuffix(fcuidForSuffix);
        console.log(suffix);
      } catch (e) {
        console.error('Error:', e.message);
        process.exit(1);
      }
      break;
      
    default:
      console.error(`Unknown command: ${command}`);
      console.log('Usage:');
      console.log('  fcuid-generator.js generate [--time-sortable true|false] [--entity-type TYPE]');
      console.log('  fcuid-generator.js generate-short');
      console.log('  fcuid-generator.js validate FCUID');
      console.log('  fcuid-generator.js extract-timestamp FCUID');
      console.log('  fcuid-generator.js extract-suffix FCUID');
      process.exit(1);
  }
}

module.exports = FCUIDGenerator;
