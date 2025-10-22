#!/usr/bin/env node
/**
 * Lookup FCUID
 * 
 * Look up FCUID by platform ID or reverse lookup
 */

const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, '../state/continuum-state.json');

/**
 * Load continuum state
 */
function loadState() {
  try {
    const data = fs.readFileSync(STATE_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error loading state:', error.message);
    return null;
  }
}

/**
 * Lookup FCUID by GitHub Issue
 */
function lookupByGitHubIssue(issueNumber) {
  const state = loadState();
  if (!state || !state.reverse_index) return null;
  
  const fcuid = state.reverse_index.github_issues[issueNumber];
  if (!fcuid) return null;
  
  return {
    fcuid,
    data: state.fcuid_registry[fcuid]
  };
}

/**
 * Lookup FCUID by GitHub PR
 */
function lookupByGitHubPR(prNumber) {
  const state = loadState();
  if (!state || !state.reverse_index) return null;
  
  const fcuid = state.reverse_index.github_prs[prNumber];
  if (!fcuid) return null;
  
  return {
    fcuid,
    data: state.fcuid_registry[fcuid]
  };
}

/**
 * Lookup FCUID by Linear Epic
 */
function lookupByLinearEpic(epicId) {
  const state = loadState();
  if (!state || !state.reverse_index) return null;
  
  const fcuid = state.reverse_index.linear_epics[epicId];
  if (!fcuid) return null;
  
  return {
    fcuid,
    data: state.fcuid_registry[fcuid]
  };
}

/**
 * Lookup FCUID by Blockchain TX
 */
function lookupByBlockchainTx(txHash) {
  const state = loadState();
  if (!state || !state.reverse_index) return null;
  
  const fcuid = state.reverse_index.blockchain_txs[txHash];
  if (!fcuid) return null;
  
  return {
    fcuid,
    data: state.fcuid_registry[fcuid]
  };
}

/**
 * Reverse lookup - Get all platform IDs for FCUID
 */
function reverseLookup(fcuid) {
  const state = loadState();
  if (!state || !state.fcuid_registry) return null;
  
  const data = state.fcuid_registry[fcuid];
  if (!data) return null;
  
  return {
    fcuid,
    github_issue: data.github_issue || null,
    github_pr: data.github_pr || null,
    linear_epic: data.linear_epic || null,
    linear_issue: data.linear_issue || null,
    kanban_card: data.kanban_card || null,
    blockchain_txs: data.blockchain_txs || {},
    entity_type: data.entity_type,
    status: data.status,
    created_at: data.created_at,
    last_updated: data.last_updated
  };
}

/**
 * List all FCUIDs
 */
function listAll(filters = {}) {
  const state = loadState();
  if (!state || !state.fcuid_registry) return [];
  
  let fcuids = Object.values(state.fcuid_registry);
  
  // Apply filters
  if (filters.entityType) {
    fcuids = fcuids.filter(f => f.entity_type === filters.entityType);
  }
  
  if (filters.status) {
    fcuids = fcuids.filter(f => f.status === filters.status);
  }
  
  // Sort by created_at (newest first)
  fcuids.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  
  return fcuids;
}

/**
 * Get FCUID statistics
 */
function getStatistics() {
  const state = loadState();
  if (!state) return null;
  
  const fcuids = Object.values(state.fcuid_registry || {});
  
  return {
    total: fcuids.length,
    active: fcuids.filter(f => f.status === 'active').length,
    completed: fcuids.filter(f => f.status === 'completed').length,
    by_type: {
      epic: fcuids.filter(f => f.entity_type === 'epic').length,
      pr: fcuids.filter(f => f.entity_type === 'pr').length,
      issue: fcuids.filter(f => f.entity_type === 'issue').length
    },
    with_blockchain: fcuids.filter(f => f.blockchain_txs && 
      (f.blockchain_txs.polygon || f.blockchain_txs.icp)).length
  };
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const value = args[1];
  
  let result;
  
  switch (command) {
    case 'github-issue':
      result = lookupByGitHubIssue(value);
      break;
      
    case 'github-pr':
      result = lookupByGitHubPR(value);
      break;
      
    case 'linear-epic':
      result = lookupByLinearEpic(value);
      break;
      
    case 'blockchain-tx':
      result = lookupByBlockchainTx(value);
      break;
      
    case 'reverse':
      result = reverseLookup(value);
      break;
      
    case 'list':
      const filters = {};
      for (let i = 1; i < args.length; i += 2) {
        const key = args[i].replace(/^--/, '');
        const val = args[i + 1];
        
        if (key === 'entity-type') filters.entityType = val;
        if (key === 'status') filters.status = val;
      }
      result = listAll(filters);
      break;
      
    case 'stats':
      result = getStatistics();
      break;
      
    default:
      console.error(`Unknown command: ${command}`);
      console.log('Usage:');
      console.log('  lookup-fcuid.js github-issue NUMBER');
      console.log('  lookup-fcuid.js github-pr NUMBER');
      console.log('  lookup-fcuid.js linear-epic ID');
      console.log('  lookup-fcuid.js blockchain-tx TX_HASH');
      console.log('  lookup-fcuid.js reverse FCUID');
      console.log('  lookup-fcuid.js list [--entity-type TYPE] [--status STATUS]');
      console.log('  lookup-fcuid.js stats');
      process.exit(1);
  }
  
  if (result) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log('No results found');
    process.exit(1);
  }
}

module.exports = {
  lookupByGitHubIssue,
  lookupByGitHubPR,
  lookupByLinearEpic,
  lookupByBlockchainTx,
  reverseLookup,
  listAll,
  getStatistics
};
