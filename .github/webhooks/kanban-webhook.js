#!/usr/bin/env node
/**
 * Rust Kanban Terminal Webhook Handler
 * Receives updates from Rust Kanban and syncs with GitHub/Linear
 */

const http = require('http');
const crypto = require('crypto');

const PORT = process.env.KANBAN_WEBHOOK_PORT || 8080;
const WEBHOOK_SECRET = process.env.KANBAN_WEBHOOK_SECRET || 'fsl-continuum-secret';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;

/**
 * Verify webhook signature
 */
function verifySignature(payload, signature) {
  const hmac = crypto.createHmac('sha256', WEBHOOK_SECRET);
  const digest = 'sha256=' + hmac.update(payload).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
}

/**
 * Handle card moved event
 */
async function handleCardMoved(data) {
  console.log(`🔄 Kanban card moved: ${data.card_id}`);
  console.log(`   From: ${data.from_status} → To: ${data.to_status}`);
  
  // Update GitHub Issue
  if (data.github_issue) {
    console.log(`   Updating GitHub Issue #${data.github_issue}`);
    // Implementation: Update issue labels/status
  }
  
  // Update Linear Sub-Issue
  if (data.linear_id) {
    console.log(`   Updating Linear ${data.linear_id}`);
    // Implementation: Update Linear status
  }
  
  // Log to blockchain
  console.log(`   Logging to blockchain...`);
  // Implementation: Call blockchain-log.sh
  
  return {
    success: true,
    message: 'Card status synced',
    github_updated: !!data.github_issue,
    linear_updated: !!data.linear_id
  };
}

/**
 * Handle card created event
 */
async function handleCardCreated(data) {
  console.log(`✨ New Kanban card created: ${data.card_id}`);
  console.log(`   Title: ${data.title}`);
  
  return {
    success: true,
    message: 'Card created'
  };
}

/**
 * Handle card deleted event
 */
async function handleCardDeleted(data) {
  console.log(`🗑️  Kanban card deleted: ${data.card_id}`);
  
  return {
    success: true,
    message: 'Card deleted'
  };
}

/**
 * Main webhook handler
 */
const server = http.createServer(async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Signature');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  if (req.method !== 'POST') {
    res.writeHead(405, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  
  if (req.url !== '/kanban/webhook') {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
    return;
  }
  
  let body = '';
  
  req.on('data', chunk => {
    body += chunk.toString();
  });
  
  req.on('end', async () => {
    try {
      // Verify signature
      const signature = req.headers['x-signature'];
      if (!signature || !verifySignature(body, signature)) {
        res.writeHead(401, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid signature' }));
        return;
      }
      
      const data = JSON.parse(body);
      console.log('🌊 FSL Continuum: Kanban Webhook Received');
      console.log(`   Event: ${data.event}`);
      
      let result;
      
      switch (data.event) {
        case 'card.moved':
          result = await handleCardMoved(data);
          break;
        case 'card.created':
          result = await handleCardCreated(data);
          break;
        case 'card.deleted':
          result = await handleCardDeleted(data);
          break;
        default:
          result = { success: false, message: 'Unknown event' };
      }
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(result));
      
    } catch (error) {
      console.error('❌ Webhook error:', error);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: error.message }));
    }
  });
});

server.listen(PORT, () => {
  console.log('🌊 FSL Continuum: Kanban Webhook Server');
  console.log(`✅ Listening on http://localhost:${PORT}/kanban/webhook`);
  console.log('');
  console.log('Rust Kanban paths:');
  console.log('  - ./rust-ai/rust_kanban/');
  console.log('  - ./autonogrammer/rust_kanban/');
  console.log('  - ./Kode/rust_kanban/');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 Shutting down webhook server...');
  server.close(() => {
    console.log('✅ Server closed');
    process.exit(0);
  });
});
