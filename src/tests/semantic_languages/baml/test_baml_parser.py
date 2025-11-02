"""
FSL Continuum - BAML Parser Tests

Comprehensive tests for BAML (BoundaryML) parser with XML transformation support.
"""

import pytest
import time
import json
from typing import Dict, List, Optional, Any, Union, Tuple
from unittest.mock import Mock, MagicMock

# Import base test class
from ...test_framework.base_test_class import SemanticLanguageBaseTest, TestResult

# Import BAML parser
from ...semantic_languages.baml.parser import BAMLParser

class TestBAMLParser(SemanticLanguageBaseTest):
    """Comprehensive tests for BAML parser."""
    
    def setup_method(self, method_name: str):
        """Setup BAML parser test environment."""
        super().setup_method(method_name)
        self.baml_parser = BAMLParser()
        self.test_fixtures = self.test_data_manager.get_baml_test_fixtures()
    
    def teardown_method(self, method_name: str):
        """Teardown BAML parser test environment."""
        super().teardown_method(method_name)
    
    def test_parse_valid_baml_data(self):
        """Test parsing of valid BAML data."""
        # Valid BAML test cases
        valid_test_cases = [
            {
                "name": "basic_baml_structure",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                },
                "expected": {
                    "success": True,
                    "boundaries_count": 1,
                    "has_boundaries": True
                }
            },
            {
                "name": "complex_baml_structure",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": f"test_boundary_{i}",
                            "type": ["data", "process", "system"][i % 3],
                            "ai_enhanced": True
                        }
                        for i in range(5)
                    ],
                    "connections": [
                        {
                            "source": f"test_boundary_{i}",
                            "target": f"test_boundary_{(i+1) % 5}",
                            "type": "data_flow"
                        }
                        for i in range(5)
                    ],
                    "constraints": [
                        {
                            "name": f"test_constraint_{i}",
                            "type": "boundary",
                            "scope": ["test_boundary_0"]
                        }
                        for i in range(3)
                    ]
                },
                "expected": {
                    "success": True,
                    "boundaries_count": 5,
                    "connections_count": 5,
                    "constraints_count": 3,
                    "has_complex_structure": True
                }
            }
        ]
        
        for test_case in valid_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_parser.parse, 
                test_case["input"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"Test case {test_case['name']} should have succeeded"
            
            # Verify expected structure
            parsed_data = test_result.details["result"]
            expected = test_case["expected"]
            
            if "boundaries_count" in expected:
                assert len(parsed_data.get("boundaries", [])) == expected["boundaries_count"], \
                    f"Boundaries count mismatch for {test_case['name']}"
            
            if "connections_count" in expected:
                assert len(parsed_data.get("connections", [])) == expected["connections_count"], \
                    f"Connections count mismatch for {test_case['name']}"
            
            if "constraints_count" in expected:
                assert len(parsed_data.get("constraints", [])) == expected["constraints_count"], \
                    f"Constraints count mismatch for {test_case['name']}"
            
            if "has_boundaries" in expected:
                assert "boundaries" in parsed_data, \
                    f"Expected boundaries in parsed data for {test_case['name']}"
            
            if "has_complex_structure" in expected:
                assert len(parsed_data.get("boundaries", [])) > 1 or \
                       len(parsed_data.get("connections", [])) > 0 or \
                       len(parsed_data.get("constraints", [])) > 0, \
                    f"Expected complex structure for {test_case['name']}"
    
    def test_parse_invalid_baml_data(self):
        """Test parsing of invalid BAML data."""
        # Invalid BAML test cases
        invalid_test_cases = [
            {
                "name": "missing_version",
                "input": {
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": []
                },
                "expected_error": "Missing required version field"
            },
            {
                "name": "missing_spec",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "boundaries": []
                },
                "expected_error": "Missing required spec field"
            },
            {
                "name": "invalid_boundaries_type",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": "not_a_list"
                },
                "expected_error": "Boundaries must be a list"
            },
            {
                "name": "invalid_boundary_structure",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "invalid_field": "should_not_be_here"
                        }
                    ]
                },
                "expected_error": "Invalid boundary structure"
            }
        ]
        
        for test_case in invalid_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_parser.parse, 
                test_case["input"]
            )
            
            self.assert_test_result(test_result, False)
            assert not test_result.success, f"Test case {test_case['name']} should have failed"
            assert test_result.error_message, f"Expected error message for {test_case['name']}"
            assert test_case["expected_error"].lower() in test_result.error_message.lower(), \
                f"Error message mismatch for {test_case['name']}"
    
    def test_parse_baml_with_xml_transformation(self):
        """Test BAML parsing with XML transformation."""
        xml_test_cases = [
            {
                "name": "baml_with_basic_xml",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "xml_test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                },
                "context": {"xml_transformation_enabled": True},
                "expected_xml_tags": ["baml-semantic-data", "boundaries", "boundary"],
                "expected_xml_attributes": ["version", "spec", "timestamp", "language"]
            },
            {
                "name": "baml_with_complex_xml",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": f"xml_test_boundary_{i}",
                            "type": ["data", "process", "system"][i % 3],
                            "ai_enhanced": True
                        }
                        for i in range(3)
                    ],
                    "connections": [
                        {
                            "source": f"xml_test_boundary_{i}",
                            "target": f"xml_test_boundary_{(i+1) % 3}",
                            "type": "data_flow",
                            "ai_enhanced": True
                        }
                        for i in range(3)
                    ]
                },
                "context": {"xml_transformation_enabled": True},
                "expected_xml_tags": ["baml-semantic-data", "boundaries", "boundary", "connections", "connection"],
                "expected_xml_attributes": ["version", "spec", "timestamp", "language", "name", "type"]
            }
        ]
        
        for test_case in xml_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_parser.parse, 
                test_case["input"], 
                test_case["context"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"XML test case {test_case['name']} should have succeeded"
            
            # Verify XML wrapper
            parsed_data = test_result.details["result"]
            assert "xml_wrapped" in parsed_data, \
                f"Expected xml_wrapped in parsed data for {test_case['name']}"
            
            xml_result = parsed_data["xml_wrapped"]
            assert xml_result.success, \
                f"XML transformation should have succeeded for {test_case['name']}"
            
            # Verify XML structure
            xml_string = xml_result.xml_wrapper
            expected_tags = test_case["expected_xml_tags"]
            for tag in expected_tags:
                assert f"<{tag}" in xml_string, \
                    f"Expected XML tag {tag} in {test_case['name']}"
                assert f"</{tag}>" in xml_string, \
                    f"Expected XML tag {tag} in {test_case['name']}"
            
            # Verify XML attributes
            expected_attributes = test_case["expected_xml_attributes"]
            for attribute in expected_attributes:
                assert f"{attribute}=" in xml_string, \
                    f"Expected XML attribute {attribute} in {test_case['name']}"
    
    def test_parse_baml_with_ai_processing(self):
        """Test BAML parsing with AI processing."""
        ai_test_cases = [
            {
                "name": "baml_with_basic_ai",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "ai_test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                },
                "context": {"ai_processing_enabled": True},
                "expected_ai_features": ["semantic_analysis", "ai_enhancement"]
            },
            {
                "name": "baml_with_advanced_ai",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": f"ai_test_boundary_{i}",
                            "type": ["data", "process", "system"][i % 3],
                            "ai_enhanced": True
                        }
                        for i in range(3)
                    ],
                    "ai_integration": {
                        "semantic_analysis": True,
                        "context_awareness": True,
                        "optimization": True
                    }
                },
                "context": {"ai_processing_enabled": True, "advanced_ai_enabled": True},
                "expected_ai_features": ["semantic_analysis", "context_awareness", "optimization", "ai_enhancement"]
            }
        ]
        
        for test_case in ai_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_parser.parse, 
                test_case["input"], 
                test_case["context"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"AI test case {test_case['name']} should have succeeded"
            
            # Verify AI processing
            parsed_data = test_result.details["result"]
            assert "ai_processed" in parsed_data, \
                f"Expected ai_processed in parsed data for {test_case['name']}"
            
            ai_result = parsed_data["ai_processed"]
            assert ai_result.success, \
                f"AI processing should have succeeded for {test_case['name']}"
            
            # Verify AI features
            ai_features = ai_result.metadata.get("ai_features", [])
            expected_features = test_case["expected_ai_features"]
            for feature in expected_features:
                assert feature in ai_features, \
                    f"Expected AI feature {feature} in {test_case['name']}"
    
    def test_baml_parser_edge_cases(self):
        """Test BAML parser edge cases."""
        edge_case_test_cases = [
            {
                "name": "empty_baml_data",
                "input": {},
                "expected": {
                    "success": True,
                    "empty_structure": True
                }
            },
            {
                "name": "minimal_baml_data",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001"
                },
                "expected": {
                    "success": True,
                    "minimal_structure": True,
                    "no_optional_fields": True
                }
            },
            {
                "name": "baml_data_with_empty_arrays",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [],
                    "connections": [],
                    "constraints": []
                },
                "expected": {
                    "success": True,
                    "empty_arrays": True
                }
            }
        ]
        
        for test_case in edge_case_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_parser.parse, 
                test_case["input"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"Edge case {test_case['name']} should have succeeded"
            
            # Verify expected behavior
            parsed_data = test_result.details["result"]
            expected = test_case["expected"]
            
            if expected.get("empty_structure"):
                assert len(parsed_data) <= 2, \
                    f"Expected empty structure for {test_case['name']}"
            
            if expected.get("minimal_structure"):
                assert "version" in parsed_data and "spec" in parsed_data, \
                    f"Expected minimal structure for {test_case['name']}"
                assert not any(key in parsed_data for key in ["boundaries", "connections", "constraints"]), \
                    f"Expected no optional fields for {test_case['name']}"
            
            if expected.get("empty_arrays"):
                assert all(len(parsed_data.get(key, [])) == 0 for key in ["boundaries", "connections", "constraints"]), \
                    f"Expected empty arrays for {test_case['name']}"
    
    def test_baml_parser_performance(self):
        """Test BAML parser performance."""
        performance_test_cases = [
            {
                "name": "small_baml_data",
                "input": self._generate_baml_data(boundary_count=5),
                "expected_max_time": 0.1,
                "expected_max_memory": 10
            },
            {
                "name": "medium_baml_data",
                "input": self._generate_baml_data(boundary_count=50),
                "expected_max_time": 0.5,
                "expected_max_memory": 50
            },
            {
                "name": "large_baml_data",
                "input": self._generate_baml_data(boundary_count=200),
                "expected_max_time": 2.0,
                "expected_max_memory": 200
            }
        ]
        
        for test_case in performance_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_parser.parse, 
                test_case["input"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"Performance test case {test_case['name']} should have succeeded"
            
            # Check performance thresholds
            performance_metrics = test_result.performance_metrics
            assert performance_metrics["execution_time"] <= test_case["expected_max_time"], \
                f"Execution time exceeded threshold for {test_case['name']}: " \
                f"{performance_metrics['execution_time']:.3f}s > {test_case['expected_max_time']}s"
            
            assert performance_metrics["memory_delta"] <= test_case["expected_max_memory"], \
                f"Memory usage exceeded threshold for {test_case['name']}: " \
                f"{performance_metrics['memory_delta']:.2f}MB > {test_case['expected_max_memory']}MB"
    
    def test_baml_parser_concurrent_parsing(self):
        """Test BAML parser with concurrent parsing."""
        import concurrent.futures
        
        test_data_list = [
            self._generate_baml_data(boundary_count=10),
            self._generate_baml_data(boundary_count=20),
            self._generate_baml_data(boundary_count=30)
        ]
        
        def parse_baml_data(baml_data):
            return self.baml_parser.parse(baml_data)
        
        # Test concurrent parsing
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_list = [executor.submit(parse_baml_data, data) for data in test_data_list]
            results = [future.result(timeout=5) for future in concurrent.futures.as_completed(future_list)]
        
        # Verify all results are successful
        for i, result in enumerate(results):
            assert result.success, f"Concurrent parsing result {i} should have succeeded"
            assert "boundaries" in result.data, \
                f"Expected boundaries in concurrent parsing result {i}"
    
    def test_baml_parser_memory_usage(self):
        """Test BAML parser memory usage patterns."""
        import gc
        
        memory_snapshots = []
        
        # Parse multiple times and check for memory leaks
        for iteration in range(10):
            baml_data = self._generate_baml_data(boundary_count=20)
            test_result = self.run_test_with_monitoring(
                self.baml_parser.parse, 
                baml_data
            )
            
            assert test_result.success, f"Memory test iteration {iteration} should have succeeded"
            
            # Capture memory usage
            if hasattr(self, '_get_memory_usage'):
                memory_usage = self._get_memory_usage()
                memory_snapshots.append(memory_usage)
            
            # Force garbage collection
            gc.collect()
        
        # Analyze memory patterns
        if memory_snapshots:
            max_memory = max(memory_snapshots)
            min_memory = min(memory_snapshots)
            memory_growth = max_memory - min_memory
            
            # Check for excessive memory growth
            assert memory_growth < 50, \
                f"Excessive memory growth detected: {memory_growth:.2f}MB"
            
            # Check for consistent memory usage
            avg_memory = sum(memory_snapshots) / len(memory_snapshots)
            memory_variance = sum((m - avg_memory) ** 2 for m in memory_snapshots) / len(memory_snapshots)
            
            assert memory_variance < 100, \
                f"Memory usage too variable: {memory_variance:.2f}"
    
    def test_baml_parser_error_handling(self):
        """Test BAML parser error handling and recovery."""
        error_handling_test_cases = [
            {
                "name": "malformed_data_structure",
                "input": "not_a_dict",
                "expected_error_type": "TypeError"
            },
            {
                "name": "null_data_input",
                "input": None,
                "expected_error_type": "TypeError"
            },
            {
                "name": "circular_reference_data",
                "input": self._create_circular_reference_data(),
                "expected_error_type": "ValueError"
            }
        ]
        
        for test_case in error_handling_test_cases:
            try:
                test_result = self.run_test_with_monitoring(
                    self.baml_parser.parse, 
                    test_case["input"]
                )
                
                # Should fail gracefully
                assert not test_result.success, \
                    f"Error handling test {test_case['name']} should have failed"
                assert test_result.error_message, \
                    f"Expected error message for {test_case['name']}"
                
            except Exception as e:
                # Should not raise unhandled exceptions
                assert type(e).__name__ == test_case["expected_error_type"], \
                    f"Expected {test_case['expected_error_type']} for {test_case['name']}, got {type(e).__name__}"
    
    def _generate_baml_data(self, boundary_count: int = 10) -> Dict[str, Any]:
        """Generate BAML test data with specified boundary count."""
        return {
            "version": "1.0.0-fsl-integration",
            "spec": "BAML-SEMANTIC-001",
            "description": f"Generated BAML data with {boundary_count} boundaries",
            "boundaries": [
                {
                    "name": f"test_boundary_{i}",
                    "type": ["data", "process", "system"][i % 3],
                    "ai_enhanced": True,
                    "constraints": [
                        {
                            "type": "validation",
                            "operator": "=",
                            "value": "test_value"
                        }
                    ]
                }
                for i in range(boundary_count)
            ],
            "connections": [
                {
                    "source": f"test_boundary_{i}",
                    "target": f"test_boundary_{(i+1) % boundary_count}",
                    "type": "data_flow",
                    "ai_enhanced": True,
                    "context": {
                        "flow_type": "generated_test_flow",
                        "generation_index": i
                    }
                }
                for i in range(boundary_count)
            ],
            "constraints": [
                {
                    "name": f"test_constraint_{i}",
                    "type": "system",
                    "scope": [f"test_boundary_{j}" for j in range(min(3, boundary_count))],
                    "conditions": [
                        {
                            "variable": "boundary.ai_enhanced",
                            "operator": "=",
                            "value": True
                        }
                    ]
                }
                for i in range(min(5, boundary_count // 2 + 1))
            ]
        }
    
    def _create_circular_reference_data(self) -> Dict[str, Any]:
        """Create data with circular reference for testing."""
        data = {"version": "1.0.0-fsl-integration", "spec": "BAML-SEMANTIC-001"}
        # Create circular reference
        data["circular"] = data
        return data

# Test configuration for pytest
def pytest_configure(config):
    """Configure pytest for BAML parser tests."""
    config.addinivalue_line(
        "markers", "baml_parser: BAML parser tests"
    )

# Mark all test methods
for method_name in dir(TestBAMLParser):
    if method_name.startswith("test_"):
        pytest.mark.baml_parser(getattr(TestBAMLParser, method_name))
