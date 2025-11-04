"""
Unit tests for Test Data Generator module.
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from fsl_continuum.test_data_generator import (
    TestDataGenerator, DataGenerationConfig, 
    GeneratedTestData, generate_test_data
)


class TestTestDataGenerator(unittest.TestCase):
    """Test cases for TestDataGenerator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = DataGenerationConfig(
            num_records=10,
            complexity_level="simple",
            include_edge_cases=False,
            seed=42
        )
        self.generator = TestDataGenerator(self.config)
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        self.assertIsInstance(self.generator, TestDataGenerator)
        self.assertEqual(self.generator.config.num_records, 10)
        self.assertEqual(self.generator.config.seed, 42)
        self.assertIsNotNone(self.generator.generators)
    
    def test_generate_baml_data(self):
        """Test BAML data generation."""
        result = self.generator.generate_data('baml')
        
        self.assertIsInstance(result, GeneratedTestData)
        self.assertEqual(result.schema_type, 'baml')
        self.assertEqual(len(result.data), 10)
        self.assertIsInstance(result.data, list)
        
        # Check record structure
        if result.data:
            record = result.data[0]
            self.assertIn('id', record)
            self.assertIn('name', record)
            self.assertIn('type', record)
            self.assertIn('properties', record)
            self.assertIn('metadata', record)
    
    def test_generate_pareto_lang_data(self):
        """Test Pareto-Lang data generation."""
        result = self.generator.generate_data('pareto_lang')
        
        self.assertIsInstance(result, GeneratedTestData)
        self.assertEqual(result.schema_type, 'pareto_lang')
        self.assertEqual(len(result.data), 10)
        
        # Check record structure
        if result.data:
            record = result.data[0]
            self.assertIn('id', record)
            self.assertIn('priority', record)
            self.assertIn('impact', record)
            self.assertIn('metrics', record)
            self.assertIn('confidence', record)
    
    def test_generate_xml_test_cases(self):
        """Test XML test case generation."""
        result = self.generator.generate_data('xml')
        
        self.assertIsInstance(result, GeneratedTestData)
        self.assertEqual(result.schema_type, 'xml')
        self.assertEqual(len(result.data), 10)
        self.assertIsInstance(result.data, list)
        
        # Check XML structure
        if result.data:
            xml_case = result.data[0]
            self.assertIsInstance(xml_case, str)
            self.assertIn('<?xml', xml_case)
    
    def test_generate_json_data(self):
        """Test JSON data generation."""
        result = self.generator.generate_data('json')
        
        self.assertIsInstance(result, GeneratedTestData)
        self.assertEqual(result.schema_type, 'json')
        self.assertEqual(len(result.data), 10)
        self.assertIsInstance(result.data, list)
        
        # Check JSON structure
        if result.data:
            record = result.data[0]
            self.assertIsInstance(record, dict)
            self.assertIn('id', record)
            self.assertIn('name', record)
            self.assertIn('nested', record)
    
    def test_generate_test_scenarios(self):
        """Test test scenario generation."""
        result = self.generator.generate_data('test_scenarios')
        
        self.assertIsInstance(result, GeneratedTestData)
        self.assertEqual(result.schema_type, 'test_scenarios')
        self.assertEqual(len(result.data), 10)
        
        # Check scenario structure
        if result.data:
            scenario = result.data[0]
            self.assertIn('id', scenario)
            self.assertIn('name', scenario)
            self.assertIn('type', scenario)
            self.assertIn('steps', scenario)
    
    def test_generate_mock_data(self):
        """Test mock data generation."""
        result = self.generator.generate_data('mock_data')
        
        self.assertIsInstance(result, GeneratedTestData)
        self.assertEqual(result.schema_type, 'mock_data')
        self.assertEqual(len(result.data), 10)
        
        # Check mock service structure
        if result.data:
            service = result.data[0]
            self.assertIn('service_name', service)
            self.assertIn('service_type', service)
            self.assertIn('endpoints', service)
    
    def test_edge_cases_inclusion(self):
        """Test edge cases inclusion."""
        edge_config = DataGenerationConfig(
            num_records=50,
            include_edge_cases=True,
            seed=42
        )
        edge_generator = TestDataGenerator(edge_config)
        
        result = edge_generator.generate_data('baml')
        
        # Check for edge cases (records with is_edge_case flag)
        edge_cases = [r for r in result.data if r.get('is_edge_case', False)]
        self.assertGreater(len(edge_cases), 0, "Edge cases should be present")
    
    def test_save_to_file(self):
        """Test saving generated data to file."""
        result = self.generator.generate_data('baml')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            self.generator.save_to_file(result, temp_file)
            
            # Verify file was created and contains valid JSON
            self.assertTrue(os.path.exists(temp_file))
            
            with open(temp_file, 'r') as f:
                saved_data = json.load(f)
            
            self.assertIn('metadata', saved_data)
            self.assertIn('data', saved_data)
            self.assertEqual(len(saved_data['data']), len(result.data))
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_unsupported_schema_type(self):
        """Test handling of unsupported schema types."""
        with self.assertRaises(ValueError):
            self.generator.generate_data('unsupported_type')
    
    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        config1 = DataGenerationConfig(num_records=5, seed=123)
        config2 = DataGenerationConfig(num_records=5, seed=123)
        
        generator1 = TestDataGenerator(config1)
        generator2 = TestDataGenerator(config2)
        
        result1 = generator1.generate_data('baml')
        result2 = generator2.generate_data('baml')
        
        # Should be identical due to same seed
        self.assertEqual(len(result1.data), len(result2.data))
        if result1.data and result2.data:
            self.assertEqual(result1.data[0]['id'], result2.data[0]['id'])
    
    def test_different_complexity_levels(self):
        """Test different complexity levels."""
        simple_config = DataGenerationConfig(complexity_level='simple', num_records=5)
        complex_config = DataGenerationConfig(complexity_level='complex', num_records=5)
        
        simple_generator = TestDataGenerator(simple_config)
        complex_generator = TestDataGenerator(complex_config)
        
        simple_result = simple_generator.generate_data('json')
        complex_result = complex_generator.generate_data('json')
        
        self.assertEqual(len(simple_result.data), 5)
        self.assertEqual(len(complex_result.data), 5)
    
    def test_get_generation_report(self):
        """Test generation report functionality."""
        report = self.generator.get_generation_report()
        
        self.assertIsInstance(report, dict)
        self.assertIn('generator_version', report)
        self.assertIn('supported_types', report)
        self.assertIn('config', report)
        self.assertIn('last_generation', report)
        
        # Check supported types
        supported_types = report['supported_types']
        self.assertIn('baml', supported_types)
        self.assertIn('pareto_lang', supported_types)
        self.assertIn('xml', supported_types)
        self.assertIn('json', supported_types)


class TestDataGenerationUtilities(unittest.TestCase):
    """Test utility functions for test data generation."""
    
    def test_generate_test_data_function(self):
        """Test standalone generate_test_data function."""
        result = generate_test_data('json', num_records=5)
        
        self.assertIsInstance(result, GeneratedTestData)
        self.assertEqual(result.schema_type, 'json')
        self.assertEqual(len(result.data), 5)
    
    def test_generate_test_data_with_output_file(self):
        """Test generate_test_data with output file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            result = generate_test_data('baml', num_records=3, output_file=temp_file)
            
            # Verify file was created
            self.assertTrue(os.path.exists(temp_file))
            
            # Check content
            with open(temp_file, 'r') as f:
                saved_data = json.load(f)
            
            self.assertIn('data', saved_data)
            self.assertEqual(len(saved_data['data']), 3)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()
