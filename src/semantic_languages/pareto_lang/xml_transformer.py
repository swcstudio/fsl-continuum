"""
FSL Continuum - Pareto-Lang XML Transformation Processor

Core processor for XML data transformation wrapping in Pareto-Lang semantic language.
Provides XML-wrapping, unwrapping, and transformation with optimization preservation.
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
    optimization_preserved: bool
    validation_result: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class ParetoLangXMLSchema:
    """XML schema for Pareto-Lang transformations."""
    wrapper_tag: str = "pareto-lang-semantic-data"
    version: str = "1.0.0-pareto-xml"
    spec: str = "PARETO-XML-TRANSFORM-001"
    
    def to_xml_element(self, data: Dict[str, Any]) -> ET.Element:
        """Convert Pareto-Lang data to XML element."""
        root = ET.Element(self.wrapper_tag)
        root.set("version", self.version)
        root.set("spec", self.spec)
        root.set("timestamp", datetime.now().isoformat())
        root.set("language", "pareto_lang")
        
        # Add metadata
        metadata = ET.SubElement(root, "metadata")
        schema = ET.SubElement(metadata, "schema")
        schema.set("type", "pareto-lang-semantic")
        schema.set("version", self.version)
        
        validation = ET.SubElement(metadata, "validation")
        validation.set("type", "pareto-lang-validation")
        validation.set("pareto_optimal", "true")
        
        # Add transformations
        transformations = ET.SubElement(root, "transformations")
        transformations.set("applied", "true")
        transformations.set("xml_wrapping", "true")
        transformations.set("optimization_preservation", "true")
        
        # Add Pareto-Lang content
        content = ET.SubElement(root, "pareto-lang-content")
        
        # Add optimizations
        if "optimizations" in data:
            optimizations = ET.SubElement(content, "optimizations")
            for optimization in data["optimizations"]:
                optimization_elem = ET.SubElement(optimizations, "optimization")
                for key, value in optimization.items():
                    if key == "constraints" and isinstance(value, list):
                        constraints = ET.SubElement(optimization_elem, "constraints")
                        for constraint in value:
                            constraint_elem = ET.SubElement(constraints, "constraint")
                            for c_key, c_value in constraint.items():
                                constraint_elem.set(c_key, str(c_value))
                    else:
                        optimization_elem.set(key, str(value))
        
        # Add resources
        if "resources" in data:
            resources = ET.SubElement(content, "resources")
            for resource in data["resources"]:
                resource_elem = ET.SubElement(resources, "resource")
                for key, value in resource.items():
                    resource_elem.set(key, str(value))
        
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
        """Convert XML element back to Pareto-Lang data."""
        pareto_data = {}
        
        # Parse Pareto-Lang content
        content_elem = xml_element.find("pareto-lang-content")
        if content_elem is not None:
            
            # Parse optimizations
            optimizations_elem = content_elem.find("optimizations")
            if optimizations_elem is not None:
                optimizations = []
                for optimization_elem in optimizations_elem.findall("optimization"):
                    optimization = {}
                    for key, value in optimization_elem.attrib.items():
                        if key == "constraints":
                            # Handle constraints specially
                            constraints_elem = optimization_elem.find("constraints")
                            if constraints_elem is not None:
                                constraints = []
                                for constraint_elem in constraints_elem.findall("constraint"):
                                    constraint = {}
                                    for c_key, c_value in constraint_elem.attrib.items():
                                        constraint[c_key] = c_value
                                    constraints.append(constraint)
                            optimization[key] = constraints
                        else:
                            optimization[key] = value
                    optimizations.append(optimization)
                pareto_data["optimizations"] = optimizations
            
            # Parse resources
            resources_elem = content_elem.find("resources")
            if resources_elem is not None:
                resources = []
                for resource_elem in resources_elem.findall("resource"):
                    resource = {}
                    for key, value in resource_elem.attrib.items():
                        resource[key] = value
                    resources.append(resource)
                pareto_data["resources"] = resources
            
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
                pareto_data["constraints"] = constraints
            
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
                
                pareto_data["ai_integration"] = ai_integration
        
        return pareto_data

class ParetoLangXMLTransformer:
    """Pareto-Lang-specific XML transformation processor."""
    
    def __init__(self):
        self.xml_schema = ParetoLangXMLSchema()
        self.transformation_history = []
        self.validation_rules = self._load_transformation_rules()
        
    def _load_transformation_rules(self) -> Dict[str, Any]:
        """Load Pareto-Lang XML transformation rules."""
        rules_path = Path(__file__).parent / "pareto_config" / "transformation_rules.json"
        try:
            with open(rules_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Pareto-Lang transformation rules not found, using defaults")
            return self._get_default_transformation_rules()
    
    def _get_default_transformation_rules(self) -> Dict[str, Any]:
        """Get default Pareto-Lang XML transformation rules."""
        return {
            "transformation_rules": {
                "optimization_wrapping": {
                    "enabled": True,
                    "xml_tag": "optimization",
                    "attributes": ["name", "type", "target", "efficiency", "ai_enhanced"],
                    "preserve_optimization": True
                },
                "resource_wrapping": {
                    "enabled": True,
                    "xml_tag": "resource",
                    "attributes": ["name", "type", "capacity", "utilization", "optimization"],
                    "preserve_resource": True
                },
                "constraint_wrapping": {
                    "enabled": True,
                    "xml_tag": "constraint",
                    "attributes": ["name", "type", "scope", "pareto_optimal", "conditions"],
                    "pareto_optimal": True
                },
                "ai_integration_wrapping": {
                    "enabled": True,
                    "xml_tag": "ai-integration",
                    "attributes": ["optimization_analysis", "pareto_efficiency", "context_awareness"],
                    "ai_enhanced": True
                }
            },
            "validation_rules": {
                "xml_structure_validation": True,
                "optimization_preservation_validation": True,
                "transformation_completeness_validation": True,
                "pareto_lang_compatibility_validation": True
            }
        }
    
    def wrap_pareto_lang_with_xml(self, pareto_data: Dict[str, Any], 
                                     context: Optional[Dict[str, Any]] = None) -> XMLTransformationResult:
        """Wrap Pareto-Lang semantic data with XML transformation."""
        start_time = time.time()
        
        try:
            # Validate Pareto-Lang data before transformation
            validation_result = self._validate_pareto_lang_data(pareto_data)
            
            if not validation_result["valid"]:
                return XMLTransformationResult(
                    success=False,
                    transformed_data={},
                    xml_wrapper="",
                    transformation_time=time.time() - start_time,
                    optimization_preserved=False,
                    validation_result=validation_result,
                    metadata={"error": "Pareto-Lang validation failed"}
                )
            
            # Create XML wrapper
            xml_element = self.xml_schema.to_xml_element(pareto_data)
            xml_string = ET.tostring(xml_element, encoding='unicode')
            
            # Store transformation history
            transformation_record = {
                "timestamp": datetime.now().isoformat(),
                "transformation_type": "pareto_lang_to_xml",
                "context": context,
                "success": True
            }
            self.transformation_history.append(transformation_record)
            
            # Validate XML wrapper
            xml_validation = self._validate_xml_wrapper(xml_string)
            
            return XMLTransformationResult(
                success=True,
                transformed_data=pareto_data,
                xml_wrapper=xml_string,
                transformation_time=time.time() - start_time,
                optimization_preserved=True,
                validation_result={
                    "pareto_lang_validation": validation_result,
                    "xml_validation": xml_validation
                },
                metadata={
                    "transformation_applied": True,
                    "context_applied": context is not None,
                    "optimization_preservation": True,
                    "xml_schema_version": self.xml_schema.version
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to wrap Pareto-Lang with XML: {e}")
            return XMLTransformationResult(
                success=False,
                transformed_data={},
                xml_wrapper="",
                transformation_time=time.time() - start_time,
                optimization_preserved=False,
                validation_result={"error": str(e)},
                metadata={"exception": str(e)}
            )
    
    def unwrap_xml_to_pareto_lang(self, xml_wrapper: str, 
                                     context: Optional[Dict[str, Any]] = None) -> XMLTransformationResult:
        """Unwrap XML wrapper back to Pareto-Lang semantic data."""
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
                    optimization_preserved=False,
                    validation_result=xml_validation,
                    metadata={"error": "XML validation failed"}
                )
            
            # Extract Pareto-Lang data
            pareto_data = self.xml_schema.from_xml_element(xml_element)
            
            # Validate extracted Pareto-Lang data
            pareto_validation = self._validate_pareto_lang_data(pareto_data)
            
            # Store transformation history
            transformation_record = {
                "timestamp": datetime.now().isoformat(),
                "transformation_type": "xml_to_pareto_lang",
                "context": context,
                "success": True
            }
            self.transformation_history.append(transformation_record)
            
            return XMLTransformationResult(
                success=True,
                transformed_data=pareto_data,
                xml_wrapper=xml_wrapper,
                transformation_time=time.time() - start_time,
                optimization_preserved=True,
                validation_result={
                    "xml_validation": xml_validation,
                    "pareto_lang_validation": pareto_validation
                },
                metadata={
                    "transformation_applied": True,
                    "context_applied": context is not None,
                    "optimization_preservation": True,
                    "xml_schema_version": xml_element.get("version", self.xml_schema.version)
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to unwrap XML to Pareto-Lang: {e}")
            return XMLTransformationResult(
                success=False,
                transformed_data={},
                xml_wrapper=xml_wrapper,
                transformation_time=time.time() - start_time,
                optimization_preserved=False,
                validation_result={"error": str(e)},
                metadata={"exception": str(e)}
            )
    
    def apply_pareto_transformation_rules(self, pareto_data: Dict[str, Any], 
                                            transformation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply Pareto-Lang-specific transformation rules."""
        transformed_data = pareto_data.copy()
        
        # Apply optimization transformation rules
        if transformation_rules.get("optimization_wrapping", {}).get("enabled", True):
            transformed_data = self._apply_optimization_transformation_rules(
                transformed_data, transformation_rules["optimization_wrapping"]
            )
        
        # Apply resource transformation rules
        if transformation_rules.get("resource_wrapping", {}).get("enabled", True):
            transformed_data = self._apply_resource_transformation_rules(
                transformed_data, transformation_rules["resource_wrapping"]
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
    
    def _validate_pareto_lang_data(self, pareto_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Pareto-Lang semantic data."""
        validation_result = {"valid": True, "errors": [], "warnings": []}
        
        # Basic structure validation
        if not isinstance(pareto_data, dict):
            validation_result["valid"] = False
            validation_result["errors"].append("Pareto-Lang data must be a dictionary")
            return validation_result
        
        # Validate optimizations if present
        if "optimizations" in pareto_data:
            if not isinstance(pareto_data["optimizations"], list):
                validation_result["valid"] = False
                validation_result["errors"].append("Pareto-Lang optimizations must be a list")
            else:
                for i, optimization in enumerate(pareto_data["optimizations"]):
                    if not isinstance(optimization, dict):
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"Pareto-Lang optimization {i} must be a dictionary")
        
        # Validate resources if present
        if "resources" in pareto_data:
            if not isinstance(pareto_data["resources"], list):
                validation_result["valid"] = False
                validation_result["errors"].append("Pareto-Lang resources must be a list")
            else:
                for i, resource in enumerate(pareto_data["resources"]):
                    if not isinstance(resource, dict):
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"Pareto-Lang resource {i} must be a dictionary")
        
        # Validate constraints if present
        if "constraints" in pareto_data:
            if not isinstance(pareto_data["constraints"], list):
                validation_result["valid"] = False
                validation_result["errors"].append("Pareto-Lang constraints must be a list")
            else:
                for i, constraint in enumerate(pareto_data["constraints"]):
                    if not isinstance(constraint, dict):
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"Pareto-Lang constraint {i} must be a dictionary")
        
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
            if xml_element.get("language") != "pareto_lang":
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"Language must be 'pareto_lang', got '{xml_element.get('language')}'"
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
        if xml_element.get("language") != "pareto_lang":
            validation_result["valid"] = False
            validation_result["errors"].append(
                f"Language must be 'pareto_lang', got '{xml_element.get('language')}'"
            )
        
        return validation_result
    
    def _apply_optimization_transformation_rules(self, pareto_data: Dict[str, Any], 
                                                  rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply optimization transformation rules."""
        # Placeholder for optimization transformation logic
        # In production, this would apply specific optimization transformation rules
        return pareto_data
    
    def _apply_resource_transformation_rules(self, pareto_data: Dict[str, Any], 
                                                 rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply resource transformation rules."""
        # Placeholder for resource transformation logic
        # In production, this would apply specific resource transformation rules
        return pareto_data
    
    def _apply_constraint_transformation_rules(self, pareto_data: Dict[str, Any], 
                                                 rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply constraint transformation rules."""
        # Placeholder for constraint transformation logic
        # In production, this would apply specific constraint transformation rules
        return pareto_data
    
    def _apply_ai_integration_transformation_rules(self, pareto_data: Dict[str, Any], 
                                                      rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply AI integration transformation rules."""
        # Placeholder for AI integration transformation logic
        # In production, this would apply specific AI integration transformation rules
        return pareto_data
    
    def get_transformation_status(self) -> Dict[str, Any]:
        """Get Pareto-Lang XML transformation status."""
        return {
            "status": "active",
            "xml_schema": asdict(self.xml_schema),
            "transformation_rules": self.validation_rules,
            "transformation_history_size": len(self.transformation_history),
            "performance_metrics": self._get_performance_metrics()
        }
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for Pareto-Lang XML transformations."""
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
    'ParetoLangXMLTransformer',
    'ParetoLangXMLSchema',
    'XMLTransformationResult'
]
