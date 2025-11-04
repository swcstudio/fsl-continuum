#!/usr/bin/env python3
"""
FSL Continuum Production Readiness Validation Script

Comprehensive validation of FSL Continuum production readiness including:
- Package structure and imports
- Semantic language integration
- XML transformation capabilities
- AI integration functionality
- Testing framework completeness
- Documentation coverage
- Configuration consistency
- Deployment readiness
"""

import sys
import os
import importlib
import traceback
from pathlib import Path
from typing import Dict, List, Any, Tuple

class ProductionReadinessValidator:
    """Validates FSL Continuum production readiness."""
    
    def __init__(self):
        self.results = {
            'package_structure': {'status': 'pending', 'details': []},
            'semantic_languages': {'status': 'pending', 'details': []},
            'xml_transformation': {'status': 'pending', 'details': []},
            'ai_integration': {'status': 'pending', 'details': []},
            'testing_framework': {'status': 'pending', 'details': []},
            'documentation': {'status': 'pending', 'details': []},
            'configuration': {'status': 'pending', 'details': []},
            'deployment': {'status': 'pending', 'details': []}
        }
        self.overall_status = 'pending'
        
    def validate_package_structure(self) -> bool:
        """Validate package structure and imports."""
        print("🔍 Validating package structure...")
        
        tests = [
            self._test_main_module_import,
            self._test_semantic_languages_import,
            self._test_ai_integration_import,
            self._test_xml_processing_import,
            self._test_testing_framework_import,
            self._test_configuration_import
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.results['package_structure']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.results['package_structure']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.results['package_structure']['status'] = 'PASS' if success else 'FAIL'
        print(f"✅ Package structure validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_main_module_import(self) -> bool:
        """Test main module import."""
        try:
            sys.path.insert(0, 'src')
            import fsl_continuum
            info = fsl_continuum.get_info()
            return info['version'] == '3.0.0'
        except ImportError as e:
            print(f"  ❌ Main module import failed: {e}")
            return False
        except Exception as e:
            print(f"  ❌ Main module test failed: {e}")
            return False
    
    def _test_semantic_languages_import(self) -> bool:
        """Test semantic languages import."""
        try:
            from fsl_continuum import (
                BAMLParser, BAMLValidator, BAMLXMLTransformer,
                ParetoLangParser, ParetoLangValidator, ParetoLangXMLTransformer,
                UnifiedXMLProcessor
            )
            return True
        except ImportError as e:
            print(f"  ❌ Semantic languages import failed: {e}")
            return False
    
    def _test_ai_integration_import(self) -> bool:
        """Test AI integration import."""
        try:
            from fsl_continuum import (
                AIProcessor, AIOptimizer, AIContextAwareness,
                SemanticAIProcessor, SemanticAIOptimizer
            )
            return True
        except ImportError as e:
            print(f"  ❌ AI integration import failed: {e}")
            return False
    
    def _test_xml_processing_import(self) -> bool:
        """Test XML processing import."""
        try:
            from fsl_continuum import (
                XMLProcessor, XMLValidator, XMLTransformer,
                XMLRoundTripProcessor, XMLSemanticPreservation
            )
            return True
        except ImportError as e:
            print(f"  ❌ XML processing import failed: {e}")
            return False
    
    def _test_testing_framework_import(self) -> bool:
        """Test testing framework import."""
        try:
            from fsl_continuum import (
                SemanticLanguageBaseTest, TestAutomationFramework,
                TestDataManager, TestUtils, MockComponents
            )
            return True
        except ImportError as e:
            print(f"  ❌ Testing framework import failed: {e}")
            return False
    
    def _test_configuration_import(self) -> bool:
        """Test configuration import."""
        try:
            from fsl_continuum import get_version, get_info
            version = get_version()
            info = get_info()
            return version is not None and info is not None
        except ImportError as e:
            print(f"  ❌ Configuration import failed: {e}")
            return False
    
    def validate_semantic_languages(self) -> bool:
        """Validate semantic language integration."""
        print("🔍 Validating semantic language integration...")
        
        tests = [
            self._test_baml_functionality,
            self._test_pareto_lang_functionality,
            self._test_unified_xml_processor,
            self._test_semantic_bridge,
            self._test_configuration_schemas
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.results['semantic_languages']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.results['semantic_languages']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.results['semantic_languages']['status'] = 'PASS' if success else 'FAIL'
        print(f"✅ Semantic language validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_baml_functionality(self) -> bool:
        """Test BAML functionality."""
        try:
            from fsl_continuum import BAMLParser
            parser = BAMLParser()
            
            # Test basic BAML parsing
            test_data = {
                "version": "1.0.0-fsl-integration",
                "spec": "BAML-SEMANTIC-001",
                "boundaries": [
                    {
                        "name": "test_boundary",
                        "type": "data",
                        "ai_enhanced": True
                    }
                ]
            }
            
            result = parser.parse(test_data)
            return result.success
        except Exception as e:
            print(f"  ❌ BAML functionality test failed: {e}")
            return False
    
    def _test_pareto_lang_functionality(self) -> bool:
        """Test Pareto-Lang functionality."""
        try:
            from fsl_continuum import ParetoLangParser
            parser = ParetoLangParser()
            
            # Test basic Pareto-Lang parsing
            test_data = {
                "version": "1.0.0-fsl-integration",
                "spec": "PARETO-SEMANTIC-001",
                "optimizations": [
                    {
                        "name": "test_optimization",
                        "type": "pareto",
                        "target": "efficiency_maximization",
                        "efficiency": 0.85
                    }
                ]
            }
            
            result = parser.parse(test_data)
            return result.success
        except Exception as e:
            print(f"  ❌ Pareto-Lang functionality test failed: {e}")
            return False
    
    def _test_unified_xml_processor(self) -> bool:
        """Test unified XML processor."""
        try:
            from fsl_continuum import UnifiedXMLProcessor
            processor = UnifiedXMLProcessor()
            
            # Test basic processing
            test_data = {
                "baml": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001"
                }
            }
            
            result = processor.process_multiple_semantic_data_with_xml(test_data)
            return result.success
        except Exception as e:
            print(f"  ❌ Unified XML processor test failed: {e}")
            return False
    
    def _test_semantic_bridge(self) -> bool:
        """Test semantic bridge."""
        try:
            from fsl_continuum import SemanticLanguageBridge
            bridge = SemanticLanguageBridge()
            
            # Test bridge functionality
            result = bridge.connect_semantic_languages()
            return result.success
        except Exception as e:
            print(f"  ❌ Semantic bridge test failed: {e}")
            return False
    
    def _test_configuration_schemas(self) -> bool:
        """Test configuration schemas."""
        try:
            import json
            from pathlib import Path
            
            # Test BAML schema
            schema_path = Path('src/semantic_languages/config/baml_schemas.json')
            if not schema_path.exists():
                return False
            
            with open(schema_path, 'r') as f:
                schema = json.load(f)
                return 'schemas' in schema and 'baml_root' in schema['schemas']
        except Exception as e:
            print(f"  ❌ Configuration schemas test failed: {e}")
            return False
    
    def validate_xml_transformation(self) -> bool:
        """Validate XML transformation capabilities."""
        print("🔍 Validating XML transformation capabilities...")
        
        tests = [
            self._test_xml_processor,
            self._test_xml_validator,
            self._test_xml_transformer,
            self._test_xml_round_trip,
            self._test_xml_schema_manager
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.results['xml_transformation']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.results['xml_transformation']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.results['xml_transformation']['status'] = 'PASS' if success else 'FAIL'
        print(f"✅ XML transformation validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_xml_processor(self) -> bool:
        """Test XML processor."""
        try:
            from fsl_continuum import XMLProcessor
            processor = XMLProcessor()
            
            # Test basic XML processing
            result = processor.process_xml({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ XML processor test failed: {e}")
            return False
    
    def _test_xml_validator(self) -> bool:
        """Test XML validator."""
        try:
            from fsl_continuum import XMLValidator
            validator = XMLValidator()
            
            # Test basic XML validation
            result = validator.validate_xml({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ XML validator test failed: {e}")
            return False
    
    def _test_xml_transformer(self) -> bool:
        """Test XML transformer."""
        try:
            from fsl_continuum import XMLTransformer
            transformer = XMLTransformer()
            
            # Test basic XML transformation
            result = transformer.transform_data_to_xml({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ XML transformer test failed: {e}")
            return False
    
    def _test_xml_round_trip(self) -> bool:
        """Test XML round-trip processing."""
        try:
            from fsl_continuum import XMLRoundTripProcessor
            processor = XMLRoundTripProcessor()
            
            # Test basic round-trip
            result = processor.process_round_trip({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ XML round-trip test failed: {e}")
            return False
    
    def _test_xml_schema_manager(self) -> bool:
        """Test XML schema manager."""
        try:
            from fsl_continuum import XMLSchemaManager
            manager = XMLSchemaManager()
            
            # Test basic schema management
            result = manager.load_schema("test_schema")
            return result.success
        except Exception as e:
            print(f"  ❌ XML schema manager test failed: {e}")
            return False
    
    def validate_ai_integration(self) -> bool:
        """Validate AI integration."""
        print("🔍 Validating AI integration...")
        
        tests = [
            self._test_ai_processor,
            self._test_ai_optimizer,
            self._test_ai_context_awareness,
            self._test_semantic_ai_processor,
            self._test_semantic_ai_optimizer
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.results['ai_integration']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.results['ai_integration']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.results['ai_integration']['status'] = 'PASS' if success else 'FAIL'
        print(f"✅ AI integration validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_ai_processor(self) -> bool:
        """Test AI processor."""
        try:
            from fsl_continuum import AIProcessor
            processor = AIProcessor()
            
            # Test basic AI processing
            result = processor.process({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ AI processor test failed: {e}")
            return False
    
    def _test_ai_optimizer(self) -> bool:
        """Test AI optimizer."""
        try:
            from fsl_continuum import AIOptimizer
            optimizer = AIOptimizer()
            
            # Test basic AI optimization
            result = optimizer.optimize({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ AI optimizer test failed: {e}")
            return False
    
    def _test_ai_context_awareness(self) -> bool:
        """Test AI context awareness."""
        try:
            from fsl_continuum import AIContextAwareness
            awareness = AIContextAwareness()
            
            # Test basic context awareness
            result = awareness.process_context({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ AI context awareness test failed: {e}")
            return False
    
    def _test_semantic_ai_processor(self) -> bool:
        """Test semantic AI processor."""
        try:
            from fsl_continuum import SemanticAIProcessor
            processor = SemanticAIProcessor()
            
            # Test basic semantic AI processing
            result = processor.process_semantic_data({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ Semantic AI processor test failed: {e}")
            return False
    
    def _test_semantic_ai_optimizer(self) -> bool:
        """Test semantic AI optimizer."""
        try:
            from fsl_continuum import SemanticAIOptimizer
            optimizer = SemanticAIOptimizer()
            
            # Test basic semantic AI optimization
            result = optimizer.optimize_semantic_data({"test": "data"})
            return result.success
        except Exception as e:
            print(f"  ❌ Semantic AI optimizer test failed: {e}")
            return False
    
    def validate_testing_framework(self) -> bool:
        """Validate testing framework."""
        print("🔍 Validating testing framework...")
        
        tests = [
            self._test_base_test_class,
            self._test_test_data_manager,
            self._test_test_utils,
            self._test_mock_components,
            self._test_test_automation
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.results['testing_framework']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.results['testing_framework']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.results['testing_framework']['status'] = 'PASS' if success else 'FAIL'
        print(f"✅ Testing framework validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_base_test_class(self) -> bool:
        """Test base test class."""
        try:
            from fsl_continuum import SemanticLanguageBaseTest
            # Test base test class exists
            return SemanticLanguageBaseTest is not None
        except Exception as e:
            print(f"  ❌ Base test class test failed: {e}")
            return False
    
    def _test_test_data_manager(self) -> bool:
        """Test test data manager."""
        try:
            from fsl_continuum import TestDataManager
            # Test test data manager exists
            return TestDataManager is not None
        except Exception as e:
            print(f"  ❌ Test data manager test failed: {e}")
            return False
    
    def _test_test_utils(self) -> bool:
        """Test test utils."""
        try:
            from fsl_continuum import TestUtils
            # Test test utils exists
            return TestUtils is not None
        except Exception as e:
            print(f"  ❌ Test utils test failed: {e}")
            return False
    
    def _test_mock_components(self) -> bool:
        """Test mock components."""
        try:
            from fsl_continuum import MockComponents
            # Test mock components exists
            return MockComponents is not None
        except Exception as e:
            print(f"  ❌ Mock components test failed: {e}")
            return False
    
    def _test_test_automation(self) -> bool:
        """Test test automation."""
        try:
            from fsl_continuum import TestAutomationFramework
            # Test test automation exists
            return TestAutomationFramework is not None
        except Exception as e:
            print(f"  ❌ Test automation test failed: {e}")
            return False
    
    def validate_documentation(self) -> bool:
        """Validate documentation coverage."""
        print("🔍 Validating documentation coverage...")
        
        docs_path = Path('docs')
        required_docs = [
            'README.md',
            '0001-getting-started',
            '0002-guides',
            '0003-architecture',
            '0004-planning',
            '0004-semantic-languages',
            '0005-reference',
            '0006-deployment',
            '0007-contribution'
        ]
        
        results = []
        for doc in required_docs:
            doc_path = docs_path / doc
            exists = doc_path.exists() or doc_path.with_suffix('.md').exists()
            results.append(exists)
            
            self.results['documentation']['details'].append({
                'test': f'documentation_{doc}',
                'status': 'PASS' if exists else 'FAIL',
                'details': 'Exists' if exists else 'Missing'
            })
        
        success = all(results)
        self.results['documentation']['status'] = 'PASS' if success else 'FAIL'
        print(f"✅ Documentation validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def validate_configuration(self) -> bool:
        """Validate configuration consistency."""
        print("🔍 Validating configuration consistency...")
        
        config_path = Path('src/semantic_languages/config')
        required_configs = [
            'baml_schemas.json',
            'baml_xml_transformation.json',
            'ai_integration.json'
        ]
        
        results = []
        for config in required_configs:
            config_file = config_path / config
            exists = config_file.exists()
            results.append(exists)
            
            self.results['configuration']['details'].append({
                'test': f'configuration_{config}',
                'status': 'PASS' if exists else 'FAIL',
                'details': 'Exists' if exists else 'Missing'
            })
        
        success = all(results)
        self.results['configuration']['status'] = 'PASS' if success else 'FAIL'
        print(f"✅ Configuration validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def validate_deployment(self) -> bool:
        """Validate deployment readiness."""
        print("🔍 Validating deployment readiness...")
        
        tests = [
            self._test_package_files,
            self._test_docker_configuration,
            self._test_ci_cd_configuration,
            self._test_deployment_scripts
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                self.results['deployment']['details'].append({
                    'test': test.__name__,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Success' if result else 'Failed'
                })
            except Exception as e:
                results.append(False)
                self.results['deployment']['details'].append({
                    'test': test.__name__,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        success = all(results)
        self.results['deployment']['status'] = 'PASS' if success else 'FAIL'
        print(f"✅ Deployment validation: {'PASS' if success else 'FAIL'}")
        return success
    
    def _test_package_files(self) -> bool:
        """Test package files."""
        try:
            required_files = ['pyproject.toml', 'setup.py', 'MANIFEST.in']
            results = []
            for file in required_files:
                exists = Path(file).exists()
                results.append(exists)
            return all(results)
        except Exception as e:
            print(f"  ❌ Package files test failed: {e}")
            return False
    
    def _test_docker_configuration(self) -> bool:
        """Test Docker configuration."""
        try:
            docker_files = ['Dockerfile', 'docker-compose.yml']
            results = []
            for file in docker_files:
                exists = Path(file).exists()
                results.append(exists)
            return all(results)
        except Exception as e:
            print(f"  ❌ Docker configuration test failed: {e}")
            return False
    
    def _test_ci_cd_configuration(self) -> bool:
        """Test CI/CD configuration."""
        try:
            github_path = Path('.github/workflows')
            workflows = ['semantic_language_tests.yml']
            results = []
            for workflow in workflows:
                exists = (github_path / workflow).exists()
                results.append(exists)
            return all(results)
        except Exception as e:
            print(f"  ❌ CI/CD configuration test failed: {e}")
            return False
    
    def _test_deployment_scripts(self) -> bool:
        """Test deployment scripts."""
        try:
            scripts_path = Path('scripts')
            if scripts_path.exists():
                scripts = list(scripts_path.glob('*.sh'))
                return len(scripts) > 0
            return True  # Scripts are optional
        except Exception as e:
            print(f"  ❌ Deployment scripts test failed: {e}")
            return False
    
    def run_full_validation(self) -> bool:
        """Run full production readiness validation."""
        print("🚀 Starting FSL Continuum Production Readiness Validation")
        print("=" * 60)
        
        validators = [
            self.validate_package_structure,
            self.validate_semantic_languages,
            self.validate_xml_transformation,
            self.validate_ai_integration,
            self.validate_testing_framework,
            self.validate_documentation,
            self.validate_configuration,
            self.validate_deployment
        ]
        
        results = []
        for validator in validators:
            try:
                result = validator()
                results.append(result)
                print()
            except Exception as e:
                print(f"  ❌ Validator {validator.__name__} failed: {e}")
                results.append(False)
                print()
        
        # Calculate overall status
        success = all(results)
        self.overall_status = 'PASS' if success else 'FAIL'
        
        print("=" * 60)
        print("🎯 FINAL VALIDATION RESULTS")
        print("=" * 60)
        
        for category, result in self.results.items():
            print(f"📊 {category.replace('_', ' ').title()}: {result['status']}")
            if result['details']:
                for detail in result['details']:
                    print(f"   {detail['status']}: {detail['test']} - {detail['details']}")
            print()
        
        print(f"🌊 Overall Status: {self.overall_status}")
        
        if success:
            print("✅ FSL Continuum is PRODUCTION READY!")
            print("🚀 Ready for deployment and cross-project use!")
        else:
            print("❌ FSL Continuum is NOT production ready.")
            print("🔧 Please address the failing validations above.")
        
        return success
    
    def generate_report(self) -> str:
        """Generate validation report."""
        report = [
            "# FSL Continuum Production Readiness Validation Report\n",
            f"## Overall Status: {self.overall_status}\n",
            "## Validation Results\n"
        ]
        
        for category, result in self.results.items():
            report.append(f"### {category.replace('_', ' ').title()}: {result['status']}\n")
            if result['details']:
                report.append("#### Details:\n")
                for detail in result['details']:
                    report.append(f"- {detail['status']}: {detail['test']} - {detail['details']}\n")
            report.append("\n")
        
        return "".join(report)

def main():
    """Main validation function."""
    validator = ProductionReadinessValidator()
    
    try:
        success = validator.run_full_validation()
        
        # Generate report
        report = validator.generate_report()
        
        # Save report
        with open('validation_report.md', 'w') as f:
            f.write(report)
        
        print(f"\n📄 Validation report saved to: validation_report.md")
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
