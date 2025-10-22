# 🔗 Blockchain Integration Guide

## Overview

FSL Continuum uses **dual-chain blockchain logging** to create a tamper-proof audit trail. Every pipeline run is logged to both Polygon and Internet Computer (ICP), making it virtually impossible to alter historical records.

## Why Dual-Chain?

1. **Tamper-Proof**: Requires compromising TWO independent blockchains simultaneously
2. **Redundancy**: If one chain has issues, the other maintains records
3. **Verification**: Cross-chain comparison detects any tampering attempts
4. **Cost-Effective**: Polygon for cheap storage (~$0.0001/tx), ICP for permanent storage (negligible cost)

## Setup

### 1. Polygon Configuration

**Network:** Mumbai Testnet (for testing), Polygon Mainnet (for production)

**Required:**
- Polygon wallet with MATIC tokens
- Private key for signing transactions
- RPC endpoint

**Environment Variables:**
```bash
POLYGON_RPC_URL=https://rpc-mumbai.maticvigil.com
POLYGON_PRIVATE_KEY=your_private_key_here
POLYGON_CONTRACT_ADDRESS=0x1234567890abcdef...
```

**Smart Contract:**
```solidity
// FSLAuditTrail.sol
pragma solidity ^0.8.0;

contract FSLAuditTrail {
    struct PipelineRun {
        uint256 timestamp;
        bytes32 logHash;
        string pipelineId;
        string githubRepo;
        string status;
    }
    
    mapping(bytes32 => PipelineRun) public auditTrail;
    
    event PipelineLogged(
        bytes32 indexed logHash,
        string pipelineId,
        uint256 timestamp
    );
    
    function logPipeline(
        bytes32 _logHash,
        string memory _pipelineId,
        string memory _githubRepo,
        string memory _status
    ) public {
        auditTrail[_logHash] = PipelineRun({
            timestamp: block.timestamp,
            logHash: _logHash,
            pipelineId: _pipelineId,
            githubRepo: _githubRepo,
            status: _status
        });
        
        emit PipelineLogged(_logHash, _pipelineId, block.timestamp);
    }
    
    function verifyLog(bytes32 _logHash) public view returns (bool, PipelineRun memory) {
        PipelineRun memory run = auditTrail[_logHash];
        return (run.timestamp != 0, run);
    }
}
```

### 2. Internet Computer Configuration

**Network:** IC Mainnet

**Required:**
- DFX identity
- Cycles for canister calls
- Canister ID

**Environment Variables:**
```bash
ICP_IDENTITY_FILE=~/.config/dfx/identity/default/identity.pem
ICP_CANISTER_ID=rrkah-fqaaa-aaaaa-aaaaq-cai
ICP_NETWORK=ic
```

**Canister Code:**
```rust
// src/fsl_audit/lib.rs
use ic_cdk::export::candid::{CandidType, Deserialize};
use ic_cdk_macros::*;
use std::collections::HashMap;

#[derive(Clone, CandidType, Deserialize)]
struct PipelineLog {
    timestamp: u64,
    log_hash: String,
    pipeline_id: String,
    github_repo: String,
    status: String,
}

thread_local! {
    static AUDIT_TRAIL: std::cell::RefCell<HashMap<String, PipelineLog>> = 
        std::cell::RefCell::new(HashMap::new());
}

#[update]
fn log_pipeline(log: PipelineLog) -> String {
    let log_hash = log.log_hash.clone();
    AUDIT_TRAIL.with(|trail| {
        trail.borrow_mut().insert(log_hash.clone(), log);
    });
    log_hash
}

#[query]
fn verify_log(log_hash: String) -> Option<PipelineLog> {
    AUDIT_TRAIL.with(|trail| {
        trail.borrow().get(&log_hash).cloned()
    })
}

#[query]
fn get_total_logs() -> u64 {
    AUDIT_TRAIL.with(|trail| {
        trail.borrow().len() as u64
    })
}
```

## Usage

### Logging a Pipeline Run

```bash
# Create log data
LOG_DATA='{
  "event": "workflow_run",
  "repo": "owner/repo",
  "run_id": "1234567890",
  "status": "success",
  "timestamp": "2025-01-21T23:00:00Z"
}'

# Log to both chains
./github/scripts/blockchain-log.sh both "$LOG_DATA"
```

**Output:**
```json
{
  "log_hash": "a1b2c3d4e5f6...",
  "polygon_tx": "0x123456789abcdef...",
  "icp_tx": "ic://abcdef123456...",
  "timestamp": "2025-01-21T23:00:00Z",
  "verified": true
}
```

### Verifying Logs

```bash
# Verify a specific log
./github/scripts/verify-blockchain.sh <polygon_tx> <icp_tx>
```

## Integration with GitHub Actions

```yaml
- name: Log to Blockchain
  id: blockchain
  run: |
    LOG_DATA=$(cat << EOF
    {
      "event": "${{ github.event_name }}",
      "repo": "${{ github.repository }}",
      "run_id": "${{ github.run_id }}",
      "status": "${{ job.status }}"
    }
    EOF
    )
    
    RESULT=$(./.github/scripts/blockchain-log.sh both "$LOG_DATA")
    echo "result=$RESULT" >> $GITHUB_OUTPUT

- name: Comment on PR
  uses: actions/github-script@v6
  with:
    script: |
      const result = JSON.parse('${{ steps.blockchain.outputs.result }}');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `## Blockchain Audit Trail\n\n` +
              `- Polygon: ${result.polygon_tx}\n` +
              `- ICP: ${result.icp_tx}\n` +
              `- Hash: ${result.log_hash}`
      });
```

## Cost Analysis

### Polygon (Mumbai Testnet)
- **Transaction Fee:** ~0.001 MATIC (~$0.0001 USD)
- **100 runs/day:** $0.01/day = $3.65/year
- **Contract Deployment:** One-time ~$0.50

### Internet Computer
- **Cycles Cost:** ~1M cycles per call (~$0.00001 USD)
- **100 runs/day:** Negligible
- **Canister Creation:** One-time ~$1.00

**Total Annual Cost: ~$5/year** 🎉

## Verification & Integrity

### Automatic Verification

FSL Continuum performs hourly integrity checks:

```bash
# Runs every hour
0 * * * * /path/to/.github/scripts/verify-all-logs.sh
```

### Manual Verification

```bash
# Verify specific log
./github/scripts/verify-blockchain.sh \
  0x123... \  # Polygon TX
  ic://456... # ICP TX

# Verify all logs from last 24h
./github/scripts/verify-blockchain.sh --last-24h

# Verify entire history
./github/scripts/verify-blockchain.sh --all
```

### Tampering Detection

If a mismatch is detected:

1. **Alert:** Immediate Slack notification to #fsl-alerts
2. **Lock:** Repository locked for investigation
3. **Notification:** GitHub Mobile push notification
4. **Email:** Security team notified
5. **Incident:** Automatic incident created in Linear

## Best Practices

1. **Always log to both chains** - Never skip dual logging
2. **Store TX hashes in multiple places** - GitHub comments, Linear, Kanban
3. **Regular verification** - Hourly automated checks
4. **Backup keys securely** - Use GitHub Secrets, never commit
5. **Monitor costs** - Set up alerts for unusual activity
6. **Test on testnets first** - Mumbai for Polygon, local replica for ICP

## Troubleshooting

### Polygon Transaction Fails

```bash
# Check balance
cast balance $YOUR_ADDRESS --rpc-url $POLYGON_RPC_URL

# Check gas price
cast gas-price --rpc-url $POLYGON_RPC_URL

# Increase gas limit in script
```

### ICP Canister Call Fails

```bash
# Check cycles balance
dfx canister status $CANISTER_ID --network ic

# Add cycles
dfx canister deposit-cycles 1000000000000 $CANISTER_ID --network ic

# Check identity
dfx identity whoami
```

### Verification Mismatch

```bash
# This is CRITICAL - investigate immediately
# 1. Check both transactions exist
# 2. Compare data on both chains
# 3. Verify no one has access to private keys
# 4. Review recent commits to state files
# 5. Contact security team
```

## Security Considerations

1. **Private Keys:** Never commit, use GitHub Secrets only
2. **Canister IDs:** Can be public, but protect identity files
3. **RPC Endpoints:** Use rate-limited endpoints or run your own node
4. **State Files:** Sign commits with GPG keys
5. **Audit Access:** Limit who can deploy/update contracts

## Support

For blockchain integration issues:
- Check logs in `.github/logs/blockchain/`
- View transactions on explorers
- Contact #fsl-blockchain on Slack
- Review [Polygon Docs](https://docs.polygon.technology/)
- Review [ICP Docs](https://internetcomputer.org/docs)

---

**🔗 FSL Continuum: Tamper-proof audit trail via dual-chain blockchain logging**
