"""
FSL Continuum - BAML Parser Unit Tests

Complete unit tests for BAML Parser with XML transformation support
and AI integration capabilities.
"""

import unittest
import json
import time
import concurrent.futures
from pathlib import Path

# Test fixtures
from src.tests.test_framework.test_data_manager import TestDataManager
from src.tests.test_framework.mock_components import MockComponents

# Import BAML components
try:
    from src.semantic_languages.baml import BAMLParser, BAMLValidator, BAMLSchema
except ImportError:
    # Fallback for direct testing
    import sys
    sys.path.insert(0, 'src')
    from semantic_languages.baml import BAMLParser, BAMLValidator, BAMLSchema


class TestBAMLParser(unittest.TestCase):
    """Complete unit tests for BAML Parser with XML transformation support."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = BAMLParser()
        self.test_data_manager = TestDataManager()
        self.mock_components = MockComponents()
        
        # Basic test data
        self.basic_baml_data = {
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
        
        # Complex test data
        self.complex_baml_data = {
            "version": "1.0.0-fsl-integration",
            "spec": "BAML-SEMANTIC-001",
            "description": "Complex BAML test data",
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
                        "owner": "test_user"
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
                        "owner": "test_user"
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
    
    def test_parse_basic_baml(self):
        """Test basic BAML parsing functionality."""
        result = self.parser.parse(self.basic_baml_data)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertIn('boundaries', result.data)
        self.assertEqual(len(result.data['boundaries']), 1)
        
        # Check boundary data
        boundary = result.data['boundaries'][0]
        self.assertEqual(boundary['name'], 'test_boundary')
        self.assertEqual(boundary['type'], 'data')
        self.assertTrue(boundary['ai_enhanced'])
    
    def test_parse_complex_baml(self):
        """Test complex BAML parsing functionality."""
        result = self.parser.parse(self.complex_baml_data)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        
        # Check boundaries
        boundaries = result.data.get('boundaries', [])
        self.assertEqual(len(boundaries), 2)
        
        # Check first boundary
        data_boundary = boundaries[0]
        self.assertEqual(data_boundary['name'], 'data_boundary')
        self.assertEqual(data_boundary['type'], 'data')
        self.assertTrue(data_boundary['ai_enhanced'])
        
        # Check boundary constraints
        constraints = data_boundary.get('constraints', [])
        self.assertEqual(len(constraints), 1)
        
        constraint = constraints[0]
        self.assertEqual(constraint['type'], 'validation')
        self.assertEqual(constraint['operator'], 'contains')
        self.assertEqual(constraint['value'], 'semantic_metadata')
        self.assertTrue(constraint['ai_enforced'])
        
        # Check connections
        connections = result.data.get('connections', [])
        self.assertEqual(len(connections), 1)
        
        connection = connections[0]
        self.assertEqual(connection['source'], 'data_boundary')
        self.assertEqual(connection['target'], 'process_boundary')
        self.assertEqual(connection['type'], 'data_flow')
        self.assertEqual(connection['direction'], 'unidirectional')
        self.assertTrue(connection['ai_enhanced'])
        
        # Check global constraints
        global_constraints = result.data.get('constraints', [])
        self.assertEqual(len(global_constraints), 1)
        
        global_constraint = global_constraints[0]
        self.assertEqual(global_constraint['name'], 'semantic_boundary_constraint')
        self.assertEqual(global_constraint['type'], 'boundary')
        self.assertEqual(len(global_constraint['scope']), 2)
        self.assertTrue(global_constraint['ai_monitored'])
        self.assertEqual(global_constraint['severity'], 'medium')
    
    def test_parse_with_xml_transformation(self):
        """Test BAML parsing with XML transformation."""
        context = {"xml_transformation_enabled": True}
        result = self.parser.parse(self.basic_baml_data, context)
        
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
            
            # Check metadata section
            metadata = root.find('metadata')
            self.assertIsNotNone(metadata)
            
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
            self.assertEqual(len(boundary_elements), 1)
            
            boundary_element = boundary_elements[0]
            self.assertEqual(boundary_element.get('name'), 'test_boundary')
            self.assertEqual(boundary_element.get('type'), 'data')
            self.assertEqual(boundary_element.get('ai_enhanced'), 'true')
            
        except ET.ParseError as e:
            self.fail(f"XML parsing failed: {e}")
    
    def test_parse_with_ai_processing(self):
        """Test BAML parsing with AI processing."""
        context = {
            "ai_processing_enabled": True,
            "ai_enhancement": True,
            "ai_learning": True
        }
        result = self.parser.parse(self.complex_baml_data, context)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertIn('ai_processed', result.data)
        
        ai_processed = result.data['ai_processed']
        self.assertTrue(ai_processed.success)
        self.assertIsNotNone(ai_processed.metadata)
        self.assertIsNotNone(ai_processed.insights)
        self.assertIsNotNone(ai_processed.optimizations)
        
        # Check AI metadata
        metadata = ai_processed.metadata
        self.assertIn('ai_features', metadata)
        self.assertIn('models', metadata)
        self.assertIn('processing_time', metadata)
        self.assertIn('confidence_scores', metadata)
        
        # Check AI features
        ai_features = metadata['ai_features']
        self.assertIn('semantic_analysis', ai_features)
        self.assertIn('boundary_detection', ai_features)
        self.assertIn('constraint_validation', ai_features)
        self.assertIn('connection_optimization', ai_features)
        
        # Check AI insights
        insights = ai_processed.insights
        self.assertIn('boundary_patterns', insights)
        self.assertIn('connection_flows', insights)
        self.assertIn('constraint_relationships', insights)
        self.assertIn('ai_enhancement_opportunities', insights)
        
        # Check AI optimizations
        optimizations = ai_processed.optimizations
        self.assertIn('boundary_optimizations', optimizations)
        self.assertIn('connection_optimizations', optimizations)
        self.assertIn('constraint_optimizations', optimizations)
        self.assertIn('performance_optimizations', optimizations)
    
    def test_parse_invalid_baml(self):
        """Test parsing invalid BAML data."""
        invalid_data = {"invalid": "data"}
        result = self.parser.parse(invalid_data)
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertIn('version', result.error_message)
    
    def test_parse_empty_baml(self):
        """Test parsing empty BAML data."""
        result = self.parser.parse({})
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertIn('version', result.error_message)
    
    def test_parse_baml_missing_required_fields(self):
        """Test parsing BAML data with missing required fields."""
        # Missing version
        data_missing_version = {
            "spec": "BAML-SEMANTIC-001",
            "boundaries": []
        }
        result = self.parser.parse(data_missing_version)
        self.assertFalse(result.success)
        
        # Missing spec
        data_missing_spec = {
            "version": "1.0.0-fsl-integration",
            "boundaries": []
        }
        result = self.parser.parse(data_missing_spec)
        self.assertFalse(result.success)
        
        # Invalid boundary
        data_invalid_boundary = {
            "version": "1.0.0-fsl-integration",
            "spec": "BAML-SEMANTIC-001",
            "boundaries": [
                {
                    "type": "data"  # Missing name
                }
            ]
        }
        result = self.parser.parse(data_invalid_boundary)
        self.assertFalse(result.success)
    
    def test_validate_schema(self):
        """Test BAML schema validation."""
        result = self.parser.validate_schema(self.basic_baml_data)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        
        # Test invalid schema
        invalid_schema = {"invalid": "data"}
        result = self.parser.validate_schema(invalid_schema)
        
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
    
    def test_xml_round_trip(self):
        """Test XML round-trip transformation."""
        # Parse with XML transformation
        context = {"xml_transformation_enabled": True}
        parse_result = self.parser.parse(self.basic_baml_data, context)
        
        self.assertTrue(parse_result.success)
        xml_wrapper = parse_result.data['xml_wrapped']
        
        # Unwrap XML back to BAML
        unwrap_result = self.parser.unwrap_xml_to_baml(xml_wrapper.xml_wrapper)
        
        self.assertTrue(unwrap_result.success)
        self.assertIsNotNone(unwrap_result.transformed_data)
        
        # Verify semantic meaning preservation
        unwrapped_data = unwrap_result.transformed_data
        self.assertEqual(unwrapped_data['version'], self.basic_baml_data['version'])
        self.assertEqual(unwrapped_data['spec'], self.basic_baml_data['spec'])
        self.assertEqual(len(unwrapped_data['boundaries']), len(self.basic_baml_data['boundaries']))
        
        # Verify boundary preservation
        original_boundary = self.basic_baml_data['boundaries'][0]
        unwrapped_boundary = unwrapped_data['boundaries'][0]
        self.assertEqual(unwrapped_boundary['name'], original_boundary['name'])
        self.assertEqual(unwrapped_boundary['type'], original_boundary['type'])
        self.assertEqual(unwrapped_boundary['ai_enhanced'], original_boundary['ai_enhanced'])
    
    def test_performance_parsing(self):
        """Test performance of BAML parsing."""
        start_time = time.time()
        
        # Parse 100 BAML documents
        for _ in range(100):
            result = self.parser.parse(self.basic_baml_data)
            self.assertTrue(result.success)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete in under 1 second
        self.assertLess(execution_time, 1.0)
        
        # Check parsing rate
        parsing_rate = 100 / execution_time
        self.assertGreater(parsing_rate, 50)  # Should parse at least 50 docs/second
    
    def test_performance_parsing_complex(self):
        """Test performance of complex BAML parsing."""
        start_time = time.time()
        
        # Parse 10 complex BAML documents
        for _ in range(10):
            result = self.parser.parse(self.complex_baml_data)
            self.assertTrue(result.success)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete in under 2 seconds
        self.assertLess(execution_time, 2.0)
        
        # Check parsing rate
        parsing_rate = 10 / execution_time
        self.assertGreater(parsing_rate, 5)  # Should parse at least 5 docs/second
    
    def test_concurrent_parsing(self):
        """Test concurrent BAML parsing."""
        def parse_baml():
            return self.parser.parse(self.basic_baml_data)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(parse_baml) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All results should be successful
        for result in results:
            self.assertTrue(result.success)
        
        # Check thread safety
        success_count = sum(1 for result in results if result.success)
        self.assertEqual(success_count, 10)
    
    def test_memory_usage_parsing(self):
        """Test memory usage during BAML parsing."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Parse 1000 BAML documents
        for _ in range(1000):
            result = self.parser.parse(self.basic_baml_data)
            self.assertTrue(result.success)
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = memory_after - memory_before
        
        # Should use less than 100MB
        self.assertLess(memory_used, 100)
    
    def test_error_handling(self):
        """Test error handling in BAML parser."""
        # Test with None data
        result = self.parser.parse(None)
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        
        # Test with non-dict data
        result = self.parser.parse("invalid")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        
        # Test with invalid boundary types
        invalid_boundary_data = {
            "version": "1.0.0-fsl-integration",
            "spec": "BAML-SEMANTIC-001",
            "boundaries": [
                {
                    "name": "test_boundary",
                    "type": "invalid_type",
                    "ai_enhanced": True
                }
            ]
        }
        result = self.parser.parse(invalid_boundary_data)
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
    
    def test_context_processing(self):
        """Test context processing in BAML parser."""
        # Test with different contexts
        contexts = [
            {},
            {"xml_transformation_enabled": False},
            {"ai_processing_enabled": False},
            {"xml_transformation_enabled": True, "ai_processing_enabled": True},
            {"xml_transformation_enabled": True, "ai_processing_enabled": True, "debug_mode": True}
        ]
        
        for context in contexts:
            with self.subTest(context=context):
                result = self.parser.parse(self.basic_baml_data, context)
                self.assertTrue(result.success)
                self.assertIsNotNone(result.data)
    
    def test_get_schema(self):
        """Test getting BAML schema."""
        schema = self.parser.get_schema()
        
        self.assertIsNotNone(schema)
        self.assertIn('schemas', schema)
        self.assertIn('baml_root', schema['schemas'])
        self.assertIn('boundary', schema['schemas'])
        self.assertIn('connection', schema['schemas'])
        self.assertIn('constraint', schema['schemas'])
    
    def test_get_version(self):
        """Test getting BAML parser version."""
        version = self.parser.get_version()
        
        self.assertIsNotNone(version)
        self.assertEqual(version, "1.0.0-fsl-integration")


class TestBAMLValidator(unittest.TestCase):
    """Complete unit tests for BAML Validator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = BAMLValidator()
        
        self.valid_baml_data = {
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
    
    def test_validate_valid_baml(self):
        """Test validating valid BAML data."""
        result = self.validator.validate(self.valid_baml_data)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        self.assertIsNotNone(result.normalized_data)
    
    def test_validate_invalid_baml(self):
        """Test validating invalid BAML data."""
        invalid_data = {"invalid": "data"}
        result = self.validator.validate(invalid_data)
        
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIsNone(result.normalized_data)
    
    def test_validate_boundary_constraints(self):
        """Test validating boundary constraints."""
        result = self.validator.validate(self.valid_baml_data)
        
        self.assertTrue(result.is_valid)
        
        # Test boundary name constraints
        boundary_data = self.valid_baml_data.copy()
        boundary_data["boundaries"] = [
            {
                "name": "",  # Empty name
                "type": "data",
                "ai_enhanced": True
            }
        ]
        
        result = self.validator.validate(boundary_data)
        self.assertFalse(result.is_valid)
        
        # Test boundary type constraints
        boundary_data = self.valid_baml_data.copy()
        boundary_data["boundaries"] = [
            {
                "name": "test_boundary",
                "type": "invalid_type",  # Invalid type
                "ai_enhanced": True
            }
        ]
        
        result = self.validator.validate(boundary_data)
        self.assertFalse(result.is_valid)
    
    def test_validate_connection_constraints(self):
        """Test validating connection constraints."""
        connection_data = self.valid_baml_data.copy()
        connection_data["connections"] = [
            {
                "source": "test_boundary",
                "target": "test_boundary",
                "type": "data_flow"
            }
        ]
        
        result = self.validator.validate(connection_data)
        self.assertTrue(result.is_valid)
        
        # Test connection source constraints
        connection_data["connections"] = [
            {
                "source": "",  # Empty source
                "target": "test_boundary",
                "type": "data_flow"
            }
        ]
        
        result = self.validator.validate(connection_data)
        self.assertFalse(result.is_valid)
        
        # Test connection target constraints
        connection_data["connections"] = [
            {
                "source": "test_boundary",
                "target": "",  # Empty target
                "type": "data_flow"
            }
        ]
        
        result = self.validator.validate(connection_data)
        self.assertFalse(result.is_valid)
    
    def test_get_validation_rules(self):
        """Test getting validation rules."""
        rules = self.validator.get_validation_rules()
        
        self.assertIsNotNone(rules)
        self.assertIn('required_fields', rules)
        self.assertIn('field_patterns', rules)
        self.assertIn('value_constraints', rules)


class TestBAMLSchema(unittest.TestCase):
    """Complete unit tests for BAML Schema."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.schema = BAMLSchema()
    
    def test_get_schema_definition(self):
        """Test getting schema definition."""
        schema_def = self.schema.get_schema_definition()
        
        self.assertIsNotNone(schema_def)
        self.assertIn('schema_version', schema_def)
        self.assertIn('baml_version', schema_def)
        self.assertIn('schemas', schema_def)
    
    def test_validate_schema_version(self):
        """Test validating schema version."""
        # Test valid version
        result = self.schema.validate_version("1.0.0-fsl-integration")
        self.assertTrue(result)
        
        # Test invalid version
        result = self.schema.validate_version("invalid")
        self.assertFalse(result)
    
    def test_validate_boundary_schema(self):
        """Test validating boundary schema."""
        valid_boundary = {
            "name": "test_boundary",
            "type": "data",
            "ai_enhanced": True
        }
        
        result = self.schema.validate_boundary(valid_boundary)
        self.assertTrue(result)
        
        # Test invalid boundary
        invalid_boundary = {
            "name": "",  # Empty name
            "type": "data",
            "ai_enhanced": True
        }
        
        result = self.schema.validate_boundary(invalid_boundary)
        self.assertFalse(result)
    
    def test_get_boundary_types(self):
        """Test getting boundary types."""
        boundary_types = self.schema.get_boundary_types()
        
        self.assertIsNotNone(boundary_types)
        self.assertIn('data', boundary_types)
        self.assertIn('process', boundary_types)
        self.assertIn('system', boundary_types)
        self.assertIn('interface', boundary_types)
        self.assertIn('service', boundary_types)


if __name__ == '__main__':
    unittest.main()
