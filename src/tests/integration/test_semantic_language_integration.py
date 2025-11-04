"""
FSL Continuum - Semantic Language Integration Tests

Complete integration tests for BAML and Pareto-Lang semantic languages
with XML transformation support and AI integration.
"""

import unittest
import json
import time
import concurrent.futures
from pathlib import Path

# Test fixtures
from src.tests.test_framework.test_data_manager import TestDataManager
from src.tests.test_framework.mock_components import MockComponents

# Import semantic language components
try:
    from src.semantic_languages.baml import BAMLParser
    from src.semantic_languages.pareto_lang import ParetoLangParser
    from src.semantic_languages.xml_processor import UnifiedXMLProcessor
    from src.semantic_languages.bridge import SemanticLanguageBridge
    from src.semantic_languages.ai_integration import SemanticAIProcessor
except ImportError:
    # Fallback for direct testing
    import sys
    sys.path.insert(0, 'src')
    from semantic_languages.baml import BAMLParser
    from semantic_languages.pareto_lang import ParetoLangParser
    from semantic_languages.xml_processor import UnifiedXMLProcessor
    from semantic_languages.bridge import SemanticLanguageBridge
    from semantic_languages.ai_integration import SemanticAIProcessor


class TestSemanticLanguageIntegration(unittest.TestCase):
    """Complete integration tests for semantic language processing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.baml_parser = BAMLParser()
        self.pareto_parser = ParetoLangParser()
        self.xml_processor = UnifiedXMLProcessor()
        self.semantic_bridge = SemanticLanguageBridge()
        self.ai_processor = SemanticAIProcessor()
        
        self.test_data_manager = TestDataManager()
        self.mock_components = MockComponents()
        
        # Test data
        self.baml_data = {
            "version": "1.0.0-fsl-integration",
            "spec": "BAML-SEMANTIC-001",
            "description": "Integration test BAML data",
            "boundaries": [
                {
                    "name": "data_boundary",
                    "type": "data",
                    "ai_enhanced": True,
                    "constraints": [
                        {
                            "type": "validation",
                            "operator": "contains",
                            "value": "semantic_metadata",
                            "ai_enforced": True
                        }
                    ],
                    "metadata": {
                        "created_at": "2025-01-22T12:00:00Z",
                        "priority": 7,
                        "owner": "integration_test"
                    }
                },
                {
                    "name": "process_boundary",
                    "type": "process",
                    "ai_enhanced": True,
                    "constraints": [
                        {
                            "type": "performance",
                            "operator": ">",
                            "value": "min_process_time",
                            "ai_enforced": True
                        }
                    ],
                    "metadata": {
                        "created_at": "2025-01-22T12:00:00Z",
                        "priority": 8,
                        "owner": "integration_test"
                    }
                },
                {
                    "name": "system_boundary",
                    "type": "system",
                    "ai_enhanced": False,
                    "metadata": {
                        "created_at": "2025-01-22T12:00:00Z",
                        "priority": 5,
                        "owner": "integration_test"
                    }
                }
            ],
            "connections": [
                {
                    "source": "data_boundary",
                    "target": "process_boundary",
                    "type": "data_flow",
                    "direction": "unidirectional",
                    "ai_enhanced": True,
                    "priority": 9,
                    "weight": 0.85
                },
                {
                    "source": "process_boundary",
                    "target": "system_boundary",
                    "type": "control_flow",
                    "direction": "unidirectional",
                    "ai_enhanced": False,
                    "priority": 6,
                    "weight": 0.5
                }
            ],
            "constraints": [
                {
                    "name": "semantic_boundary_constraint",
                    "type": "boundary",
                    "scope": ["data_boundary", "process_boundary"],
                    "conditions": [
                        {
                            "variable": "boundary.ai_enhanced",
                            "operator": "=",
                            "value": True
                        }
                    ],
                    "ai_monitored": True,
                    "severity": "medium"
                }
            ]
        }
        
        self.pareto_lang_data = {
            "version": "1.0.0-fsl-integration",
            "spec": "PARETO-SEMANTIC-001",
            "description": "Integration test Pareto-Lang data",
            "optimizations": [
                {
                    "name": "efficiency_optimization",
                    "type": "pareto",
                    "target": "efficiency_maximization",
                    "efficiency": 0.85,
                    "constraints": [
                        {
                            "type": "performance",
                            "operator": ">=",
                            "value": "min_efficiency",
                            "ai_enforced": True
                        }
                    ],
                    "metadata": {
                        "created_at": "2025-01-22T12:00:00Z",
                        "priority": 9,
                        "owner": "integration_test"
                    }
                },
                {
                    "name": "resource_optimization",
                    "type": "pareto",
                    "target": "resource_minimization",
                    "efficiency": 0.75,
                    "metadata": {
                        "created_at": "2025-01-22T12:00:00Z",
                        "priority": 7,
                        "owner": "integration_test"
                    }
                }
            ],
            "constraints": [
                {
                    "name": "pareto_optimization_constraint",
                    "type": "optimization",
                    "scope": ["efficiency_optimization"],
                    "conditions": [
                        {
                            "variable": "optimization.efficiency",
                            "operator": ">=",
                            "value": 0.8
                        }
                    ],
                    "ai_monitored": True,
                    "severity": "high"
                }
            ]
        }
    
    def test_baml_to_xml_transformation(self):
        """Test BAML to XML transformation."""
        context = {"xml_transformation_enabled": True}
        result = self.baml_parser.parse(self.baml_data, context)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertIn('xml_wrapped', result.data)
        
        xml_wrapper = result.data['xml_wrapped']
        self.assertIsNotNone(xml_wrapper.xml_wrapper)
        self.assertTrue(xml_wrapper.success)
        self.assertEqual(xml_wrapper.xml_version, "1.0")
        self.assertEqual(xml_wrapper.encoding, "UTF-8")
        self.assertEqual(xml_wrapper.wrapper_tag, "baml-semantic-data")
        
        # Validate XML structure
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(xml_wrapper.xml_wrapper)
            self.assertEqual(root.tag, 'baml-semantic-data')
            
            # Check version attributes
            version = root.get('version')
            self.assertIsNotNone(version)
            self.assertEqual(version, '1.0.0-baml-xml')
            
            spec = root.get('spec')
            self.assertIsNotNone(spec)
            self.assertEqual(spec, 'BAML-XML-TRANSFORM-001')
            
            # Check metadata section
            metadata = root.find('metadata')
            self.assertIsNotNone(metadata)
            
            schema = metadata.find('schema')
            self.assertIsNotNone(schema)
            self.assertEqual(schema.get('type'), 'baml-schema')
            self.assertEqual(schema.get('version'), '1.0.0-baml-xml')
            
            validation = metadata.find('validation')
            self.assertIsNotNone(validation)
            self.assertEqual(validation.get('type'), 'baml-validation')
            self.assertEqual(validation.get('ai_enhanced'), 'true')
            
            # Check transformations section
            transformations = root.find('transformations')
            self.assertIsNotNone(transformations)
            self.assertEqual(transformations.get('applied'), 'true')
            self.assertEqual(transformations.get('xml_wrapping'), 'true')
            self.assertEqual(transformations.get('semantic_preservation'), 'true')
            self.assertEqual(transformations.get('context_aware'), 'true')
            self.assertEqual(transformations.get('ai_enhanced'), 'true')
            
            # Check content section
            content = root.find('baml-content')
            self.assertIsNotNone(content)
            
            # Check boundaries
            boundaries = content.find('boundaries')
            self.assertIsNotNone(boundaries)
            
            boundary_elements = boundaries.findall('boundary')
            self.assertEqual(len(boundary_elements), 3)
            
            # Check connections
            connections = content.find('connections')
            self.assertIsNotNone(connections)
            
            connection_elements = connections.findall('connection')
            self.assertEqual(len(connection_elements), 2)
            
        except ET.ParseError as e:
            self.fail(f"XML parsing failed: {e}")
    
    def test_pareto_lang_to_xml_transformation(self):
        """Test Pareto-Lang to XML transformation."""
        context = {"xml_transformation_enabled": True}
        result = self.pareto_parser.parse(self.pareto_lang_data, context)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertIn('xml_wrapped', result.data)
        
        xml_wrapper = result.data['xml_wrapped']
        self.assertIsNotNone(xml_wrapper.xml_wrapper)
        self.assertTrue(xml_wrapper.success)
        self.assertEqual(xml_wrapper.xml_version, "1.0")
        self.assertEqual(xml_wrapper.encoding, "UTF-8")
        self.assertEqual(xml_wrapper.wrapper_tag, "pareto-lang-semantic-data")
        
        # Validate XML structure
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(xml_wrapper.xml_wrapper)
            self.assertEqual(root.tag, 'pareto-lang-semantic-data')
            
            # Check version attributes
            version = root.get('version')
            self.assertIsNotNone(version)
            self.assertEqual(version, '1.0.0-pareto-lang-xml')
            
            spec = root.get('spec')
            self.assertIsNotNone(spec)
            self.assertEqual(spec, 'PARETO-LANG-XML-TRANSFORM-001')
            
            # Check content section
            content = root.find('pareto-lang-content')
            self.assertIsNotNone(content)
            
            # Check optimizations
            optimizations = content.find('optimizations')
            self.assertIsNotNone(optimizations)
            
            optimization_elements = optimizations.findall('optimization')
            self.assertEqual(len(optimization_elements), 2)
            
        except ET.ParseError as e:
            self.fail(f"XML parsing failed: {e}")
    
    def test_multi_language_xml_processing(self):
        """Test processing multiple semantic languages with XML."""
        result = self.xml_processor.process_multiple_semantic_data_with_xml({
            "baml": self.baml_data,
            "pareto_lang": self.pareto_lang_data
        })
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertIn('unified_xml', result.data)
        self.assertIn('xml_wrappers', result.data)
        
        # Check unified XML
        unified_xml = result.data['unified_xml']
        self.assertIsNotNone(unified_xml.unified_xml)
        self.assertTrue(unified_xml.success)
        self.assertEqual(unified_xml.xml_version, "1.0")
        self.assertEqual(unified_xml.encoding, "UTF-8")
        self.assertEqual(unified_xml.wrapper_tag, "unified-semantic-data")
        
        # Check XML wrappers
        xml_wrappers = result.data['xml_wrappers']
        self.assertIn('baml', xml_wrappers)
        self.assertIn('pareto_lang', xml_wrappers)
        
        # Validate unified XML structure
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(unified_xml.unified_xml)
            self.assertEqual(root.tag, 'unified-semantic-data')
            
            # Check semantic language sections
            baml_section = root.find('semantic-languages/baml')
            self.assertIsNotNone(baml_section)
            
            pareto_section = root.find('semantic-languages/pareto_lang')
            self.assertIsNotNone(pareto_section)
            
            # Check integration metadata
            integration_metadata = root.find('integration-metadata')
            self.assertIsNotNone(integration_metadata)
            
            languages = integration_metadata.find('languages')
            self.assertIsNotNone(languages)
            
            language_elements = languages.findall('language')
            self.assertEqual(len(language_elements), 2)
            
        except ET.ParseError as e:
            self.fail(f"XML parsing failed: {e}")
    
    def test_semantic_bridge_integration(self):
        """Test semantic language bridge integration."""
        result = self.semantic_bridge.connect_semantic_languages({
            "baml": self.baml_data,
            "pareto_lang": self.pareto_lang_data
        })
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertIn('connections', result.data)
        self.assertIn('semantic_mappings', result.data)
        self.assertIn('integration_metadata', result.data)
        
        # Check connections
        connections = result.data['connections']
        self.assertIsNotNone(connections)
        self.assertIn('baml_to_pareto_lang', connections)
        self.assertIn('pareto_lang_to_baml', connections)
        
        # Check semantic mappings
        semantic_mappings = result.data['semantic_mappings']
        self.assertIsNotNone(semantic_mappings)
        self.assertIn('boundary_mappings', semantic_mappings)
        self.assertIn('constraint_mappings', semantic_mappings)
        self.assertIn('metadata_mappings', semantic_mappings)
        
        # Check integration metadata
        integration_metadata = result.data['integration_metadata']
        self.assertIsNotNone(integration_metadata)
        self.assertIn('bridge_version', integration_metadata)
        self.assertIn('integration_timestamp', integration_metadata)
        self.assertIn('semantic_preservation', integration_metadata)
        self.assertIn('ai_integration', integration_metadata)
    
    def test_ai_integration_with_semantic_languages(self):
        """Test AI integration with semantic language processing."""
        result = self.ai_processor.process_semantic_languages({
            "baml": self.baml_data,
            "pareto_lang": self.pareto_lang_data
        })
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertIn('ai_processed', result.data)
        self.assertIn('semantic_insights', result.data)
        self.assertIn('optimization_suggestions', result.data)
        
        # Check AI processed data
        ai_processed = result.data['ai_processed']
        self.assertIsNotNone(ai_processed)
        self.assertIn('baml_ai_processed', ai_processed)
        self.assertIn('pareto_lang_ai_processed', ai_processed)
        self.assertIn('integration_ai_processed', ai_processed)
        
        # Check semantic insights
        semantic_insights = result.data['semantic_insights']
        self.assertIsNotNone(semantic_insights)
        self.assertIn('boundary_patterns', semantic_insights)
        self.assertIn('optimization_patterns', semantic_insights)
        self.assertIn('constraint_patterns', semantic_insights)
        self.assertIn('relationship_patterns', semantic_insights)
        
        # Check optimization suggestions
        optimization_suggestions = result.data['optimization_suggestions']
        self.assertIsNotNone(optimization_suggestions)
        self.assertIn('boundary_optimizations', optimization_suggestions)
        self.assertIn('connection_optimizations', optimization_suggestions)
        self.assertIn('constraint_optimizations', optimization_suggestions)
        self.assertIn('ai_optimizations', optimization_suggestions)
    
    def test_xml_round_trip_preservation(self):
        """Test XML round-trip preservation of semantic meaning."""
        # Process with XML transformation
        result = self.xml_processor.process_multiple_semantic_data_with_xml({
            "baml": self.baml_data,
            "pareto_lang": self.pareto_lang_data
        })
        
        self.assertTrue(result.success)
        unified_xml = result.data['unified_xml']
        
        # Unwrap and validate semantic preservation
        unwrap_result = self.xml_processor.unwrap_unified_xml_to_semantic_data(unified_xml.unified_xml)
        
        self.assertTrue(unwrap_result.success)
        self.assertIsNotNone(unwrap_result.transformed_data)
        
        # Validate semantic meaning preservation
        unwrapped_data = unwrap_result.transformed_data
        self.assertIn('baml', unwrapped_data)
        self.assertIn('pareto_lang', unwrapped_data)
        
        # Check BAML preservation
        unwrapped_baml = unwrapped_data['baml']
        self.assertEqual(unwrapped_baml['version'], self.baml_data['version'])
        self.assertEqual(unwrapped_baml['spec'], self.baml_data['spec'])
        self.assertEqual(len(unwrapped_baml['boundaries']), len(self.baml_data['boundaries']))
        self.assertEqual(len(unwrapped_baml['connections']), len(self.baml_data['connections']))
        self.assertEqual(len(unwrapped_baml['constraints']), len(self.baml_data['constraints']))
        
        # Check Pareto-Lang preservation
        unwrapped_pareto_lang = unwrapped_data['pareto_lang']
        self.assertEqual(unwrapped_pareto_lang['version'], self.pareto_lang_data['version'])
        self.assertEqual(unwrapped_pareto_lang['spec'], self.pareto_lang_data['spec'])
        self.assertEqual(len(unwrapped_pareto_lang['optimizations']), len(self.pareto_lang_data['optimizations']))
        self.assertEqual(len(unwrapped_pareto_lang['constraints']), len(self.pareto_lang_data['constraints']))
    
    def test_concurrent_semantic_language_processing(self):
        """Test concurrent semantic language processing."""
        def process_baml():
            return self.baml_parser.parse(self.baml_data)
        
        def process_pareto_lang():
            return self.pareto_parser.parse(self.pareto_lang_data)
        
        def process_multi_language():
            return self.xml_processor.process_multiple_semantic_data_with_xml({
                "baml": self.baml_data,
                "pareto_lang": self.pareto_lang_data
            })
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(process_baml),
                executor.submit(process_pareto_lang),
                executor.submit(process_multi_language),
                executor.submit(process_multi_language)  # Duplicate for concurrency test
            ]
            
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All results should be successful
        for i, result in enumerate(results):
            self.assertTrue(result.success, f"Result {i} should be successful")
            self.assertIsNotNone(result.data, f"Result {i} should have data")
    
    def test_performance_multi_language_processing(self):
        """Test performance of multi-language semantic processing."""
        start_time = time.time()
        
        # Process 10 multi-language datasets
        for _ in range(10):
            result = self.xml_processor.process_multiple_semantic_data_with_xml({
                "baml": self.baml_data,
                "pareto_lang": self.pareto_lang_data
            })
            self.assertTrue(result.success)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete in under 5 seconds
        self.assertLess(execution_time, 5.0)
        
        # Check processing rate
        processing_rate = 10 / execution_time
        self.assertGreater(processing_rate, 2.0)  # Should process at least 2 datasets/second
    
    def test_error_handling_integration(self):
        """Test error handling in integration scenarios."""
        # Test with invalid BAML data
        invalid_baml_data = {"invalid": "data"}
        result = self.xml_processor.process_multiple_semantic_data_with_xml({
            "baml": invalid_baml_data,
            "pareto_lang": self.pareto_lang_data
        })
        
        # Should handle error gracefully
        self.assertTrue(result.success)  # Should still succeed with partial data
        self.assertIn('errors', result.data)
        self.assertIn('warnings', result.data)
        
        # Test with missing semantic language
        result = self.xml_processor.process_multiple_semantic_data_with_xml({
            "baml": self.baml_data
            # Missing pareto_lang
        })
        
        self.assertTrue(result.success)  # Should succeed with available data
        self.assertIn('available_languages', result.data)
        self.assertIn('missing_languages', result.data)
        
        # Test with empty data
        result = self.xml_processor.process_multiple_semantic_data_with_xml({})
        
        self.assertTrue(result.success)  # Should succeed gracefully
        self.assertIn('message', result.data)
        self.assertEqual(result.data['message'], "No semantic language data provided")
    
    def test_context_aware_processing(self):
        """Test context-aware semantic language processing."""
        contexts = [
            {},
            {"operation_type": "semantic_analysis"},
            {"operation_type": "xml_transformation"},
            {"operation_type": "ai_processing"},
            {"operation_type": "integration", "priority": "high"},
            {"operation_type": "performance_optimization"},
            {"operation_type": "debug_mode"},
            {"operation_type": "validation_mode"},
            {"operation_type": "all_features"}
        ]
        
        for context in contexts:
            with self.subTest(context=context):
                # Test BAML with context
                baml_result = self.baml_parser.parse(self.baml_data, context)
                self.assertTrue(baml_result.success)
                
                # Test Pareto-Lang with context
                pareto_result = self.pareto_parser.parse(self.pareto_lang_data, context)
                self.assertTrue(pareto_result.success)
                
                # Test multi-language with context
                multi_result = self.xml_processor.process_multiple_semantic_data_with_xml({
                    "baml": self.baml_data,
                    "pareto_lang": self.pareto_lang_data
                }, context)
                
                self.assertTrue(multi_result.success)
                self.assertIsNotNone(multi_result.data)
    
    def test_large_data_processing(self):
        """Test processing large semantic language datasets."""
        # Generate large BAML data
        large_baml_data = self.generate_large_baml_data(100)
        
        # Generate large Pareto-Lang data
        large_pareto_data = self.generate_large_pareto_data(100)
        
        start_time = time.time()
        
        # Process large data
        result = self.xml_processor.process_multiple_semantic_data_with_xml({
            "baml": large_baml_data,
            "pareto_lang": large_pareto_data
        })
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        
        # Should complete in under 10 seconds
        self.assertLess(execution_time, 10.0)
        
        # Check memory efficiency
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        # Should use less than 500MB
        self.assertLess(memory_usage, 500)
    
    def generate_large_baml_data(self, boundary_count):
        """Generate large BAML test data."""
        data = {
            "version": "1.0.0-fsl-integration",
            "spec": "BAML-SEMANTIC-001",
            "boundaries": [],
            "connections": [],
            "constraints": []
        }
        
        for i in range(boundary_count):
            boundary = {
                "name": f"large_boundary_{i}",
                "type": "data" if i % 2 == 0 else "process",
                "ai_enhanced": i % 3 == 0,
                "metadata": {
                    "created_at": "2025-01-22T12:00:00Z",
                    "priority": (i % 10) + 1,
                    "owner": "integration_test"
                }
            }
            data["boundaries"].append(boundary)
            
            # Add connections (sparse)
            if i > 0 and i % 3 == 0:
                connection = {
                    "source": f"large_boundary_{i-1}",
                    "target": f"large_boundary_{i}",
                    "type": "data_flow",
                    "direction": "unidirectional",
                    "priority": (i % 10) + 1,
                    "weight": 0.5 + (i % 5) * 0.1
                }
                data["connections"].append(connection)
        
        return data
    
    def generate_large_pareto_data(self, optimization_count):
        """Generate large Pareto-Lang test data."""
        data = {
            "version": "1.0.0-fsl-integration",
            "spec": "PARETO-SEMANTIC-001",
            "optimizations": [],
            "constraints": []
        }
        
        for i in range(optimization_count):
            optimization = {
                "name": f"large_optimization_{i}",
                "type": "pareto",
                "target": "efficiency_maximization" if i % 2 == 0 else "resource_minimization",
                "efficiency": 0.5 + (i * 0.005) % 0.5,
                "metadata": {
                    "created_at": "2025-01-22T12:00:00Z",
                    "priority": (i % 10) + 1,
                    "owner": "integration_test"
                }
            }
            data["optimizations"].append(optimization)
        
        return data


if __name__ == '__main__':
    unittest.main()
