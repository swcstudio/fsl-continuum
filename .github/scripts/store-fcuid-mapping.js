#!/usr/bin/env node
/**
 * Store FCUID Mapping
 * 
 * Stores FCUID mappings in continuum-state.json
 * Creates bidirectional indexes for fast lookups
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
    process.exit(1);
  }
}

/**
 * Save continuum state
 */
function saveState(state) {
  try {
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf8');
    console.log('✅ State saved successfully');
  } catch (error) {
    console.error('Error saving state:', error.message);
    process.exit(1);
  }
}

/**
 * Store FCUID mapping
 */
function storeFCUIDMapping(options) {
  const {
    fcuid,
    githubIssue,
    githubPR,
    linearEpic,
    linearIssue,
    kanbanCard,
    polygonTx,
    icpTx,
    entityType,
    status = 'active'
  } = options;
  
  // Validate FCUID
  if (!fcuid || !fcuid.startsWith('FSL-')) {
    console.error('❌ Error: Invalid FCUID format');
    process.exit(1);
  }
  
  console.log(`🔐 Storing FCUID mapping: ${fcuid}`);
  
  // Load state
  const state = loadState();
  
  // Initialize FCUID structures if needed
  if (!state.fcuid_registry) {
    state.fcuid_registry = {};
  }
  if (!state.reverse_index) {
    state.reverse_index = {
      github_issues: {},
      github_prs: {},
      linear_epics: {},
      linear_issues: {},
      kanban_cards: {},
      blockchain_txs: {}
    };
  }
  
  // Create or update FCUID entry
  if (!state.fcuid_registry[fcuid]) {
    state.fcuid_registry[fcuid] = {
      fcuid,
      created_at: new Date().toISOString(),
      entity_type: entityType || 'unknown',
      status: status
    };
  }
  
  const fcuidEntry = state.fcuid_registry[fcuid];
  
  // Update mappings
  if (githubIssue) {
    fcuidEntry.github_issue = parseInt(githubIssue);
    state.reverse_index.github_issues[githubIssue] = fcuid;
    console.log(`   GitHub Issue #${githubIssue} → ${fcuid}`);
  }
  
  if (githubPR) {
    fcuidEntry.github_pr = parseInt(githubPR);
    state.reverse_index.github_prs[githubPR] = fcuid;
    console.log(`   GitHub PR #${githubPR} → ${fcuid}`);
  }
  
  if (linearEpic) {
    fcuidEntry.linear_epic = linearEpic;
    state.reverse_index.linear_epics[linearEpic] = fcuid;
    console.log(`   Linear Epic ${linearEpic} → ${fcuid}`);
  }
  
  if (linearIssue) {
    fcuidEntry.linear_issue = linearIssue;
    state.reverse_index.linear_issues[linearIssue] = fcuid;
    console.log(`   Linear Issue ${linearIssue} → ${fcuid}`);
  }
  
  if (kanbanCard) {
    fcuidEntry.kanban_card = kanbanCard;
    state.reverse_index.kanban_cards[kanbanCard] = fcuid;
    console.log(`   Kanban Card ${kanbanCard} → ${fcuid}`);
  }
  
  // Store blockchain TXs
  if (!fcuidEntry.blockchain_txs) {
    fcuidEntry.blockchain_txs = {};
  }
  
  if (polygonTx) {
    fcuidEntry.blockchain_txs.polygon = polygonTx;
    state.reverse_index.blockchain_txs[polygonTx] = fcuid;
    console.log(`   Polygon TX ${polygonTx} → ${fcuid}`);
  }
  
  if (icpTx) {
    fcuidEntry.blockchain_txs.icp = icpTx;
    state.reverse_index.blockchain_txs[icpTx] = fcuid;
    console.log(`   ICP TX ${icpTx} → ${fcuid}`);
  }
  
  // Update last modified
  fcuidEntry.last_updated = new Date().toISOString();
  
  // Update statistics
  if (!state.fcuid_statistics) {
    state.fcuid_statistics = {
      total_fcuids_generated: 0,
      active_fcuids: 0,
      completed_fcuids: 0
    };
  }
  
  state.fcuid_statistics.total_fcuids_generated = Object.keys(state.fcuid_registry).length;
  state.fcuid_statistics.active_fcuids = Object.values(state.fcuid_registry)
    .filter(e => e.status === 'active').length;
  state.fcuid_statistics.completed_fcuids = Object.values(state.fcuid_registry)
    .filter(e => e.status === 'completed').length;
  
  // Update state version
  state.version = '2.0.0-security';
  state.last_updated = new Date().toISOString();
  
  // Save state
  saveState(state);
  
  // Output summary
  console.log('');
  console.log('📊 FCUID Mapping Summary:');
  console.log(`   FCUID: ${fcuid}`);
  console.log(`   Entity Type: ${fcuidEntry.entity_type}`);
  console.log(`   Status: ${fcuidEntry.status}`);
  console.log(`   Mappings: ${Object.keys(fcuidEntry).filter(k => 
    !['fcuid', 'created_at', 'last_updated', 'entity_type', 'status'].includes(k)
  ).length}`);
  console.log('');
  console.log('✅ FCUID mapping stored successfully');
  
  return fcuidEntry;
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  
  const options = {};
  
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    const value = args[i + 1];
    
    switch (key) {
      case 'fcuid':
        options.fcuid = value;
        break;
      case 'github-issue':
        options.githubIssue = value;
        break;
      case 'github-pr':
        options.githubPR = value;
        break;
      case 'linear-epic':
        options.linearEpic = value;
        break;
      case 'linear-issue':
        options.linearIssue = value;
        break;
      case 'kanban-card':
        options.kanbanCard = value;
        break;
      case 'polygon-tx':
        options.polygonTx = value;
        break;
      case 'icp-tx':
        options.icpTx = value;
        break;
      case 'entity-type':
        options.entityType = value;
        break;
      case 'status':
        options.status = value;
        break;
    }
  }
  
  if (!options.fcuid) {
    console.error('Error: --fcuid is required');
    console.log('Usage:');
    console.log('  store-fcuid-mapping.js --fcuid FCUID [options]');
    console.log('');
    console.log('Options:');
    console.log('  --github-issue NUM      GitHub issue number');
    console.log('  --github-pr NUM         GitHub PR number');
    console.log('  --linear-epic ID        Linear epic ID');
    console.log('  --linear-issue ID       Linear issue ID');
    console.log('  --kanban-card ID        Kanban card ID');
    console.log('  --polygon-tx TX         Polygon transaction hash');
    console.log('  --icp-tx TX             ICP transaction ID');
    console.log('  --entity-type TYPE      Entity type (epic, pr, issue)');
    console.log('  --status STATUS         Status (active, completed)');
    process.exit(1);
  }
  
  storeFCUIDMapping(options);
}

module.exports = { storeFCUIDMapping, loadState, saveState };
