# 🚀 FSL Continuum v2.0 Setup Guide

## Quick Start

**Time to setup:** ~30 minutes  
**Complexity:** Intermediate  
**Prerequisites:** GitHub self-hosted runner, Node.js 18+, Rust (optional for Kanban)

---

## Step 1: Clone FSL Continuum

```bash
# Your project already has .github/ structure
cd /path/to/your/project

# Verify structure
ls -la .github/
```

Expected structure:
```
.github/
├── workflows/
├── fsl-pipelines/
├── ISSUE_TEMPLATE/
├── PULL_REQUEST_TEMPLATE/
├── scripts/
├── actions/
├── webhooks/
├── state/
└── docs/
```

---

## Step 2: Configure Secrets

### GitHub Repository Secrets

Navigate to: **Settings → Secrets and variables → Actions → New repository secret**

Required secrets:

```bash
# Linear Integration
LINEAR_API_KEY=lin_api_xxxxx
LINEAR_TEAM_ID=your-team-id

# Blockchain (Polygon)
POLYGON_RPC_URL=https://rpc-mumbai.maticvigil.com
POLYGON_PRIVATE_KEY=your_private_key
POLYGON_CONTRACT_ADDRESS=0x1234...

# Blockchain (Internet Computer)
ICP_IDENTITY_FILE=/path/to/identity.pem
ICP_CANISTER_ID=rrkah-fqaaa-aaaaa-aaaaq-cai

# Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz

# Kanban
KANBAN_WEBHOOK_SECRET=your-secret-key

# GitHub Token (auto-provided)
GITHUB_TOKEN=ghp_xxxx  # Automatically available
```

---

## Step 3: Install Dependencies

### For Self-Hosted Runner

```bash
# Node.js dependencies (for webhooks and actions)
cd .github/actions/linear-sync
npm install @linear/sdk @actions/core @actions/github

# Blockchain tools
npm install -g @polygon/sdk ethers

# Internet Computer CLI
sh -ci "$(curl -fsSL https://sdk.dfinity.org/install.sh)"
```

---

## Step 4: Deploy Blockchain Contracts

### Polygon Smart Contract

```bash
# Install Hardhat
npm install --save-dev hardhat @nomiclabs/hardhat-ethers ethers

# Create hardhat.config.js
cat > hardhat.config.js << 'EOF'
require("@nomiclabs/hardhat-ethers");

module.exports = {
  solidity: "0.8.0",
  networks: {
    mumbai: {
      url: process.env.POLYGON_RPC_URL,
      accounts: [process.env.POLYGON_PRIVATE_KEY]
    }
  }
};
EOF

# Create deployment script
mkdir -p scripts
cat > scripts/deploy-audit-trail.js << 'EOF'
async function main() {
  const FSLAuditTrail = await ethers.getContractFactory("FSLAuditTrail");
  const contract = await FSLAuditTrail.deploy();
  await contract.deployed();
  console.log("FSLAuditTrail deployed to:", contract.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
EOF

# Deploy
npx hardhat run scripts/deploy-audit-trail.js --network mumbai
```

### Internet Computer Canister

```bash
# Create ICP project
dfx new fsl_audit_canister
cd fsl_audit_canister

# Copy canister code (from BLOCKCHAIN_INTEGRATION.md)
# Build and deploy
dfx build
dfx deploy --network ic

# Save canister ID
echo "Canister ID: $(dfx canister id fsl_audit_canister --network ic)"
```

---

## Step 5: Configure Linear

1. Go to **Linear → Settings → API**
2. Create new API key
3. Copy API key → Add to GitHub Secrets
4. Find your Team ID in Linear URL: `app.linear.app/TEAM_ID/...`

---

## Step 6: Configure Slack

1. Go to **api.slack.com**
2. Create new app
3. Enable **Incoming Webhooks**
4. Add webhook to workspace
5. Copy webhook URL → Add to GitHub Secrets

Create channels:
```
#fsl-builds
#fsl-deploys
#fsl-alerts
#fsl-audits
#fsl-updates
```

---

## Step 7: Setup Rust Kanban (Optional)

```bash
# Kanban is already installed at:
# - ./rust-ai/rust_kanban/
# - ./autonogrammer/rust_kanban/
# - ./Kode/rust_kanban/

# Run Kanban terminal
cd rust-ai/rust_kanban/
cargo run

# In another terminal, start webhook server
node .github/webhooks/kanban-webhook.js
```

---

## Step 8: Initialize Continuum State

```bash
# State file already exists at .github/state/continuum-state.json
# Verify it:
cat .github/state/continuum-state.json

# Update with your details
jq '.fsl_version = "2.0.0" | .initialized_at = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' \
   .github/state/continuum-state.json > tmp.json
mv tmp.json .github/state/continuum-state.json
```

---

## Step 9: Test Integration

### Test 1: Create an Epic

```bash
# Create a new issue with "epic" label
gh issue create \
  --title "[EPIC] Test FSL Continuum" \
  --body "Testing the continuum setup" \
  --label "epic"

# Watch for:
# - Linear Epic creation
# - Blockchain logging
# - Kanban card creation
# - Slack notification
```

### Test 2: Run a Pipeline

```bash
# Trigger the continuum orchestrator
gh workflow run continuum-orchestrator.yml

# Check status
gh run list --limit 1

# View logs
gh run view
```

### Test 3: Verify Blockchain

```bash
# Check state file
cat .github/state/continuum-state.json | jq '.blockchain_ledger'

# Should show non-zero totals if logging worked
```

---

## Step 10: Configure GitHub Mobile

1. Install **GitHub Mobile** app
2. Sign in
3. Go to **Settings → Notifications → Actions**
4. Enable notifications for:
   - Workflow runs
   - Failed builds
   - Security alerts

---

## Verification Checklist

- [ ] All secrets configured
- [ ] Blockchain contracts deployed
- [ ] Linear API key working
- [ ] Slack webhooks configured
- [ ] Kanban terminal running (optional)
- [ ] Continuum orchestrator workflow exists
- [ ] State file initialized
- [ ] Test epic created successfully
- [ ] Blockchain logs visible
- [ ] GitHub Mobile notifications working

---

## Troubleshooting

### "Linear sync failed"
```bash
# Check API key
curl -H "Authorization: YOUR_API_KEY" https://api.linear.app/graphql \
  -d '{"query": "{ viewer { id name } }"}'

# Should return your user info
```

### "Blockchain logging failed"
```bash
# Test Polygon connection
curl -X POST $POLYGON_RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Should return current block number
```

### "Kanban webhook not working"
```bash
# Check webhook server is running
curl http://localhost:8080/kanban/webhook -v

# Should return "Method not allowed" (but connection works)
```

### "State file not updating"
```bash
# Check git config
git config user.name "FSL Continuum Bot"
git config user.email "fsl-continuum@users.noreply.github.com"

# Check permissions
ls -la .github/state/
```

---

## Next Steps

1. **Read the Architecture:** [CONTINUUM_ARCHITECTURE.md](./CONTINUUM_ARCHITECTURE.md)
2. **Explore Blockchain:** [BLOCKCHAIN_INTEGRATION.md](./BLOCKCHAIN_INTEGRATION.md)
3. **Configure Linear:** [LINEAR_INTEGRATION.md](./LINEAR_INTEGRATION.md)
4. **Setup Kanban:** [KANBAN_INTEGRATION.md](./KANBAN_INTEGRATION.md)
5. **Slack Alerts:** [SLACK_INTEGRATION.md](./SLACK_INTEGRATION.md)

---

## Support

- **Slack:** #fsl-help
- **Issues:** Create issue with `help` label
- **Docs:** `.github/docs/`
- **Wiki:** Check repository wiki

---

**🌊 FSL Continuum v2.0 - Ship features infinitely with persistent state!** 🚀
