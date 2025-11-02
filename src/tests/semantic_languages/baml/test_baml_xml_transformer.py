"""
FSL Continuum - BAML XML Transformer Tests

Comprehensive tests for BAML XML transformer with transformation validation
and semantic preservation.
"""

import pytest
import time
import json
from typing import Dict, List, Optional, Any, Union, Tuple
from unittest.mock import Mock, MagicMock
import xml.etree.ElementTree as ET

# Import base test class
from ...test_framework.base_test_class import SemanticLanguageBaseTest, TestResult

# Import BAML XML transformer
from ...semantic_languages.baml.xml_transformer import BAMLXMLTransformer

class TestBAMLXMLTransformer(SemanticLanguageBaseTest):
    """Comprehensive tests for BAML XML transformer."""
    
    def setup_method(self, method_name: str):
        """Setup BAML XML transformer test environment."""
        super().setup_method(method_name)
        self.baml_xml_transformer = BAMLXMLTransformer()
        self.test_fixtures = self.test_data_manager.get_baml_test_fixtures()
    
    def teardown_method(self, method_name: str):
        """Teardown BAML XML transformer test environment."""
        super().teardown_method(method_name)
    
    def test_wrap_baml_with_xml_basic(self):
        """Test wrapping BAML data with XML - basic cases."""
        basic_test_cases = [
            {
                "name": "simple_baml_structure",
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
                "expected_xml_elements": ["baml-semantic-data", "metadata", "transformations", "baml-content", "boundaries", "boundary"],
                "expected_xml_attributes": ["version", "spec", "timestamp", "language"],
                "expected_semantic_preserved": True
            },
            {
                "name": "baml_with_connections",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "test_boundary_1",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ],
                    "connections": [
                        {
                            "source": "test_boundary_1",
                            "target": "test_boundary_2",
                            "type": "data_flow"
                        }
                    ]
                },
                "expected_xml_elements": ["baml-semantic-data", "metadata", "transformations", "baml-content", "boundaries", "boundary", "connections", "connection"],
                "expected_xml_attributes": ["version", "spec", "timestamp", "language", "source", "target"],
                "expected_semantic_preserved": True
            }
        ]
        
        for test_case in basic_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"Basic XML transformation test {test_case['name']} should have succeeded"
            
            # Verify XML wrapper
            xml_result = test_result.details["result"]
            assert xml_result.success, f"XML transformation should have succeeded for {test_case['name']}"
            assert xml_result.semantic_preserved, f"Semantic should be preserved for {test_case['name']}"
            
            # Parse XML and verify structure
            xml_string = xml_result.xml_wrapper
            root_element = ET.fromstring(xml_string)
            
            # Verify root element
            assert root_element.tag == "baml-semantic-data", \
                f"Root element should be 'baml-semantic-data' for {test_case['name']}"
            
            # Verify expected XML elements
            xml_text = xml_string
            for element in test_case["expected_xml_elements"]:
                assert f"<{element}" in xml_text, \
                    f"Expected XML element {element} in {test_case['name']}"
                assert f"</{element}>" in xml_text, \
                    f"Expected XML closing element {element} in {test_case['name']}"
            
            # Verify expected XML attributes
            for attribute in test_case["expected_xml_attributes"]:
                assert f"{attribute}=" in xml_text, \
                    f"Expected XML attribute {attribute} in {test_case['name']}"
            
            # Verify semantic preservation
            self._verify_semantic_preservation(test_case["input"], xml_result, test_case["name"])
    
    def test_wrap_baml_with_xml_complex(self):
        """Test wrapping BAML data with XML - complex cases."""
        complex_test_cases = [
            {
                "name": "baml_with_constraints",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "test_boundary_1",
                            "type": "data",
                            "ai_enhanced": True,
                            "constraints": [
                                {
                                    "type": "validation",
                                    "operator": "=",
                                    "value": "test_value"
                                }
                            ]
                        }
                    ],
                    "constraints": [
                        {
                            "name": "test_constraint",
                            "type": "boundary",
                            "scope": ["test_boundary_1"]
                        }
                    ]
                },
                "expected_xml_elements": ["baml-semantic-data", "metadata", "transformations", "baml-content", "boundaries", "boundary", "constraints", "constraint"],
                "expected_xml_attributes": ["version", "spec", "timestamp", "language", "name", "type", "scope"],
                "expected_semantic_preserved": True
            },
            {
                "name": "baml_with_ai_integration",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "ai_test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ],
                    "ai_integration": {
                        "semantic_analysis": True,
                        "context_awareness": True,
                        "optimization": True
                    }
                },
                "expected_xml_elements": ["baml-semantic-data", "metadata", "transformations", "baml-content", "boundaries", "boundary", "ai-integration"],
                "expected_xml_attributes": ["version", "spec", "timestamp", "language"],
                "expected_semantic_preserved": True
            }
        ]
        
        for test_case in complex_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"Complex XML transformation test {test_case['name']} should have succeeded"
            
            # Verify XML wrapper
            xml_result = test_result.details["result"]
            assert xml_result.success, f"XML transformation should have succeeded for {test_case['name']}"
            assert xml_result.semantic_preserved, f"Semantic should be preserved for {test_case['name']}"
            
            # Parse XML and verify complex structure
            xml_string = xml_result.xml_wrapper
            root_element = ET.fromstring(xml_string)
            
            # Verify expected XML elements
            xml_text = xml_string
            for element in test_case["expected_xml_elements"]:
                assert f"<{element}" in xml_text, \
                    f"Expected XML element {element} in {test_case['name']}"
            
            # Verify nested constraints
            if "constraints" in test_case["input"]:
                constraints_element = root_element.find(".//baml-content/constraints")
                assert constraints_element is not None, \
                    f"Expected constraints element in {test_case['name']}"
            
            # Verify AI integration
            if "ai_integration" in test_case["input"]:
                ai_element = root_element.find(".//baml-content/ai-integration")
                assert ai_element is not None, \
                    f"Expected ai-integration element in {test_case['name']}"
            
            # Verify semantic preservation
            self._verify_semantic_preservation(test_case["input"], xml_result, test_case["name"])
    
    def test_unwrap_xml_to_baml_basic(self):
        """Test unwrapping XML data back to BAML - basic cases."""
        basic_test_cases = [
            {
                "name": "simple_xml_to_baml",
                "xml_input": """<baml-semantic-data version="1.0.0-baml-xml" spec="BAML-XML-TRANSFORM-001" timestamp="2025-01-22T12:00:00Z" language="baml">
                    <metadata>
                        <schema type="baml-semantic" version="1.0.0-baml-xml"/>
                        <validation type="baml-validation" ai_enhanced="true"/>
                    </metadata>
                    <transformations applied="true" xml_wrapping="true" semantic_preservation="true"/>
                    <baml-content>
                        <boundaries>
                            <boundary name="test_boundary" type="data" ai_enhanced="true"/>
                        </boundaries>
                    </baml-content>
                </baml-semantic-data>""",
                "expected_baml_structure": {
                    "boundaries": [
                        {
                            "name": "test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                },
                "expected_semantic_preserved": True
            },
            {
                "name": "xml_with_connections_to_baml",
                "xml_input": """<baml-semantic-data version="1.0.0-baml-xml" spec="BAML-XML-TRANSFORM-001" timestamp="2025-01-22T12:00:00Z" language="baml">
                    <baml-content>
                        <boundaries>
                            <boundary name="test_boundary_1" type="data" ai_enhanced="true"/>
                            <boundary name="test_boundary_2" type="process" ai_enhanced="true"/>
                        </boundaries>
                        <connections>
                            <connection source="test_boundary_1" target="test_boundary_2" type="data_flow"/>
                        </connections>
                    </baml-content>
                </baml-semantic-data>""",
                "expected_baml_structure": {
                    "boundaries": [
                        {
                            "name": "test_boundary_1",
                            "type": "data",
                            "ai_enhanced": True
                        },
                        {
                            "name": "test_boundary_2",
                            "type": "process",
                            "ai_enhanced": True
                        }
                    ],
                    "connections": [
                        {
                            "source": "test_boundary_1",
                            "target": "test_boundary_2",
                            "type": "data_flow"
                        }
                    ]
                },
                "expected_semantic_preserved": True
            }
        ]
        
        for test_case in basic_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.unwrap_xml_to_baml,
                test_case["xml_input"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"Basic XML unwrapping test {test_case['name']} should have succeeded"
            
            # Verify BAML data
            baml_result = test_result.details["result"]
            assert baml_result.success, f"BAML extraction should have succeeded for {test_case['name']}"
            assert baml_result.semantic_preserved, f"Semantic should be preserved for {test_case['name']}"
            
            # Verify expected BAML structure
            baml_data = baml_result.transformed_data
            expected_structure = test_case["expected_baml_structure"]
            
            # Verify boundaries
            if "boundaries" in expected_structure:
                actual_boundaries = baml_data.get("boundaries", [])
                expected_boundaries = expected_structure["boundaries"]
                
                assert len(actual_boundaries) == len(expected_boundaries), \
                    f"Boundaries count mismatch in {test_case['name']}"
                
                for i, expected_boundary in enumerate(expected_boundaries):
                    actual_boundary = actual_boundaries[i]
                    assert actual_boundary["name"] == expected_boundary["name"], \
                        f"Boundary name mismatch in {test_case['name']}"
                    assert actual_boundary["type"] == expected_boundary["type"], \
                        f"Boundary type mismatch in {test_case['name']}"
                    assert actual_boundary["ai_enhanced"] == expected_boundary["ai_enhanced"], \
                        f"Boundary ai_enhanced mismatch in {test_case['name']}"
            
            # Verify connections
            if "connections" in expected_structure:
                actual_connections = baml_data.get("connections", [])
                expected_connections = expected_structure["connections"]
                
                assert len(actual_connections) == len(expected_connections), \
                    f"Connections count mismatch in {test_case['name']}"
                
                for i, expected_connection in enumerate(expected_connections):
                    actual_connection = actual_connections[i]
                    assert actual_connection["source"] == expected_connection["source"], \
                        f"Connection source mismatch in {test_case['name']}"
                    assert actual_connection["target"] == expected_connection["target"], \
                        f"Connection target mismatch in {test_case['name']}"
                    assert actual_connection["type"] == expected_connection["type"], \
                        f"Connection type mismatch in {test_case['name']}"
    
    def test_baml_xml_round_trip_transformation(self):
        """Test BAML XML round-trip transformation."""
        round_trip_test_cases = [
            {
                "name": "basic_round_trip",
                "input_data": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "round_trip_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                }
            },
            {
                "name": "complex_round_trip",
                "input_data": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": f"round_trip_boundary_{i}",
                            "type": ["data", "process", "system"][i % 3],
                            "ai_enhanced": True,
                            "constraints": [
                                {
                                    "type": "validation",
                                    "operator": "=",
                                    "value": f"test_value_{i}"
                                }
                            ]
                        }
                        for i in range(3)
                    ],
                    "connections": [
                        {
                            "source": f"round_trip_boundary_{i}",
                            "target": f"round_trip_boundary_{(i+1) % 3}",
                            "type": "data_flow",
                            "context": {
                                "flow_type": "round_trip_flow",
                                "iteration": i
                            }
                        }
                        for i in range(3)
                    ],
                    "constraints": [
                        {
                            "name": f"round_trip_constraint_{i}",
                            "type": "system",
                            "scope": [f"round_trip_boundary_{j}" for j in range(min(2, i+1))]
                        }
                        for i in range(2)
                    ],
                    "ai_integration": {
                        "semantic_analysis": True,
                        "context_awareness": True,
                        "optimization": True
                    }
                }
            }
        ]
        
        for test_case in round_trip_test_cases:
            # First wrap BAML data with XML
            wrap_test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input_data"]
            )
            
            self.assert_test_result(wrap_test_result, True)
            assert wrap_test_result.success, f"XML wrapping should have succeeded for {test_case['name']}"
            
            xml_wrapper = wrap_test_result.details["result"].xml_wrapper
            
            # Then unwrap XML data back to BAML
            unwrap_test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.unwrap_xml_to_baml,
                xml_wrapper
            )
            
            self.assert_test_result(unwrap_test_result, True)
            assert unwrap_test_result.success, f"XML unwrapping should have succeeded for {test_case['name']}"
            
            # Verify round-trip preservation
            unwrapped_baml_data = unwrap_test_result.details["result"].transformed_data
            
            self._verify_round_trip_preservation(
                test_case["input_data"], 
                unwrapped_baml_data, 
                test_case["name"]
            )
    
    def test_baml_xml_transformation_with_ai(self):
        """Test BAML XML transformation with AI enhancement."""
        ai_test_cases = [
            {
                "name": "baml_xml_with_basic_ai",
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
                "context": {"ai_enhancement_enabled": True},
                "expected_ai_features": ["semantic_analysis", "ai_enhancement"]
            },
            {
                "name": "baml_xml_with_advanced_ai",
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
                        "optimization": True,
                        "learning": True
                    }
                },
                "context": {"ai_enhancement_enabled": True, "advanced_ai_enabled": True},
                "expected_ai_features": ["semantic_analysis", "context_awareness", "optimization", "learning", "ai_enhancement"]
            }
        ]
        
        for test_case in ai_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input"],
                test_case["context"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"AI-enhanced XML transformation test {test_case['name']} should have succeeded"
            
            # Verify AI enhancement
            xml_result = test_result.details["result"]
            assert xml_result.success, f"XML transformation should have succeeded for {test_case['name']}"
            
            # Check for AI features in XML
            xml_string = xml_result.xml_wrapper
            ai_features = test_case["expected_ai_features"]
            
            for feature in ai_features:
                assert feature in xml_string.lower(), \
                    f"Expected AI feature {feature} in {test_case['name']}"
            
            # Verify AI metadata
            ai_metadata = xml_result.metadata.get("ai_enhancement", {})
            assert ai_metadata, f"Expected AI enhancement metadata for {test_case['name']}"
    
    def test_baml_xml_transformation_performance(self):
        """Test BAML XML transformer performance."""
        performance_test_cases = [
            {
                "name": "small_baml_xml_transformation",
                "input_data": self._generate_baml_data(boundary_count=5),
                "expected_max_time": 0.1,
                "expected_max_memory": 10
            },
            {
                "name": "medium_baml_xml_transformation",
                "input_data": self._generate_baml_data(boundary_count=50),
                "expected_max_time": 0.5,
                "expected_max_memory": 50
            },
            {
                "name": "large_baml_xml_transformation",
                "input_data": self._generate_baml_data(boundary_count=200),
                "expected_max_time": 2.0,
                "expected_max_memory": 200
            }
        ]
        
        for test_case in performance_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input_data"]
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
            
            # Log performance metrics
            logger.info(f"Performance metrics for {test_case['name']}: {performance_metrics}")
    
    def test_baml_xml_transformation_error_handling(self):
        """Test BAML XML transformer error handling."""
        error_test_cases = [
            {
                "name": "invalid_baml_structure",
                "input": {
                    "invalid_field": "this should not be here",
                    "boundaries": "not_a_list"
                },
                "expected_error": "Invalid BAML structure"
            },
            {
                "name": "null_baml_input",
                "input": None,
                "expected_error": "Null BAML input"
            },
            {
                "name": "malformed_baml_data",
                "input": "not_a_dict",
                "expected_error": "Malformed BAML input"
            }
        ]
        
        for test_case in error_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input"]
            )
            
            # Should handle errors gracefully
            assert not test_result.success, f"Error test case {test_case['name']} should have failed"
            assert test_result.error_message, f"Expected error message for {test_case['name']}"
            assert test_case["expected_error"].lower() in test_result.error_message.lower(), \
                f"Error message mismatch for {test_case['name']}: " \
                f"{test_case['expected_error']} not in {test_result.error_message}"
            
            logger.info(f"Error handling test {test_case['name']}: {test_result.error_message}")
    
    def test_baml_xml_transformation_edge_cases(self):
        """Test BAML XML transformer edge cases."""
        edge_case_test_cases = [
            {
                "name": "empty_baml_data",
                "input": {},
                "expected_xml_elements": ["baml-semantic-data", "metadata", "transformations", "baml-content"],
                "expected_semantic_preserved": True
            },
            {
                "name": "minimal_baml_data",
                "input": {
                    "version": "1.0.0-fsl-integration"
                },
                "expected_xml_elements": ["baml-semantic-data", "metadata", "transformations"],
                "expected_semantic_preserved": True
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
                "expected_xml_elements": ["baml-semantic-data", "metadata", "transformations", "baml-content", "boundaries", "connections", "constraints"],
                "expected_semantic_preserved": True
            }
        ]
        
        for test_case in edge_case_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"Edge case {test_case['name']} should have succeeded"
            
            # Verify XML wrapper
            xml_result = test_result.details["result"]
            assert xml_result.success, f"XML transformation should have succeeded for {test_case['name']}"
            assert xml_result.semantic_preserved, f"Semantic should be preserved for {test_case['name']}"
            
            # Verify expected XML elements
            xml_string = xml_result.xml_wrapper
            for element in test_case["expected_xml_elements"]:
                assert f"<{element}" in xml_string, \
                    f"Expected XML element {element} in {test_case['name']}"
                assert f"</{element}>" in xml_string, \
                    f"Expected XML closing element {element} in {test_case['name']}"
    
    def test_baml_xml_transformation_validation(self):
        """Test BAML XML transformation validation."""
        validation_test_cases = [
            {
                "name": "valid_xml_structure_validation",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "validation_test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                },
                "expected_validation_result": {
                    "xml_structure_valid": True,
                    "baml_schema_valid": True,
                    "semantic_preservation_valid": True
                }
            },
            {
                "name": "xml_schema_validation",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "schema_test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                },
                "expected_validation_result": {
                    "xml_schema_valid": True,
                    "baml_schema_valid": True
                }
            }
        ]
        
        for test_case in validation_test_cases:
            # Transform BAML to XML
            transform_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input"]
            )
            
            self.assert_test_result(transform_result, True)
            assert transform_result.success, f"Validation test case {test_case['name']} should have succeeded"
            
            # Get validation result
            xml_result = transform_result.details["result"]
            validation_result = xml_result.validation_result
            
            # Verify expected validation
            expected_validation = test_case["expected_validation_result"]
            
            for validation_key, expected_value in expected_validation.items():
                actual_value = validation_result.get(validation_key, False)
                assert actual_value == expected_value, \
                    f"Validation mismatch for {validation_key} in {test_case['name']}: " \
                    f"expected {expected_value}, got {actual_value}"
    
    def test_baml_xml_transformation_context_awareness(self):
        """Test BAML XML transformation with context awareness."""
        context_test_cases = [
            {
                "name": "xml_transformation_with_context",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "context_test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                },
                "context": {
                    "operation_type": "xml_transformation",
                    "priority": "high",
                    "user_preferences": {
                        "xml_pretty_print": True,
                        "xml_indentation": 2
                    }
                },
                "expected_context_features": ["operation_type", "priority", "xml_pretty_print"]
            },
            {
                "name": "xml_transformation_with_ai_context",
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": "ai_context_test_boundary",
                            "type": "data",
                            "ai_enhanced": True
                        }
                    ]
                },
                "context": {
                    "operation_type": "xml_transformation",
                    "ai_enabled": True,
                    "ai_config": {
                        "semantic_analysis": True,
                        "context_awareness": True,
                        "optimization": True
                    }
                },
                "expected_context_features": ["operation_type", "ai_enabled", "semantic_analysis", "context_awareness"]
            }
        ]
        
        for test_case in context_test_cases:
            test_result = self.run_test_with_monitoring(
                self.baml_xml_transformer.wrap_baml_with_xml,
                test_case["input"],
                test_case["context"]
            )
            
            self.assert_test_result(test_result, True)
            assert test_result.success, f"Context-aware test case {test_case['name']} should have succeeded"
            
            # Verify context features
            xml_result = test_result.details["result"]
            metadata = xml_result.metadata
            
            expected_features = test_case["expected_context_features"]
            for feature in expected_features:
                # Check if feature is applied
                assert feature in str(metadata), \
                    f"Expected context feature {feature} in {test_case['name']}"
            
            # Verify context preservation
            assert metadata.get("context_applied", False), \
                f"Context should be applied for {test_case['name']}"
    
    def _verify_semantic_preservation(self, original_data: Dict[str, Any], xml_result: Any, test_name: str):
        """Verify semantic preservation during XML transformation."""
        # Basic semantic preservation checks
        assert xml_result.semantic_preserved, \
            f"Semantic should be preserved in {test_name}"
        
        # Check if key semantic elements are preserved
        if "boundaries" in original_data:
            xml_string = xml_result.xml_wrapper
            assert "boundaries" in xml_string, \
                f"Boundaries should be preserved in XML for {test_name}"
        
        if "connections" in original_data:
            xml_string = xml_result.xml_wrapper
            assert "connections" in xml_string, \
                f"Connections should be preserved in XML for {test_name}"
        
        if "constraints" in original_data:
            xml_string = xml_result.xml_wrapper
            assert "constraints" in xml_string, \
                f"Constraints should be preserved in XML for {test_name}"
        
        if "ai_integration" in original_data:
            xml_string = xml_result.xml_wrapper
            assert "ai-integration" in xml_string, \
                f"AI integration should be preserved in XML for {test_name}"
    
    def _verify_round_trip_preservation(self, original_data: Dict[str, Any], unwrapped_data: Dict[str, Any], test_name: str):
        """Verify round-trip data preservation."""
        # Compare key semantic structures
        semantic_keys = ["boundaries", "connections", "constraints", "ai_integration"]
        
        for key in semantic_keys:
            if key in original_data:
                assert key in unwrapped_data, \
                    f"Key {key} should be preserved in round-trip for {test_name}"
                
                # For lists, compare lengths and key properties
                if isinstance(original_data[key], list):
                    assert len(unwrapped_data[key]) == len(original_data[key]), \
                        f"Length of {key} should be preserved in round-trip for {test_name}"
                    
                    for i, original_item in enumerate(original_data[key]):
                        unwrapped_item = unwrapped_data[key][i]
                        self._compare_semantic_item(original_item, unwrapped_item, key, i, test_name)
                else:
                    # For single values
                    assert unwrapped_data[key] == original_data[key], \
                        f"Value of {key} should be preserved in round-trip for {test_name}"
    
    def _compare_semantic_item(self, original_item: Any, unwrapped_item: Any, item_type: str, index: int, test_name: str):
        """Compare individual semantic items."""
        if isinstance(original_item, dict):
            for key, value in original_item.items():
                assert key in unwrapped_item, \
                    f"Key {key} should be preserved in {item_type}[{index}] for {test_name}"
                assert unwrapped_item[key] == value, \
                    f"Value of {key} should be preserved in {item_type}[{index}] for {test_name}"
        else:
            assert unwrapped_item == original_item, \
                f"Item should be preserved in {item_type}[{index}] for {test_name}"
    
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
                            "value": f"test_value_{i}"
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
            ],
            "ai_integration": {
                "semantic_analysis": True,
                "context_awareness": True,
                "optimization": True,
                "learning": True
            }
        }

# Test configuration for pytest
def pytest_configure(config):
    """Configure pytest for BAML XML transformer tests."""
    config.addinivalue_line(
        "markers", "baml_xml_transformer: BAML XML transformer tests"
    )

# Mark all test methods
for method_name in dir(TestBAMLXMLTransformer):
    if method_name.startswith("test_"):
        pytest.mark.baml_xml_transformer(getattr(TestBAMLXMLTransformer, method_name))
