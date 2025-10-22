#!/bin/bash
#
# FSL Continuum Script
# SPEC:000 - Tools & Scripts Migration
# Part of FSL Continuum v2.1 - Terminal Velocity CI/CD
#

# Context Analyzer - Enhanced File Understanding for AI Systems
# This script provides deep analysis of codebase structure and context for better AI tool integration

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_analysis() {
    echo -e "${PURPLE}[ANALYSIS]${NC} $1"
}

echo "🔍 Context Analyzer - Deep File Understanding for AI Systems"
echo "=========================================================="

# Configuration
ANALYSIS_DIR="${1:-.}"
OUTPUT_DIR="${ANALYSIS_DIR}/.context-analysis"
mkdir -p "$OUTPUT_DIR"

print_status "Starting comprehensive codebase analysis..."
print_status "Analysis directory: $ANALYSIS_DIR"
print_status "Output directory: $OUTPUT_DIR"

# Step 1: File type analysis
print_analysis "1. Analyzing file types and structure..."

find "$ANALYSIS_DIR" -type f -name "*.py" | head -20 > "$OUTPUT_DIR/python_files.txt"
find "$ANALYSIS_DIR" -type f -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" | head -20 > "$OUTPUT_DIR/javascript_files.txt"
find "$ANALYSIS_DIR" -type f -name "*.md" > "$OUTPUT_DIR/markdown_files.txt"
find "$ANALYSIS_DIR" -type f -name "*.yml" -o -name "*.yaml" > "$OUTPUT_DIR/yaml_files.txt"
find "$ANALYSIS_DIR" -type f -name "Dockerfile*" -o -name "docker-compose*" > "$OUTPUT_DIR/docker_files.txt"
find "$ANALYSIS_DIR" -type f -name "requirements*.txt" -o -name "package*.json" -o -name "Cargo.toml" > "$OUTPUT_DIR/dependency_files.txt"

PYTHON_FILES=$(wc -l < "$OUTPUT_DIR/python_files.txt")
JS_FILES=$(wc -l < "$OUTPUT_DIR/javascript_files.txt")
MD_FILES=$(wc -l < "$OUTPUT_DIR/markdown_files.txt")
YAML_FILES=$(wc -l < "$OUTPUT_DIR/yaml_files.txt")
DOCKER_FILES=$(wc -l < "$OUTPUT_DIR/docker_files.txt")

print_analysis "Found: $PYTHON_FILES Python files, $JS_FILES JavaScript files, $MD_FILES Markdown files"

# Step 2: Dependency analysis
print_analysis "2. Analyzing dependencies..."

cat > "$OUTPUT_DIR/dependency_analysis.md" << EOF
# 📦 Dependency Analysis

## Python Dependencies
EOF

if [ -f "requirements.txt" ]; then
    echo "\`\`\`" >> "$OUTPUT_DIR/dependency_analysis.md"
    cat requirements.txt >> "$OUTPUT_DIR/dependency_analysis.md"
    echo "\`\`\`" >> "$OUTPUT_DIR/dependency_analysis.md"
fi

if [ -f "package.json" ]; then
    echo "## JavaScript Dependencies" >> "$OUTPUT_DIR/dependency_analysis.md"
    echo "\`\`\`json" >> "$OUTPUT_DIR/dependency_analysis.md"
    cat package.json >> "$OUTPUT_DIR/dependency_analysis.md"
    echo "\`\`\`" >> "$OUTPUT_DIR/dependency_analysis.md"
fi

# Step 3: Python import analysis (if Python files exist)
if [ $PYTHON_FILES -gt 0 ]; then
    print_analysis "3. Analyzing Python imports and dependencies..."
    
    cat > "$OUTPUT_DIR/python_analysis.py" << 'EOF'
import ast
import os
import json
from collections import defaultdict, Counter

def analyze_python_imports(file_paths):
    """Analyze Python imports across multiple files"""
    imports = defaultdict(list)
    external_deps = Counter()
    internal_deps = defaultdict(list)
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports[alias.name].append(file_path)
                        if '.' in alias.name:
                            external_deps[alias.name.split('.')[0]] += 1
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports[node.module].append(file_path)
                        if node.level > 0:  # Relative import
                            internal_deps[file_path].append(f".{node.module}")
                        else:
                            external_deps[node.module.split('.')[0]] += 1
                            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    return imports, external_deps, internal_deps

def analyze_functions_classes(file_paths):
    """Analyze function and class definitions"""
    functions = []
    classes = []
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'file': file_path,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'file': file_path,
                        'line': node.lineno,
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
                    
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    return functions, classes

if __name__ == "__main__":
    # Get Python files from the analysis
    with open('python_files.txt', 'r') as f:
        python_files = [line.strip() for line in f if line.strip()]
    
    print(f"Analyzing {len(python_files)} Python files...")
    
    imports, external_deps, internal_deps = analyze_python_imports(python_files)
    functions, classes = analyze_functions_classes(python_files)
    
    # Generate analysis report
    report = {
        'summary': {
            'total_files': len(python_files),
            'total_functions': len(functions),
            'total_classes': len(classes),
            'external_dependencies': len(external_deps)
        },
        'external_dependencies': dict(external_deps.most_common(20)),
        'top_imports': {k: v for k, v in sorted(imports.items(), key=lambda x: len(x[1]), reverse=True)[:20]},
        'functions': functions[:50],  # Limit for readability
        'classes': classes[:30]
    }
    
    with open('python_structure_analysis.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Analysis complete. Report saved to python_structure_analysis.json")
EOF

    cd "$OUTPUT_DIR"
    python3 python_analysis.py
    cd - > /dev/null
fi

# Step 4: Project structure analysis
print_analysis "4. Creating project structure map..."

cat > "$OUTPUT_DIR/project_structure.md" << EOF
# 🏗️ Project Structure Analysis

## Directory Structure
\`\`\`
$(find "$ANALYSIS_DIR" -type d -name ".git" -prune -o -type d -print | head -30 | sed 's/^/  /')
\`\`\`

## Key Files

### Configuration Files
EOF

# Find configuration files
find "$ANALYSIS_DIR" -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.toml" -o -name "*.ini" | head -10 >> "$OUTPUT_DIR/config_files.txt"

while IFS= read -r file; do
    if [ -f "$file" ]; then
        echo "- \`\`$file\`\`" >> "$OUTPUT_DIR/project_structure.md"
    fi
done < "$OUTPUT_DIR/config_files.txt"

echo "" >> "$OUTPUT_DIR/project_structure.md"
echo "### Documentation Files" >> "$OUTPUT_DIR/project_structure.md"

# Find documentation files
find "$ANALYSIS_DIR" -name "*.md" -o -name "README*" -o -name "*.rst" | head -10 >> "$OUTPUT_DIR/doc_files.txt"

while IFS= read -r file; do
    if [ -f "$file" ]; then
        echo "- \`\`$file\`\`" >> "$OUTPUT_DIR/project_structure.md"
    fi
done < "$OUTPUT_DIR/doc_files.txt"

# Step 5: Technology stack detection
print_analysis "5. Detecting technology stack..."

cat > "$OUTPUT_DIR/tech_stack.md" << EOF
# 🔧 Technology Stack Detection

## Programming Languages
EOF

if [ $PYTHON_FILES -gt 0 ]; then
    echo "### Python ($PYTHON_FILES files)" >> "$OUTPUT_DIR/tech_stack.md"
    
    # Check for Python frameworks
    if grep -r "flask\|Flask" "$ANALYSIS_DIR" --include="*.py" | head -1 > /dev/null; then
        echo "- **Flask** web framework detected" >> "$OUTPUT_DIR/tech_stack.md"
    fi
    
    if grep -r "django\|Django" "$ANALYSIS_DIR" --include="*.py" | head -1 > /dev/null; then
        echo "- **Django** web framework detected" >> "$OUTPUT_DIR/tech_stack.md"
    fi
    
    if grep -r "fastapi\|FastAPI" "$ANALYSIS_DIR" --include="*.py" | head -1 > /dev/null; then
        echo "- **FastAPI** web framework detected" >> "$OUTPUT_DIR/tech_stack.md"
    fi
fi

if [ $JS_FILES -gt 0 ]; then
    echo "### JavaScript/TypeScript ($JS_FILES files)" >> "$OUTPUT_DIR/tech_stack.md"
    
    # Check for JavaScript frameworks
    if [ -f "package.json" ]; then
        if grep -q "react\|React" package.json; then
            echo "- **React** framework detected" >> "$OUTPUT_DIR/tech_stack.md"
        fi
        if grep -q "vue\|Vue" package.json; then
            echo "- **Vue.js** framework detected" >> "$OUTPUT_DIR/tech_stack.md"
        fi
        if grep -q "express\|Express" package.json; then
            echo "- **Express.js** detected" >> "$OUTPUT_DIR/tech_stack.md"
        fi
    fi
fi

if [ $DOCKER_FILES -gt 0 ]; then
    echo "### Containerization" >> "$OUTPUT_DIR/tech_stack.md"
    echo "- **Docker** detected ($DOCKER_FILES files)" >> "$OUTPUT_DIR/tech_stack.md"
fi

# Step 6: AI-ready context generation
print_analysis "6. Generating AI-ready context..."

cat > "$OUTPUT_DIR/ai_context.json" << EOF
{
  "project_name": "$(basename "$(pwd)")",
  "analysis_timestamp": "$(date -Iseconds)",
  "file_types": {
    "python": $PYTHON_FILES,
    "javascript": $JS_FILES,
    "markdown": $MD_FILES,
    "yaml": $YAML_FILES,
    "docker": $DOCKER_FILES
  },
  "total_files": $(find "$ANALYSIS_DIR" -type f | wc -l),
  "directories": $(find "$ANALYSIS_DIR" -type d | wc -l),
  "project_structure": {
    "has_tests": $(find "$ANALYSIS_DIR" -name "*test*" -type d -o -name "*test*.py" | wc -l),
    "has_docs": [ -d "$ANALYSIS_DIR/docs" ] && echo "true" || echo "false",
    "has_config": $(find "$ANALYSIS_DIR" -name "*.yml" -o -name "*.yaml" -o -name "*.json" | wc -l),
    "has_docker": [ $DOCKER_FILES -gt 0 ] && echo "true" || echo "false"
  },
  "ai_review_guidance": {
    "focus_areas": [
      "security_vulnerabilities",
      "performance_optimizations",
      "code_quality",
      "test_coverage",
      "documentation_completeness",
      "architecture_consistency"
    ],
    "ignore_patterns": [
      "*.min.js",
      "node_modules/*",
      ".git/*",
      "__pycache__/*",
      "*.pyc"
    ]
  }
}
EOF

# Step 7: Generate comprehensive report
print_analysis "7. Generating final report..."

cat > "$OUTPUT_DIR/comprehensive_analysis.md" << EOF
# 📊 Comprehensive Codebase Analysis

Generated on: $(date)
Project: $(basename "$(pwd)")

## 📈 Summary Statistics
- **Total Files**: $(find "$ANALYSIS_DIR" -type f | wc -l)
- **Total Directories**: $(find "$ANALYSIS_DIR" -type d | wc -l)
- **Python Files**: $PYTHON_FILES
- **JavaScript Files**: $JS_FILES
- **Documentation Files**: $MD_FILES
- **Configuration Files**: $YAML_FILES
- **Docker Files**: $DOCKER_FILES

## 🎯 Key Findings

### Technology Stack
$(cat "$OUTPUT_DIR/tech_stack.md")

### Project Structure
$(cat "$OUTPUT_DIR/project_structure.md")

### Dependencies
$(cat "$OUTPUT_DIR/dependency_analysis.md")

## 🤖 AI Analysis Guidance

This analysis provides context for AI tools like Greptile to better understand your codebase:

### Recommended Analysis Focus
1. **Security**: Check for hardcoded secrets, SQL injection, XSS vulnerabilities
2. **Performance**: Look for database queries, memory usage, I/O operations
3. **Maintainability**: Analyze code complexity, function length, naming conventions
4. **Test Coverage**: Verify test adequacy and quality
5. **Documentation**: Assess API documentation and code comments

### Files to Prioritize for Review
1. Main application files (app.py, main.py, index.js)
2. Authentication and authorization code
3. Database interaction code
4. API endpoints and routes
5. Configuration files

### Context for AI Tools
The \`ai_context.json\` file contains structured information optimized for AI analysis tools.

---

*This analysis was generated by the Context Analyzer script for enhanced AI code review integration.*
EOF

print_status "✅ Analysis complete!"
echo ""
echo "📁 Analysis files created in: $OUTPUT_DIR/"
echo ""
echo "📋 Generated files:"
echo "  • comprehensive_analysis.md - Full analysis report"
echo "  • ai_context.json - AI-optimized context"
echo "  • project_structure.md - Directory structure"
echo "  • tech_stack.md - Technology detection"
echo "  • dependency_analysis.md - Dependencies overview"
echo ""
if [ -f "$OUTPUT_DIR/python_structure_analysis.json" ]; then
    echo "  • python_structure_analysis.json - Python code structure"
fi
echo ""
echo "💡 Usage tips:"
echo "1. Share ai_context.json with AI tools for better analysis"
echo "2. Use comprehensive_analysis.md for PR descriptions"
echo "3. Update analysis regularly as project evolves"
echo ""
print_status "Better file understanding achieved! 🚀"
