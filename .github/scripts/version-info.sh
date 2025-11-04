#!/bin/bash
# FSL Continuum Version Info Script
# Usage: .github/scripts/version-info.sh [--version|--features|--all]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GITHUB_DIR="$(dirname "$SCRIPT_DIR")"

show_version() {
    echo "=== FSL Continuum Version Information ==="
    echo ""
    if [ -f "$GITHUB_DIR/VERSION" ]; then
        cat "$GITHUB_DIR/VERSION"
    else
        echo "ERROR: VERSION file not found"
        exit 1
    fi
}

show_features() {
    echo "=== FSL Continuum Features ==="
    echo ""
    if [ -f "$GITHUB_DIR/FEATURES.md" ]; then
        cat "$GITHUB_DIR/FEATURES.md"
    else
        echo "ERROR: FEATURES.md file not found"
        exit 1
    fi
}

show_summary() {
    echo "=== FSL Continuum Quick Summary ==="
    echo ""
    
    # Extract version from VERSION file
    if [ -f "$GITHUB_DIR/VERSION" ]; then
        VERSION=$(grep "\*\*v" "$GITHUB_DIR/VERSION" | head -1 | sed 's/\*\*//g')
        SHORT_COMMIT=$(grep "^- \*\*Short Hash\*\*" "$GITHUB_DIR/VERSION" | cut -d: -f2 | xargs)
        
        echo "Version: $VERSION"
        echo "Commit: $SHORT_COMMIT"
        echo ""
    fi
    
    # Count resources
    WORKFLOW_COUNT=$(find "$GITHUB_DIR/workflows" -name "*.yml" -type f 2>/dev/null | wc -l)
    TOOL_COUNT=$(find "$GITHUB_DIR/fsl-pipelines" -name "*.py" -type f ! -name "__init__.py" 2>/dev/null | wc -l)
    DOC_COUNT=$(find "$GITHUB_DIR" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
    
    echo "Available Resources:"
    echo "  - Workflows: $WORKFLOW_COUNT"
    echo "  - Tools: $TOOL_COUNT"
    echo "  - Core Docs: $DOC_COUNT"
    echo ""
    echo "Status: ✅ Production Ready"
    echo "Terminal Velocity: ✅ Achieved"
    echo ""
    echo "For full details:"
    echo "  - Version info: cat .github/VERSION"
    echo "  - Feature list: cat .github/FEATURES.md"
    echo "  - Full README: cat .github/README.md"
}

# Main
case "${1:-}" in
    --version|-v)
        show_version
        ;;
    --features|-f)
        show_features
        ;;
    --all|-a)
        show_version
        echo ""
        echo ""
        show_features
        ;;
    --summary|-s|"")
        show_summary
        ;;
    --help|-h)
        echo "Usage: $(basename "$0") [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --version, -v     Show VERSION file content"
        echo "  --features, -f    Show FEATURES.md file content"
        echo "  --all, -a         Show both VERSION and FEATURES.md"
        echo "  --summary, -s     Show quick summary (default)"
        echo "  --help, -h        Show this help message"
        echo ""
        echo "Examples:"
        echo "  $(basename "$0")              # Show summary"
        echo "  $(basename "$0") --version    # Show version details"
        echo "  $(basename "$0") --features   # Show all features"
        ;;
    *)
        echo "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
