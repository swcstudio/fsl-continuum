#!/usr/bin/env python3
"""
FSL Continuum - Deepwiki Generator

SPEC:000 - Tools & Scripts Migration
Part of FSL Continuum v2.1 - Terminal Velocity CI/CD

Multi-Market Engineering Principles:
- US: Innovation & rapid iteration
- CN: Scale & performance optimization  
- IN: Quality assurance & cost-effectiveness
- JP: Craftsmanship (Monozukuri, Kaizen, Wa, Ringi, Anshin)

Japanese Principles:
- Monozukuri (ものづくり): Craftsmanship in manufacturing/code
- Kaizen (改善): Continuous improvement
- Wa (和): Harmony and teamwork
- Ringi (稟議): Consensus-based decision making
- Anshin (安心): Peace of mind through security

Category: Docs
"""

import os
import sys
import json
import logging
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, UTC
import base64
import requests
from dataclasses import dataclass, asdict

# Add deepwiki-open to path
sys.path.append('/opt/deepwiki-open')
sys.path.append('/opt/deepwiki-open/api')

# Setup path for deepwiki imports
DEEPWIKI_PATH = '/opt/deepwiki-open'

@dataclass
class DocumentationConfig:
    """Configuration for DeepWiki generation."""
    repo_url: str
    pr_number: Optional[str] = None
    branch: str = "main"
    output_dir: str = "docs"
    include_context: bool = True
    include_greptile_analysis: bool = True
    include_business_practices: bool = True
    theme: str = "github"
    api_keys: Dict[str, str] = None

class DeepWikiGenerator:
    """Enhanced DeepWiki generator with GitHub Actions and Greptile integration."""
    
    def __init__(self, config: DocumentationConfig):
        self.config = config
        self.logger = self._setup_logging()
        self.temp_dir = None
        self.deepwiki_repo = None
        
    def _setup_logging(self):
        """Setup comprehensive logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def load_environment(self):
        """Load environment variables and API keys."""
        self.logger.info("Loading environment configuration...")
        
        # Load from environment
        api_keys = {}
        api_keys['google_api_key'] = os.getenv('GOOGLE_API_KEY')
        api_keys['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        api_keys['openrouter_api_key'] = os.getenv('OPENROUTER_API_KEY')
        api_keys['github_token'] = os.getenv('GITHUB_TOKEN')
        
        # Check required keys
        required_keys = ['GOOGLE_API_KEY', 'OPENAI_API_KEY']
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            self.logger.warning(f"Missing API keys: {missing_keys}")
            self.logger.info("Some features may be limited without these keys")
        
        self.api_keys = api_keys
        self.logger.info("Environment loaded successfully")
    
    def clone_repo(self):
        """Clone the repository for analysis."""
        self.logger.info(f"Cloning repository: {self.config.repo_url}")
        
        self.temp_dir = tempfile.mkdtemp(prefix='deepwiki-')
        self.logger.info(f"Working directory: {self.temp_dir}")
        
        # Add GitHub token for private repos
        clone_url = self.config.repo_url
        if self.api_keys.get('github_token') and 'github.com' in clone_url:
            if clone_url.startswith('https://'):
                clone_url = clone_url.replace('https://', f'https://{self.api_keys["github_token"]}@')
        
        try:
            subprocess.run([
                'git', 'clone', clone_url, self.temp_dir
            ], check=True, capture_output=True, text=True)
            
            # Checkout specific branch if needed
            if self.config.branch != 'main':
                subprocess.run([
                    'git', 'checkout', self.config.branch
                ], cwd=self.temp_dir, check=True, capture_output=True, text=True)
            
            self.logger.info("Repository cloned successfully")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to clone repository: {e}")
            raise
    
    def enhance_with_greptile_context(self, repo_analysis: Dict) -> Dict:
        """Enhance repo analysis with Greptile context awareness."""
        if not self.config.include_greptile_analysis:
            return repo_analysis
            
        self.logger.info("Enhancing analysis with Greptile context...")
        
        enhanced_analysis = repo_analysis.copy()
        enhanced_analysis['greptile_insights'] = {}
        
        try:
            # Greptile API integration (would need endpoint)
            if self.api_keys.get('greptile_api_key'):
                greptile_insights = self._fetch_greptile_insights()
                enhanced_analysis['greptile_insights'] = greptile_insights
            else:
                # Fallback: Simulate Greptile-like analysis
                enhanced_analysis['greptile_insights'] = self._simulate_greptile_analysis(repo_analysis)
                
            self.logger.info("Greptile context enhancement completed")
            
        except Exception as e:
            self.logger.warning(f"Greptile integration failed: {e}")
            enhanced_analysis['greptile_insights'] = {'error': str(e)}
        
        return enhanced_analysis
    
    def _simulate_greptile_analysis(self, repo_analysis: Dict) -> Dict:
        """Simulate Greptile-style analysis for business practices."""
        self.logger.info("Simulating Greptile-style business practice analysis...")
        
        insights = {
            'code_quality_areas': [],
            'security_considerations': [],
            'performance_implications': [],
            'maintainability_issues': [],
            'business_value_assessment': {},
            'technical_debt_analysis': {},
            'recommendations': []
        }
        
        # Analyze file structure for business insights
        file_types = repo_analysis.get('file_types', {})
        
        # Business value insights
        if file_types.get('python', 0) > 10:
            insights['business_value_assessment']['backend_strength'] = 'high'
        
        if file_types.get('javascript', 0) > 10 or file_types.get('typescript', 0) > 10:
            insights['business_value_assessment']['frontend_presence'] = 'strong'
        
        # Test coverage indicators
        test_files = repo_analysis.get('test_files', [])
        if len(test_files) > 0:
            insights['business_value_assessment']['testing_maturity'] = 'established'
        else:
            insights['business_value_assessment']['testing_maturity'] = 'needs_improvement'
            insights['recommendations'].append('Implement automated testing for better business reliability')
        
        # Security considerations
        security_patterns = ['auth', 'password', 'token', 'key', 'secret']
        security_files = [f for f in repo_analysis.get('files', []) 
                         if any(pattern in f.lower() for pattern in security_patterns)]
        
        if security_files:
            insights['security_considerations'].append(f"Security-related files detected: {security_files[:5]}")
            insights['recommendations'].append('Ensure robust security practices in authentication flows')
        
        # Performance indicators
        performance_files = ['cache', 'optimize', 'performance', 'benchmark']
        perf_files = [f for f in repo_analysis.get('files', []) 
                     if any(pattern in f.lower() for pattern in performance_files)]
        
        if perf_files:
            insights['performance_implications'].append("Performance optimization detected")
            insights['business_value_assessment']['performance_focus'] = 'evident'
        
        # Technical debt indicators
        TODO_comments = subprocess.run([
            'grep', '-r', 'TODO', self.temp_dir
        ], capture_output=True, text=True).stdout.count('\n') if self.temp_dir else 0
        
        if TODO_comments > 10:
            insights['technical_debt_analysis']['todo_count'] = TODO_comments
            insights['recommendations'].append(f'Address {TODO_comments} TODO items to reduce technical debt')
        
        return insights
    
    def analyze_repository(self) -> Dict:
        """Analyze the repository structure and content."""
        self.logger.info("Analyzing repository structure...")
        
        if not self.temp_dir:
            raise ValueError("Repository not cloned yet")
        
        analysis = {
            'repo_url': self.config.repo_url,
            'pr_number': self.config.pr_number,
            'branch': self.config.branch,
            'generated_at': datetime.now(UTC).isoformat(),
            'files': [],
            'file_types': {},
            'directories': [],
            'test_files': [],
            'documentation_files': [],
            'configuration_files': [],
            'security_files': []
        }
        
        # Walk through repository
        for root, dirs, files in os.walk(self.temp_dir):
            # Skip .git
            if '.git' in root:
                continue
                
            rel_path = os.path.relpath(root, self.temp_dir)
            if rel_path != '.':
                analysis['directories'].append(rel_path)
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, self.temp_dir)
                
                analysis['files'].append(rel_file_path)
                
                # Categorize files
                ext = os.path.splitext(file)[1].lower()
                analysis['file_types'][ext] = analysis['file_types'].get(ext, 0) + 1
                
                # Special categorization
                if 'test' in file.lower() or ext == '.test.js' or ext == '.spec.js':
                    analysis['test_files'].append(rel_file_path)
                
                if ext in ['.md', '.rst', '.txt']:
                    analysis['documentation_files'].append(rel_file_path)
                
                if ext in ['.yml', '.yaml', '.json', '.toml', '.env', '.ini']:
                    analysis['configuration_files'].append(rel_file_path)
                
                if any(pattern in file.lower() for pattern in ['auth', 'secret', 'key', 'password']):
                    analysis['security_files'].append(rel_file_path)
        
        # Add statistics
        analysis['total_files'] = len(analysis['files'])
        analysis['total_directories'] = len(analysis['directories'])
        
        self.logger.info(f"Analysis complete: {analysis['total_files']} files, {analysis['total_directories']} directories")
        
        return analysis
    
    def generate_deepwiki_content(self, repo_analysis: Dict) -> Dict:
        """Generate DeepWiki content using the enhanced analysis."""
        self.logger.info("Generating DeepWiki content...")
        
        try:
            # Import deepwiki modules
            from api.pages_generator import PagesGenerator
            from api.data_pipeline import DataPipeline
            
            # Initialize DeepWiki components
            pipeline = DataPipeline()
            pages_generator = PagesGenerator()
            
            # Process repository through DeepWiki pipeline
            repo_data = {
                'url': self.config.repo_url,
                'branch': self.config.branch,
                'local_path': self.temp_dir,
                'analysis': repo_analysis
            }
            
            # Generate wiki content
            wiki_content = pipeline.process_repository(repo_data)
            
            # Add enhanced business insights
            if self.config.include_business_practices:
                wiki_content['business_insights'] = self._generate_business_insights(repo_analysis)
            
            # Add PR-specific context
            if self.config.pr_number:
                wiki_content['pr_context'] = self._generate_pr_context(repo_analysis)
            
            self.logger.info("DeepWiki content generated successfully")
            return wiki_content
            
        except Exception as e:
            self.logger.error(f"DeepWiki generation failed: {e}")
            # Fallback to simple content generation
            return self._generate_fallback_content(repo_analysis)
    
    def _generate_business_insights(self, repo_analysis: Dict) -> Dict:
        """Generate business-focused insights from repository analysis."""
        insights = {
            'business_maturity': 'developing',
            'technical_health': 'good',
            'growth_potential': 'medium',
            'risk_factors': [],
            'opportunities': [],
            'recommendations': []
        }
        
        file_count = repo_analysis.get('total_files', 0)
        test_count = len(repo_analysis.get('test_files', []))
        doc_count = len(repo_analysis.get('documentaiton_files', []))
        
        # Assess business maturity
        if file_count > 100:
            insights['business_maturity'] = 'mature'
            insights['opportunities'].append('Established codebase ready for scaling')
        elif file_count < 20:
            insights['business_maturity'] = 'early'
            insights['opportunities'].append('Early stage with high growth potential')
        
        # Technical health assessment
        test_ratio = test_count / max(file_count, 1)
        if test_ratio > 0.3:
            insights['technical_health'] = 'excellent'
        elif test_ratio < 0.1:
            insights['technical_health'] = 'needs_attention'
            insights['recommendations'].append('Increase test coverage for better reliability')
        
        # Risk assessment
        if len(repo_analysis.get('security_files', [])) > 0:
            insights['opportunities'].append('Security practices in place')
            insights['risk_factors'].append('Ensure security patterns are properly implemented')
        
        return insights
    
    def _generate_pr_context(self, repo_analysis: Dict) -> Dict:
        """Generate PR-specific contextual information."""
        return {
            'pr_number': self.config.pr_number,
            'focus_areas': [
                'business_impact_analysis',
                'code_quality_assessment', 
                'security_implications',
                'performance_considerations',
                'maintainability_evaluation'
            ],
            'business_questions': [
                'How does this change affect user experience?',
                'What business value does this add?',
                'Are there any revenue implications?',
                'How scalable is this solution?',
                'What are the maintenance considerations?'
            ]
        }
    
    def _generate_fallback_content(self, repo_analysis: Dict) -> Dict:
        """Generate fallback content when DeepWiki fails."""
        self.logger.info("Generating fallback content...")
        
        return {
            'title': f'Repository Documentation: {self.config.repo_url}',
            'sections': [
                {
                    'title': 'Repository Overview',
                    'content': f"This repository contains {repo_analysis.get('total_files', 0)} files"
                },
                {
                    'title': 'Business Analysis',
                    'content': "Business-focused analysis with AI insights"
                }
            ],
            'analysis': repo_analysis,
            'generated_with': 'DeepWiki GitHub Action'
        }
    
    def generate_github_pages_site(self, wiki_content: Dict) -> str:
        """Generate static GitHub Pages site from wiki content."""
        self.logger.info("Generating GitHub Pages site...")
        
        # Create output directory structure
        output_path = Path(self.config.output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Create assets directory
        (output_path / 'assets' / 'css').mkdir(parents=True, exist_ok=True)
        (output_path / 'assets' / 'js').mkdir(parents=True, exist_ok=True)
        
        # Generate HTML files
        html_files = self._generate_html_pages(wiki_content, output_path)
        
        # Copy assets
        self._copy_static_assets(output_path)
        
        # Generate index.html
        self._generate_index_page(wiki_content, output_path)
        
        self.logger.info(f"GitHub Pages site generated in {output_path}")
        return str(output_path.absolute())
    
    def _generate_html_pages(self, wiki_content: Dict, output_path: Path) -> List[str]:
        """Generate individual HTML pages for wiki sections."""
        html_files = []
        
        for section in wiki_content.get('sections', []):
            section_filename = f"{section['title'].lower().replace(' ', '-')}.html"
            section_path = output_path / section_filename
            
            html_content = self._render_page_template(section, wiki_content)
            
            with open(section_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            html_files.append(section_filename)
        
        return html_files
    
    def _render_page_template(self, section: Dict, wiki_content: Dict) -> str:
        """Render HTML template for a wiki section."""
        template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{section.get('title', 'Documentation')} - {wiki_content.get('title', 'DeepWiki')}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body class="markdown-body">
    <header>
        <nav>
            <a href="index.html">← Back to Overview</a>
        </nav>
    </header>
    <main>
        <h1>{section.get('title', 'Documentation')}</h1>
        <div class="content">
            {section.get('content', '')}
        </div>
        
        {self._render_greptile_insights(wiki_content) if 'greptile_insights' in wiki_content else ''}
        {self._render_business_insights(wiki_content) if 'business_insights' in wiki_content else ''}
    </main>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
</body>
</html>
        """
        return template
    
    def _render_greptile_insights(self, wiki_content: Dict) -> str:
        """Render Greptile insights section."""
        insights = wiki_content.get('greptile_insights', {})
        
        if not insights:
            return ""
        
        html = """
        <div class="greptile-insights">
            <h2>🤖 AI Code Review Insights</h2>
        """
        
        for category, items in insights.items():
            if items:
                html += f"<h3>{category.replace('_', ' ').title()}</h3>"
                html += "<ul>"
                
                if isinstance(items, list):
                    for item in items:
                        html += f"<li>{item}</li>"
                else:
                    html += f"<li>{items}</li>"
                
                html += "</ul>"
        
        html += "</div>"
        return html
    
    def _render_business_insights(self, wiki_content: Dict) -> str:
        """Render business insights section."""
        insights = wiki_content.get('business_insights', {})
        
        if not insights:
            return ""
        
        html = """
        <div class="business-insights">
            <h2>💼 Business Analysis</h2>
        """
        
        for key, value in insights.items():
            if value:
                html += f"<p><strong>{key.replace('_', ' ').title()}:</strong> {value}</p>"
        
        html += "</div>"
        return html
    
    def _generate_index_page(self, wiki_content: Dict, output_path: Path):
        """Generate the main index page."""
        index_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{wiki_content.get('title', 'DeepWiki Documentation')}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="markdown-body">
    <header>
        <h1>{wiki_content.get('title', 'DeepWiki Documentation')}</h1>
        <p>Generated on: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        {f'<p>PR #{wiki_content.get("pr_number", "")}</p>' if wiki_content.get('pr_number') else ''}
    </header>
    <main>
        <section class="overview">
            <h2>📊 Repository Overview</h2>
            <p>This documentation was automatically generated using DeepWiki with AI-enhanced analysis.</p>
        </section>
        
        <section class="navigation">
            <h2>📑 Table of Contents</h2>
            <ul>
                {''.join(f'<li><a href="{section["title"].lower().replace(" ", "-")}.html">{section["title"]}</a></li>' 
                         for section in wiki_content.get('sections', []))}
            </ul>
        </section>
        
        {self._render_greptile_insights(wiki_content)}
        {self._render_business_insights(wiki_content)}
    </main>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
</body>
</html>
        """
        
        with open(output_path / 'index.html', 'w', encoding='utf-8') as f:
            f.write(index_content)
    
    def _copy_static_assets(self, output_path: Path):
        """Copy static assets for the GitHub Pages site."""
        # Create minimal CSS
        css_content = """
        body {
            max-width: 1024px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
        }
        
        .greptile-insights, .business-insights {
            background: #f6f8fa;
            border-left: 4px solid #0366d6;
            padding: 16px;
            margin: 20px 0;
            border-radius: 6px;
        }
        
        .greptile-insights h2, .business-insights h2 {
            margin-top: 0;
            color: #0366d6;
        }
        
        nav {
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e1e4e8;
        }
        
        nav a {
            color: #0366d6;
            text-decoration: none;
            font-weight: 500;
        }
        
        nav a:hover {
            text-decoration: underline;
        }
        """
        
        with open(output_path / 'assets' / 'css' / 'style.css', 'w') as f:
            f.write(css_content)
    
    def generate_summary_report(self, repo_analysis: Dict, output_path: str) -> Dict:
        """Generate a summary report of the documentation generation."""
        report = {
            'success': True,
            'repo_url': self.config.repo_url,
            'pr_number': self.config.pr_number,
            'branch': self.config.branch,
            'generated_at': datetime.now(UTC).isoformat(),
            'output_path': output_path,
            'statistics': {
                'total_files': repo_analysis.get('total_files', 0),
                'total_directories': repo_analysis.get('total_directories', 0),
                'file_types': repo_analysis.get('file_types', {}),
                'test_files': len(repo_analysis.get('test_files', [])),
                'documentation_files': len(repo_analysis.get('documentation_files', [])),
                'configuration_files': len(repo_analysis.get('configuration_files', [])),
                'security_files': len(repo_analysis.get('security_files', []))
            },
            'features_enabled': {
                'greptile_analysis': self.config.include_greptile_analysis,
                'business_practices': self.config.include_business_practices,
                'context_awareness': self.config.include_context
            },
            'generated_pages': repo_analysis.get('total_files', 0) + 1,  # +1 for index
            'business_insights_available': bool(repo_analysis.get('greptile_insights'))
        }
        
        # Save report to GitHub Actions output
        if os.getenv('GITHUB_OUTPUT'):
            with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                f.write(f"summary={json.dumps(report)}\n")
        
        return report
    
    def cleanup(self):
        """Clean up temporary files and resources."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.logger.info("Temporary files cleaned up")
    
    def execute(self) -> Dict:
        """Execute the complete DeepWiki generation workflow."""
        try:
            self.logger.info("Starting DeepWiki GitHub Action execution...")
            
            # Load environment
            self.load_environment()
            
            # Clone repository
            self.clone_repo()
            
            # Analyze repository
            repo_analysis = self.analyze_repository()
            
            # Enhance with Greptile context
            repo_analysis = self.enhance_with_greptile_context(repo_analysis)
            
            # Generate DeepWiki content
            wiki_content = self.generate_deepwiki_content(repo_analysis)
            
            # Generate GitHub Pages site
            output_path = self.generate_github_pages_site(wiki_content)
            
            # Generate summary report
            report = self.generate_summary_report(repo_analysis, output_path)
            
            self.logger.info("DeepWiki generation completed successfully!")
            return report
            
        except Exception as e:
            self.logger.error(f"DeepWiki generation failed: {e}")
            error_report = {
                'success': False,
                'error': str(e),
                'repo_url': self.config.repo_url,
                'pr_number': self.config.pr_number
            }
            return error_report
        
        finally:
            self.cleanup()


def main():
    """Main entry point for the GitHub Action."""
    parser = argparse.ArgumentParser(description='Generate DeepWiki documentation')
    parser.add_argument('--repo-url', required=True, help='Repository URL')
    parser.add_argument('--pr-number', help='Pull request number')
    parser.add_argument('--branch', default='main', help='Branch to analyze')
    parser.add_argument('--output-dir', default='docs', help='Output directory')
    parser.add_argument('--include-greptile', action='store_true', default=True, 
                       help='Include Greptile analysis')
    parser.add_argument('--include-business', action='store_true', default=True,
                       help='Include business practices analysis')
    parser.add_argument('--include-context', action='store_true', default=True,
                       help='Include context awareness')
    
    args = parser.parse_args()
    
    # Create configuration
    config = DocumentationConfig(
        repo_url=args.repo_url,
        pr_number=args.pr_number,
        branch=args.branch,
        output_dir=args.output_dir,
        include_greptile_analysis=args.include_greptile,
        include_business_practices=args.include_business,
        include_context=args.include_context
    )
    
    # Execute DeepWiki generation
    generator = DeepWikiGenerator(config)
    result = generator.execute()
    
    # Output result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
