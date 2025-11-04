"""
Unit tests for Test Data Generator module.
"""

import sys
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
    
    def test_unsupported_schema_type(self):
        """Test handling of unsupported schema types."""
        with self.assertRaises(ValueError):
            self.generator.generate_data('unsupported_type')
    
    def test_save_to_file(self):
        """Test saving generated data to file."""
        result = self.generator.generate_data('json')
        
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
    
    def test_get_generation_report(self):
        """Test generation report functionality."""
        report = self.generator.get_generation_report()
        
        self.assertIsInstance(report, dict)
        self.assertIn('generator_version', report)
        self.assertIn('supported_types', report)
        self.assertIn('config', report)
        self.assertIn('last_generation', report)


class TestDataGenerationUtilities(unittest.TestCase):
    """Test utility functions for test data generation."""
    
    def test_generate_test_data_function(self):
        """Test standalone generate_test_data function."""
        result = generate_test_data('json', num_records=5)
        
        self.assertIsInstance(result, GeneratedTestData)
        self.assertEqual(result.schema_type, 'json')
        self.assertEqual(len(result.data), 5)


if __name__ == '__main__':
    unittest.main()
