# 🗺️ FSL Continuum Migration Guide

> **SPEC:000** | Complete upgrade guide for FSL Continuum v2.1

This guide helps you update references after the SPEC:000 migration from `github-actions/` to `.github/` with FSL Continuum branding.

---

## 📋 Quick Reference

### Migration Status

✅ **All 5 phases complete!**
- Phase 1: Core Workflows (13 files)
- Phase 2: Tools & Scripts (33 files)
- Phase 3: Documentation (18 files)
- Phase 4: Integrations (8 systems)
- Phase 5: Cleanup & Validation

**Total:** 75+ files migrated | January 22, 2025

---

## 🔄 Workflow Name Changes

All workflows renamed from `flow-state-*` to `fsl-*`:

| Old Name | New Name | Purpose |
|----------|----------|---------|
| `flow-state-orchestrator.yml` | `fsl-orchestrator.yml` | Master coordinator |
| `flow-state-initiation.yml` | `fsl-initiation.yml` | Epic creation from issues |
| `flow-state-decomposition.yml` | `fsl-decomposition.yml` | AI task decomposition |
| `flow-state-execution.yml` | `fsl-execution.yml` | Code generation |
| `flow-state-merger.yml` | `fsl-merger.yml` | PR automation |
| `flow-state-security-validation.yml` | `fsl-security.yml` | Multi-market security |
| `flow-state-self-healing.yml` | `fsl-self-healing.yml` | Autonomous healing |
| `flow-state-predictive-intelligence.yml` | `fsl-predictive-ai.yml` | ML predictions |
| `flow-state-web3-dao.yml` | `fsl-web3-dao.yml` | DAO governance |
| `ai-enhanced-pr-review.yml` | `fsl-ai-pr-review.yml` | AI code review |
| `copilot-enhanced-pr-review.yml` | `fsl-copilot-review.yml` | Copilot integration |
| `spec-driven-development.yml` | `fsl-spec-driven.yml` | SPEC→code |
| `spec-driven-copilot.yml` | `fsl-spec-copilot.yml` | SPEC+Copilot |

**Plus:** Merged `continuum-orchestrator.yml` functionality into `fsl-orchestrator.yml`

---

## 📦 Tool Relocations

Tools moved from flat structure to 14 organized categories:

### AI Category

| Old Path | New Path |
|----------|----------|
| `tools/ai-code-reviewer.py` | `fsl-pipelines/ai/code-reviewer.py` |
| `tools/ai-test-generator.py` | `fsl-pipelines/ai/test-generator.py` |
| `tools/explainable-ai.py` | `fsl-pipelines/ai/explainable-ai.py` |
| `tools/multi-model-ensemble.py` | `fsl-pipelines/ai/ensemble.py` |

### Machine Learning Category

| Old Path | New Path |
|----------|----------|
| `tools/ml-predictor.py` | `fsl-pipelines/ml/predictor.py` |
| `tools/model-trainer.py` | `fsl-pipelines/ml/trainer.py` |
| `tools/distributed-ml-trainer.py` | `fsl-pipelines/ml/distributed-trainer.py` |
| `tools/feature-extractor.py` | `fsl-pipelines/ml/feature-extractor.py` |

### Security Category

| Old Path | New Path |
|----------|----------|
| `tools/security-compliance-scanner.py` | `fsl-pipelines/security/compliance-scanner.py` |

### Monitoring Category

| Old Path | New Path |
|----------|----------|
| `tools/health-monitor.py` | `fsl-pipelines/monitoring/health-monitor.py` |
| `tools/observability-suite.py` | `fsl-pipelines/monitoring/observability.py` |

### Optimization Category

| Old Path | New Path |
|----------|----------|
| `tools/cost-optimizer.py` | `fsl-pipelines/optimization/cost-optimizer.py` |
| `tools/performance-optimizer.py` | `fsl-pipelines/optimization/performance.py` |

### Analytics Category

| Old Path | New Path |
|----------|----------|
| `tools/analytics-dashboard.py` | `fsl-pipelines/analytics/analytics-dashboard.py` |
| `tools/dx-analytics.py` | `fsl-pipelines/analytics/dx-metrics.py` |

### Other Categories

**Deployment:**
- `tools/progressive-deployer.py` → `fsl-pipelines/deployment/progressive-deployer.py`

**Testing:**
- `tools/genetic-test-generator.py` → `fsl-pipelines/testing/genetic-generator.py`

**Documentation:**
- `tools/auto-doc-generator.py` → `fsl-pipelines/docs/auto-generator.py`
- `tools/spec-doc-generator.py` → `fsl-pipelines/docs/spec-generator.py`

**Collaboration:**
- `tools/realtime-collaboration.py` → `fsl-pipelines/collaboration/realtime-sync.py`

**Enterprise:**
- `tools/enterprise-integration-hub.py` → `fsl-pipelines/enterprise/integration-hub.py`

**Knowledge:**
- `tools/knowledge-graph-builder.py` → `fsl-pipelines/knowledge/graph-builder.py`

**Self-Healing:**
- `tools/healing-actions.py` → `fsl-pipelines/self-healing/healing-actions.py`

**Web3:**
- `tools/dao-governance.py` → `fsl-pipelines/web3/dao-governance.py`

---

## 📜 Script Relocations

Scripts organized by purpose:

### Setup Scripts

| Old Path | New Path |
|----------|----------|
| `install-github-actions.sh` | `scripts/setup/install-actions.sh` |
| `setup-globals.sh` | `scripts/setup/setup-globals.sh` |
| `install-deps.sh` | `scripts/setup/install-deps.sh` |
| `setup-greptile.sh` | `scripts/setup/setup-greptile.sh` |

### Deployment Scripts

| Old Path | New Path |
|----------|----------|
| `clean-deploy-script-v2.py` | `scripts/deployment/clean-deploy-v2.py` |
| `deploy-to-prod.sh` | `scripts/deployment/deploy-to-prod.sh` |
| `rollback.sh` | `scripts/deployment/rollback.sh` |

### OpenSpec Scripts

| Old Path | New Path |
|----------|----------|
| `setup-openspec.py` | `scripts/openspec/setup-commands.py` |

### Root Scripts

| Old Path | New Path |
|----------|----------|
| `tools/flow-state-init.sh` | `scripts/fsl-init.sh` |
| `tools/context-analyzer.sh` | `scripts/context-analyzer.sh` |
| `blockchain-log.sh` | `scripts/blockchain-log.sh` |

---

## 📚 Documentation Reorganization

Documentation organized into 4 categories:

### History Category

- `docs/history/` - Historical documents and architecture evolution

### Integrations Category

| Old Path | New Path |
|----------|----------|
| `docs/FOUR_MARKETS.md` | `docs/integrations/FOUR_MARKETS.md` |
| `docs/JAPANESE_ENGINEERING.md` | `docs/integrations/JAPANESE_ENGINEERING.md` |
| `docs/COPILOT_SETUP.md` | `docs/integrations/COPILOT_SETUP.md` |

### Setup Category

| Old Path | New Path |
|----------|----------|
| `SETUP.md` | `docs/setup/SETUP.md` |
| `INSTALLATION.md` | `docs/setup/INSTALLATION.md` |

### OpenSpec Category

- `docs/openspec/SPEC_SYSTEM.md` - **NEW** - Complete SPEC versioning guide
- `docs/openspec/AGENTS.md` - Agent configuration
- `docs/openspec/PROJECT.md` - Project structure

**Plus:** Created `docs/README.md` (35KB) - Complete documentation index

---

## 🔌 Integration Changes

### Actions Directory

**Removed empty placeholders:**
- `actions/slack-notify/` - Empty (use GitHub Slack app)
- `actions/blockchain-audit/` - Empty (script sufficient)
- `actions/kanban-update/` - Empty (webhook sufficient)

**Kept functional:**
- `actions/linear-sync/` - ✅ Complete Linear.app integration

### Webhooks

- `webhooks/kanban-webhook.js` - ✅ Real-time Kanban sync

### Scripts

- `scripts/blockchain-log.sh` - ✅ FCUID-enhanced blockchain logging

---

## ⚠️ Breaking Changes

### 1. Workflow References

If you reference workflows externally:

```yaml
# OLD
workflow_run:
  workflows: ["flow-state-initiation"]
  
# NEW
workflow_run:
  workflows: ["fsl-initiation"]
```

### 2. Tool Import Paths

If you import or call tools:

```bash
# OLD
python3 github-actions/tools/ai-code-reviewer.py

# NEW
python3 .github/fsl-pipelines/ai/code-reviewer.py
```

### 3. Script Paths

If you call scripts:

```bash
# OLD
bash github-actions/setup-globals.sh

# NEW
bash .github/scripts/setup/setup-globals.sh
```

### 4. Documentation Links

If you link to documentation:

```markdown
# OLD
[Setup Guide](github-actions/docs/SETUP.md)

# NEW
[Setup Guide](.github/docs/setup/SETUP.md)
```

### 5. Branding Terminology

| Old Term | New Term | Reason |
|----------|----------|--------|
| "Flow State Loop" | "FSL Continuum" | Emphasizes persistent state |
| "pipeline" | "continuum" | Never resets, accumulates state |
| "flow-state-*" | "fsl-*" | Consistent branding |

---

## 🚀 Upgrade Instructions

### For External References

#### Step 1: Update Workflow Triggers

If you have external workflows that depend on FSL Continuum:

```yaml
# Update workflow names
on:
  workflow_run:
    workflows: 
      - "fsl-initiation"        # Was: flow-state-initiation
      - "fsl-execution"         # Was: flow-state-execution
      - "fsl-merger"            # Was: flow-state-merger
```

#### Step 2: Update Tool Paths

Update any scripts or workflows that call tools:

```yaml
# In GitHub Actions workflows
- name: Run Code Review
  run: python3 .github/fsl-pipelines/ai/code-reviewer.py
  
# In shell scripts
python3 "${REPO_ROOT}/.github/fsl-pipelines/ml/predictor.py"
```

#### Step 3: Update Documentation Links

```markdown
# Update README and docs
- [Workflow Documentation](./.github/workflows/README.md)
- [Tool Documentation](./.github/fsl-pipelines/README.md)
- [Setup Guide](./.github/docs/setup/SETUP.md)
```

#### Step 4: Update Configuration Files

```yaml
# config files (e.g., .factory/commands/)
tools_directory: ".github/fsl-pipelines"
scripts_directory: ".github/scripts"
workflows_directory: ".github/workflows"
```

### For Internal Migration

**Nothing to do!** All internal references were updated in Phases 1-4:
- ✅ All workflow cross-references updated
- ✅ All tool import paths updated
- ✅ All script paths updated
- ✅ All documentation links updated

---

## 📋 Complete Migration Map

### Workflows (13 files + 1 merged)

| # | Old | New | Status |
|---|-----|-----|--------|
| 1 | flow-state-orchestrator.yml | fsl-orchestrator.yml | ✅ Merged |
| 2 | flow-state-initiation.yml | fsl-initiation.yml | ✅ Migrated |
| 3 | flow-state-decomposition.yml | fsl-decomposition.yml | ✅ Migrated |
| 4 | flow-state-execution.yml | fsl-execution.yml | ✅ Migrated |
| 5 | flow-state-merger.yml | fsl-merger.yml | ✅ Migrated |
| 6 | flow-state-security-validation.yml | fsl-security.yml | ✅ Migrated |
| 7 | flow-state-self-healing.yml | fsl-self-healing.yml | ✅ Migrated |
| 8 | flow-state-predictive-intelligence.yml | fsl-predictive-ai.yml | ✅ Migrated |
| 9 | flow-state-web3-dao.yml | fsl-web3-dao.yml | ✅ Migrated |
| 10 | ai-enhanced-pr-review.yml | fsl-ai-pr-review.yml | ✅ Migrated |
| 11 | copilot-enhanced-pr-review.yml | fsl-copilot-review.yml | ✅ Migrated |
| 12 | spec-driven-development.yml | fsl-spec-driven.yml | ✅ Migrated |
| 13 | spec-driven-copilot.yml | fsl-spec-copilot.yml | ✅ Migrated |
| - | continuum-orchestrator.yml | → fsl-orchestrator.yml | ✅ Merged |

### Tools (23 files organized)

All tools relocated to categorized structure in `fsl-pipelines/[category]/`

### Scripts (10+ files organized)

All scripts organized in `scripts/[category]/`

### Documentation (15 migrated + 3 created)

All docs organized in `docs/[category]/`

---

## 🔄 Rollback Procedure

If you need to rollback to the old structure:

### Restore Archive

```bash
# Navigate to archives
cd ~/fsl-archives/

# List available archives
ls -lh github-actions-archive-*.tar.gz

# Restore (replace TIMESTAMP with actual)
tar -xzf github-actions-archive-20251022-123025.tar.gz -C /home/ubuntu/src/repos/

# Verify restoration
cd /home/ubuntu/src/repos/github-actions/
ls -la
```

### Revert Workflow Names

```bash
# In your workflows, revert names back to:
# fsl-* → flow-state-*
```

### Revert Tool Paths

```bash
# Update paths back to:
# .github/fsl-pipelines/ → github-actions/tools/
```

### Important Notes

⚠️ **Rollback not recommended!** The new structure:
- Better organization (14 categories)
- Cleaner branding (FSL Continuum)
- Better documentation (indexed)
- Persistent state (continuum vs pipeline)
- Production-ready

---

## 🎯 Migration Checklist

Use this checklist if you have external dependencies:

### External Workflow Dependencies
- [ ] Update workflow_run references to fsl-* names
- [ ] Update workflow dispatch calls
- [ ] Update status check names
- [ ] Test workflow triggers

### External Tool/Script Dependencies
- [ ] Update tool import paths to fsl-pipelines/[category]/
- [ ] Update script paths to scripts/[category]/
- [ ] Update configuration files
- [ ] Test tool execution

### Documentation Dependencies
- [ ] Update documentation links to new paths
- [ ] Update README references
- [ ] Update API documentation
- [ ] Update developer guides

### Integration Dependencies
- [ ] Update webhook URLs (if applicable)
- [ ] Update API endpoints (if applicable)
- [ ] Update environment variables
- [ ] Update secret names

### Testing
- [ ] Run complete workflow test
- [ ] Verify all tools accessible
- [ ] Verify all scripts executable
- [ ] Verify all documentation links work
- [ ] Verify integrations functional

---

## 📖 Additional Resources

### Migration Documentation

- [TODO.md](../TODO.md) - Complete phase-by-phase checklist
- [SPEC-000-MIGRATION.md](../SPEC-000-MIGRATION.md) - Technical specification
- [CHANGELOG.md](../CHANGELOG.md) - SPEC versioning history
- [SPEC-000-COMPLETE.md](../SPEC-000-COMPLETE.md) - Final completion report

### Phase Reports

- [PHASE1-COMPLETE.md](../PHASE1-COMPLETE.md) - Core workflows
- [PHASE2-COMPLETE.md](../PHASE2-COMPLETE.md) - Tools & scripts
- [PHASE3-COMPLETE.md](../PHASE3-COMPLETE.md) - Documentation
- [PHASE4-COMPLETE.md](../PHASE4-COMPLETE.md) - Integrations
- [PHASE5-COMPLETE.md](../PHASE5-COMPLETE.md) - Cleanup & validation

### Documentation Index

- [docs/README.md](README.md) - Complete documentation index
- [docs/openspec/SPEC_SYSTEM.md](openspec/SPEC_SYSTEM.md) - SPEC versioning guide

---

## 💡 Best Practices

### Using New Structure

**Workflows:**
```yaml
# Reference workflows by new names
uses: ./.github/workflows/fsl-initiation.yml

# Call workflows with fsl- prefix
workflow_run:
  workflows: ["fsl-execution"]
```

**Tools:**
```bash
# Use categorized paths
python3 .github/fsl-pipelines/ai/code-reviewer.py
python3 .github/fsl-pipelines/ml/predictor.py
python3 .github/fsl-pipelines/security/compliance-scanner.py
```

**Scripts:**
```bash
# Use organized script paths
bash .github/scripts/setup/install-actions.sh
bash .github/scripts/deployment/deploy-to-prod.sh
bash .github/scripts/blockchain-log.sh
```

**Documentation:**
```markdown
# Link to organized docs
[Setup Guide](docs/setup/SETUP.md)
[Integration Guide](docs/integrations/FOUR_MARKETS.md)
[SPEC System](docs/openspec/SPEC_SYSTEM.md)
```

---

## ❓ FAQ

### Q: Why rename workflows from flow-state-* to fsl-*?

**A:** Consistent branding. "FSL Continuum" emphasizes the persistent state that never resets, differentiating from traditional pipelines.

### Q: Why organize tools into categories?

**A:** Scalability and discoverability. 14 categories make it easy to find tools by purpose rather than searching a flat list.

### Q: Can I use the old github-actions/ directory?

**A:** No. It's archived. All functionality is in `.github/` with improvements. See `github-actions/ARCHIVED.md` for details.

### Q: What if I have external scripts calling old paths?

**A:** Update them using this guide's path mappings. All tools are in `fsl-pipelines/[category]/` and scripts in `scripts/[category]/`.

### Q: How do I verify my migration is complete?

**A:** Check:
- All workflows use fsl-* names
- All tool paths use .github/fsl-pipelines/
- All script paths use .github/scripts/
- All docs link to .github/docs/
- No references to github-actions/ (except ARCHIVED.md)

### Q: What's the difference between "continuum" and "pipeline"?

**A:** 
- **Pipeline:** Stateless, resets after each run
- **Continuum:** Persistent state, accumulates knowledge, never resets
- **Result:** Terminal velocity (maximum sustainable development speed)

---

## 🎉 Migration Complete!

If you've followed this guide, your FSL Continuum integration is up to date!

**Verify your migration:**
```bash
# All workflows present
ls .github/workflows/fsl-*.yml | wc -l
# Expected: 14 files

# All tools organized
find .github/fsl-pipelines/*/ -name "*.py" ! -name "__init__.py" | wc -l
# Expected: 23 files

# All scripts accessible
find .github/scripts/ -type f | wc -l
# Expected: 15+ files

# All docs indexed
find .github/docs/ -name "*.md" | wc -l
# Expected: 22+ files
```

**Everything working?** Congratulations! You're running FSL Continuum v2.1! 🌊

---

## 📞 Support

**Issues?** Check:
- [SPEC-000-MIGRATION.md](../SPEC-000-MIGRATION.md) - Technical details
- [TODO.md](../TODO.md) - Complete migration checklist
- [INTEGRATION-STATUS.md](../INTEGRATION-STATUS.md) - Integration setup

**Still stuck?** File an issue with:
- What you're trying to do
- Old path you're migrating from
- Error message or unexpected behavior

---

**SPEC:000** | Migration Guide | FSL Continuum v2.1  
**Updated:** January 22, 2025 | **Status:** Complete
