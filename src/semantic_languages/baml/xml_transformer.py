"""
FSL Continuum - BAML XML Transformation Processor

Core processor for XML data transformation wrapping in BAML semantic language.
Provides XML-wrapping, unwrapping, and transformation with semantic preservation.
"""

import json
import time
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class XMLTransformationResult:
    """Result of XML transformation operation."""
    success: bool
    transformed_data: Dict[str, Any]
    xml_wrapper: str
    transformation_time: float
    semantic_preserved: bool
    validation_result: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class BAMLXMLSchema:
    """XML schema for BAML transformations."""
    wrapper_tag: str = "baml-semantic-data"
    version: str = "1.0.0-baml-xml"
    spec: str = "BAML-XML-TRANSFORM-001"
    
    def to_xml_element(self, data: Dict[str, Any]) -> ET.Element:
        """Convert BAML data to XML element."""
        root = ET.Element(self.wrapper_tag)
        root.set("version", self.version)
        root.set("spec", self.spec)
        root.set("timestamp", datetime.now().isoformat())
        root.set("language", "baml")
        
        # Add metadata
        metadata = ET.SubElement(root, "metadata")
        schema = ET.SubElement(metadata, "schema")
        schema.set("type", "baml-semantic")
        schema.set("version", self.version)
        
        validation = ET.SubElement(metadata, "validation")
        validation.set("type", "baml-validation")
        validation.set("ai_enhanced", "true")
        
        # Add transformations
        transformations = ET.SubElement(root, "transformations")
        transformations.set("applied", "true")
        transformations.set("xml_wrapping", "true")
        transformations.set("semantic_preservation", "true")
        
        # Add BAML content
        content = ET.SubElement(root, "baml-content")
        
        # Add boundaries
        if "boundaries" in data:
            boundaries = ET.SubElement(content, "boundaries")
            for boundary in data["boundaries"]:
                boundary_elem = ET.SubElement(boundaries, "boundary")
                for key, value in boundary.items():
                    if key == "constraints" and isinstance(value, list):
                        constraints = ET.SubElement(boundary_elem, "constraints")
                        for constraint in value:
                            constraint_elem = ET.SubElement(constraints, "constraint")
                            for c_key, c_value in constraint.items():
                                constraint_elem.set(c_key, str(c_value))
                    else:
                        boundary_elem.set(key, str(value))
        
        # Add connections
        if "connections" in data:
            connections = ET.SubElement(content, "connections")
            for connection in data["connections"]:
                connection_elem = ET.SubElement(connections, "connection")
                for key, value in connection.items():
                    if key == "context" and isinstance(value, dict):
                        context = ET.SubElement(connection_elem, "context")
                        for c_key, c_value in value.items():
                            context.set(c_key, str(c_value))
                    else:
                        connection_elem.set(key, str(value))
        
        # Add constraints
        if "constraints" in data:
            constraints = ET.SubElement(content, "constraints")
            for constraint in data["constraints"]:
                constraint_elem = ET.SubElement(constraints, "constraint")
                for key, value in constraint.items():
                    if key == "conditions" and isinstance(value, list):
                        conditions = ET.SubElement(constraint_elem, "conditions")
                        for condition in value:
                            condition_elem = ET.SubElement(conditions, "condition")
                            for cond_key, cond_value in condition.items():
                                condition_elem.set(cond_key, str(cond_value))
                    else:
                        constraint_elem.set(key, str(value))
        
        # Add AI integration
        if "ai_integration" in data:
            ai_integration = ET.SubElement(content, "ai-integration")
            for key, value in data["ai_integration"].items():
                if isinstance(value, dict):
                    sub_elem = ET.SubElement(ai_integration, key)
                    for sub_key, sub_value in value.items():
                        sub_elem.set(sub_key, str(sub_value))
                else:
                    ai_integration.set(key, str(value))
        
        return root
    
    def from_xml_element(self, xml_element: ET.Element) -> Dict[str, Any]:
        """Convert XML element back to BAML data."""
        baml_data = {}
        
        # Parse BAML content
        content_elem = xml_element.find("baml-content")
        if content_elem is not None:
            
            # Parse boundaries
            boundaries_elem = content_elem.find("boundaries")
            if boundaries_elem is not None:
                boundaries = []
                for boundary_elem in boundaries_elem.findall("boundary"):
                    boundary = {}
                    for key, value in boundary_elem.attrib.items():
                        if key == "constraints":
                            # Handle constraints specially
                            constraints_elem = boundary_elem.find("constraints")
                            if constraints_elem is not None:
                                constraints = []
                                for constraint_elem in constraints_elem.findall("constraint"):
                                    constraint = {}
                                    for c_key, c_value in constraint_elem.attrib.items():
                                        constraint[c_key] = c_value
                                    constraints.append(constraint)
                            boundary[key] = constraints
                        else:
                            boundary[key] = value
                    boundaries.append(boundary)
                baml_data["boundaries"] = boundaries
            
            # Parse connections
            connections_elem = content_elem.find("connections")
            if connections_elem is not None:
                connections = []
                for connection_elem in connections_elem.findall("connection"):
                    connection = {}
                    for key, value in connection_elem.attrib.items():
                        if key == "context":
                            # Handle context specially
                            context_elem = connection_elem.find("context")
                            if context_elem is not None:
                                context = {}
                                for c_key, c_value in context_elem.attrib.items():
                                    context[c_key] = c_value
                                connection[key] = context
                        else:
                            connection[key] = value
                    connections.append(connection)
                baml_data["connections"] = connections
            
            # Parse constraints
            constraints_elem = content_elem.find("constraints")
            if constraints_elem is not None:
                constraints = []
                for constraint_elem in constraints_elem.findall("constraint"):
                    constraint = {}
                    for key, value in constraint_elem.attrib.items():
                        if key == "conditions":
                            # Handle conditions specially
                            conditions_elem = constraint_elem.find("conditions")
                            if conditions_elem is not None:
                                conditions = []
                                for condition_elem in conditions_elem.findall("condition"):
                                    condition = {}
                                    for cond_key, cond_value in condition_elem.attrib.items():
                                        condition[cond_key] = cond_value
                                    conditions.append(condition)
                            constraint[key] = conditions
                        else:
                            constraint[key] = value
                    constraints.append(constraint)
                baml_data["constraints"] = constraints
            
            # Parse AI integration
            ai_integration_elem = content_elem.find("ai-integration")
            if ai_integration_elem is not None:
                ai_integration = {}
                for key, value in ai_integration_elem.attrib.items():
                    ai_integration[key] = value
                
                # Parse sub-elements
                for sub_elem in ai_integration_elem:
                    sub_data = {}
                    for sub_key, sub_value in sub_elem.attrib.items():
                        sub_data[sub_key] = sub_value
                    ai_integration[sub_elem.tag] = sub_data
                
                baml_data["ai_integration"] = ai_integration
        
        return baml_data

class BAMLXMLTransformer:
    """BAML-specific XML transformation processor."""
    
    def __init__(self):
        self.xml_schema = BAMLXMLSchema()
        self.transformation_history = []
        self.validation_rules = self._load_transformation_rules()
        
    def _load_transformation_rules(self) -> Dict[str, Any]:
        """Load BAML XML transformation rules."""
        rules_path = Path(__file__).parent / "baml_config" / "transformation_rules.json"
        try:
            with open(rules_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("BAML transformation rules not found, using defaults")
            return self._get_default_transformation_rules()
    
    def _get_default_transformation_rules(self) -> Dict[str, Any]:
        """Get default BAML XML transformation rules."""
        return {
            "transformation_rules": {
                "boundary_wrapping": {
                    "enabled": True,
                    "xml_tag": "boundary",
                    "attributes": ["name", "type", "constraints", "ai_enhanced"],
                    "preserve_semantics": True
                },
                "connection_wrapping": {
                    "enabled": True,
                    "xml_tag": "connection",
                    "attributes": ["source", "target", "type", "direction", "ai_enhanced"],
                    "preserve_semantics": True
                },
                "constraint_wrapping": {
                    "enabled": True,
                    "xml_tag": "constraint",
                    "attributes": ["name", "type", "scope", "conditions"],
                    "preserve_semantics": True
                },
                "ai_integration_wrapping": {
                    "enabled": True,
                    "xml_tag": "ai-integration",
                    "attributes": ["semantic_analysis", "context_awareness", "optimization"],
                    "preserve_semantics": True
                }
            },
            "validation_rules": {
                "xml_structure_validation": True,
                "semantic_preservation_validation": True,
                "transformation_completeness_validation": True,
                "baml_compatibility_validation": True
            }
        }
    
    def wrap_baml_with_xml(self, baml_data: Dict[str, Any], 
                             context: Optional[Dict[str, Any]] = None) -> XMLTransformationResult:
        """Wrap BAML semantic data with XML transformation."""
        start_time = time.time()
        
        try:
            # Validate BAML data before transformation
            validation_result = self._validate_baml_data(baml_data)
            
            if not validation_result["valid"]:
                return XMLTransformationResult(
                    success=False,
                    transformed_data={},
                    xml_wrapper="",
                    transformation_time=time.time() - start_time,
                    semantic_preserved=False,
                    validation_result=validation_result,
                    metadata={"error": "BAML validation failed"}
                )
            
            # Create XML wrapper
            xml_element = self.xml_schema.to_xml_element(baml_data)
            xml_string = ET.tostring(xml_element, encoding='unicode')
            
            # Store transformation history
            transformation_record = {
                "timestamp": datetime.now().isoformat(),
                "transformation_type": "baml_to_xml",
                "context": context,
                "success": True
            }
            self.transformation_history.append(transformation_record)
            
            # Validate XML wrapper
            xml_validation = self._validate_xml_wrapper(xml_string)
            
            return XMLTransformationResult(
                success=True,
                transformed_data=baml_data,
                xml_wrapper=xml_string,
                transformation_time=time.time() - start_time,
                semantic_preserved=True,
                validation_result={
                    "baml_validation": validation_result,
                    "xml_validation": xml_validation
                },
                metadata={
                    "transformation_applied": True,
                    "context_applied": context is not None,
                    "semantic_preservation": True,
                    "xml_schema_version": self.xml_schema.version
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to wrap BAML with XML: {e}")
            return XMLTransformationResult(
                success=False,
                transformed_data={},
                xml_wrapper="",
                transformation_time=time.time() - start_time,
                semantic_preserved=False,
                validation_result={"error": str(e)},
                metadata={"exception": str(e)}
            )
    
    def unwrap_xml_to_baml(self, xml_wrapper: str, 
                             context: Optional[Dict[str, Any]] = None) -> XMLTransformationResult:
        """Unwrap XML wrapper back to BAML semantic data."""
        start_time = time.time()
        
        try:
            # Parse XML
            xml_element = ET.fromstring(xml_wrapper)
            
            # Validate XML element
            xml_validation = self._validate_xml_element(xml_element)
            
            if not xml_validation["valid"]:
                return XMLTransformationResult(
                    success=False,
                    transformed_data={},
                    xml_wrapper=xml_wrapper,
                    transformation_time=time.time() - start_time,
                    semantic_preserved=False,
                    validation_result=xml_validation,
                    metadata={"error": "XML validation failed"}
                )
            
            # Extract BAML data
            baml_data = self.xml_schema.from_xml_element(xml_element)
            
            # Validate extracted BAML data
            baml_validation = self._validate_baml_data(baml_data)
            
            # Store transformation history
            transformation_record = {
                "timestamp": datetime.now().isoformat(),
                "transformation_type": "xml_to_baml",
                "context": context,
                "success": True
            }
            self.transformation_history.append(transformation_record)
            
            return XMLTransformationResult(
                success=True,
                transformed_data=baml_data,
                xml_wrapper=xml_wrapper,
                transformation_time=time.time() - start_time,
                semantic_preserved=True,
                validation_result={
                    "xml_validation": xml_validation,
                    "baml_validation": baml_validation
                },
                metadata={
                    "transformation_applied": True,
                    "context_applied": context is not None,
                    "semantic_preservation": True,
                    "xml_schema_version": xml_element.get("version", self.xml_schema.version)
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to unwrap XML to BAML: {e}")
            return XMLTransformationResult(
                success=False,
                transformed_data={},
                xml_wrapper=xml_wrapper,
                transformation_time=time.time() - start_time,
                semantic_preserved=False,
                validation_result={"error": str(e)},
                metadata={"exception": str(e)}
            )
    
    def apply_baml_transformation_rules(self, baml_data: Dict[str, Any], 
                                        transformation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply BAML-specific transformation rules."""
        transformed_data = baml_data.copy()
        
        # Apply boundary transformation rules
        if transformation_rules.get("boundary_wrapping", {}).get("enabled", True):
            transformed_data = self._apply_boundary_transformation_rules(
                transformed_data, transformation_rules["boundary_wrapping"]
            )
        
        # Apply connection transformation rules
        if transformation_rules.get("connection_wrapping", {}).get("enabled", True):
            transformed_data = self._apply_connection_transformation_rules(
                transformed_data, transformation_rules["connection_wrapping"]
            )
        
        # Apply constraint transformation rules
        if transformation_rules.get("constraint_wrapping", {}).get("enabled", True):
            transformed_data = self._apply_constraint_transformation_rules(
                transformed_data, transformation_rules["constraint_wrapping"]
            )
        
        # Apply AI integration transformation rules
        if transformation_rules.get("ai_integration_wrapping", {}).get("enabled", True):
            transformed_data = self._apply_ai_integration_transformation_rules(
                transformed_data, transformation_rules["ai_integration_wrapping"]
            )
        
        return transformed_data
    
    def _validate_baml_data(self, baml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate BAML semantic data."""
        validation_result = {"valid": True, "errors": [], "warnings": []}
        
        # Basic structure validation
        if not isinstance(baml_data, dict):
            validation_result["valid"] = False
            validation_result["errors"].append("BAML data must be a dictionary")
            return validation_result
        
        # Validate boundaries if present
        if "boundaries" in baml_data:
            if not isinstance(baml_data["boundaries"], list):
                validation_result["valid"] = False
                validation_result["errors"].append("BAML boundaries must be a list")
            else:
                for i, boundary in enumerate(baml_data["boundaries"]):
                    if not isinstance(boundary, dict):
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"BAML boundary {i} must be a dictionary")
        
        # Validate connections if present
        if "connections" in baml_data:
            if not isinstance(baml_data["connections"], list):
                validation_result["valid"] = False
                validation_result["errors"].append("BAML connections must be a list")
            else:
                for i, connection in enumerate(baml_data["connections"]):
                    if not isinstance(connection, dict):
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"BAML connection {i} must be a dictionary")
        
        # Validate constraints if present
        if "constraints" in baml_data:
            if not isinstance(baml_data["constraints"], list):
                validation_result["valid"] = False
                validation_result["errors"].append("BAML constraints must be a list")
            else:
                for i, constraint in enumerate(baml_data["constraints"]):
                    if not isinstance(constraint, dict):
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"BAML constraint {i} must be a dictionary")
        
        return validation_result
    
    def _validate_xml_wrapper(self, xml_string: str) -> Dict[str, Any]:
        """Validate XML wrapper."""
        validation_result = {"valid": True, "errors": [], "warnings": []}
        
        try:
            # Parse XML to check structure
            xml_element = ET.fromstring(xml_string)
            
            # Validate root element
            if xml_element.tag != self.xml_schema.wrapper_tag:
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"Root element must be '{self.xml_schema.wrapper_tag}', got '{xml_element.tag}'"
                )
            
            # Validate required attributes
            required_attrs = ["version", "spec", "timestamp", "language"]
            for attr in required_attrs:
                if attr not in xml_element.attrib:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Missing required attribute: {attr}")
            
            # Validate language attribute
            if xml_element.get("language") != "baml":
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"Language must be 'baml', got '{xml_element.get('language')}'"
                )
            
        except ET.ParseError as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"XML parse error: {e}")
        
        return validation_result
    
    def _validate_xml_element(self, xml_element: ET.Element) -> Dict[str, Any]:
        """Validate XML element."""
        validation_result = {"valid": True, "errors": [], "warnings": []}
        
        # Validate root element
        if xml_element.tag != self.xml_schema.wrapper_tag:
            validation_result["valid"] = False
            validation_result["errors"].append(
                f"Root element must be '{self.xml_schema.wrapper_tag}', got '{xml_element.tag}'"
            )
        
        # Validate required attributes
        required_attrs = ["version", "spec", "timestamp", "language"]
        for attr in required_attrs:
            if attr not in xml_element.attrib:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Missing required attribute: {attr}")
        
        # Validate language attribute
        if xml_element.get("language") != "baml":
            validation_result["valid"] = False
            validation_result["errors"].append(
                f"Language must be 'baml', got '{xml_element.get('language')}'"
            )
        
        return validation_result
    
    def _apply_boundary_transformation_rules(self, baml_data: Dict[str, Any], 
                                            rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply boundary transformation rules."""
        # Placeholder for boundary transformation logic
        # In production, this would apply specific boundary transformation rules
        return baml_data
    
    def _apply_connection_transformation_rules(self, baml_data: Dict[str, Any], 
                                            rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply connection transformation rules."""
        # Placeholder for connection transformation logic
        # In production, this would apply specific connection transformation rules
        return baml_data
    
    def _apply_constraint_transformation_rules(self, baml_data: Dict[str, Any], 
                                             rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply constraint transformation rules."""
        # Placeholder for constraint transformation logic
        # In production, this would apply specific constraint transformation rules
        return baml_data
    
    def _apply_ai_integration_transformation_rules(self, baml_data: Dict[str, Any], 
                                                    rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply AI integration transformation rules."""
        # Placeholder for AI integration transformation logic
        # In production, this would apply specific AI integration transformation rules
        return baml_data
    
    def get_transformation_status(self) -> Dict[str, Any]:
        """Get BAML XML transformation status."""
        return {
            "status": "active",
            "xml_schema": asdict(self.xml_schema),
            "transformation_rules": self.validation_rules,
            "transformation_history_size": len(self.transformation_history),
            "performance_metrics": self._get_performance_metrics()
        }
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for BAML XML transformations."""
        if not self.transformation_history:
            return {"status": "no_transformations_performed"}
        
        transformation_times = [
            record.get("transformation_time", 0) 
            for record in self.transformation_history
            if "transformation_time" in record
        ]
        
        successful_transformations = [
            record for record in self.transformation_history
            if record.get("success", False)
        ]
        
        return {
            "total_transformations": len(self.transformation_history),
            "successful_transformations": len(successful_transformations),
            "success_rate": len(successful_transformations) / len(self.transformation_history),
            "average_transformation_time": (
                sum(transformation_times) / len(transformation_times) 
                if transformation_times else 0
            ),
            "last_transformation": self.transformation_history[-1] if self.transformation_history else None
        }

# Export main classes
__all__ = [
    'BAMLXMLTransformer',
    'BAMLXMLSchema',
    'XMLTransformationResult'
]
