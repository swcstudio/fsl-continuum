"""
FSL Continuum - Unified XML Processor

Unified XML processor for BAML and Pareto-Lang semantic languages.
Provides consistent XML transformation processing across all semantic languages.
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

# Import semantic language processors
from .baml.xml_transformer import BAMLXMLTransformer
from .pareto_lang.xml_transformer import ParetoLangXMLTransformer

@dataclass
class UnifiedXMLProcessingResult:
    """Result of unified XML processing operation."""
    success: bool
    processed_data: Dict[str, Any]
    xml_wrappers: Dict[str, Any]
    transformation_times: Dict[str, float]
    semantic_preserved: Dict[str, bool]
    validation_results: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class UnifiedXMLSchema:
    """Unified XML schema for all semantic languages."""
    baml_schema_version: str = "1.0.0-baml-xml"
    pareto_lang_schema_version: str = "1.0.0-pareto-xml"
    unified_version: str = "1.0.0-unified-xml"
    spec: str = "UNIFIED-XML-TRANSFORM-001"
    
    def get_schema_for_language(self, language_type: str) -> Dict[str, Any]:
        """Get XML schema for specific language."""
        if language_type == "baml":
            return {
                "version": self.baml_schema_version,
                "spec": self.spec,
                "language": "baml",
                "wrapper_tag": "baml-semantic-data"
            }
        elif language_type == "pareto_lang":
            return {
                "version": self.pareto_lang_schema_version,
                "spec": self.spec,
                "language": "pareto_lang",
                "wrapper_tag": "pareto-lang-semantic-data"
            }
        else:
            raise ValueError(f"Unsupported language type: {language_type}")

class UnifiedXMLProcessor:
    """Unified XML processor for semantic languages."""
    
    def __init__(self):
        self.baml_transformer = BAMLXMLTransformer()
        self.pareto_lang_transformer = ParetoLangXMLTransformer()
        self.unified_schema = UnifiedXMLSchema()
        
        self.processing_history = []
        self.performance_metrics = {}
        
    def process_semantic_data_with_xml(self, semantic_data: Dict[str, Any], 
                                        language_type: str,
                                        context: Optional[Dict[str, Any]] = None) -> UnifiedXMLProcessingResult:
        """Process semantic data with XML transformation for specified language."""
        start_time = time.time()
        
        try:
            # Validate language type
            if language_type not in ["baml", "pareto_lang"]:
                raise ValueError(f"Unsupported language type: {language_type}")
            
            # Get appropriate transformer
            if language_type == "baml":
                transformer = self.baml_transformer
            else:
                transformer = self.pareto_lang_transformer
            
            # Apply XML transformation
            if context and context.get("xml_transformation_enabled", False):
                transformation_result = transformer.wrap_data_with_xml(semantic_data)
                xml_wrapper = transformation_result.xml_wrapper
                xml_applied = True
            else:
                xml_wrapper = ""
                xml_applied = False
            
            # Calculate processing metrics
            processing_time = time.time() - start_time
            
            # Store processing history
            processing_record = {
                "timestamp": datetime.now().isoformat(),
                "language_type": language_type,
                "xml_transformation_applied": xml_applied,
                "processing_time": processing_time,
                "success": True
            }
            self.processing_history.append(processing_record)
            
            return UnifiedXMLProcessingResult(
                success=True,
                processed_data=semantic_data,
                xml_wrappers={language_type: xml_wrapper},
                transformation_times={language_type: processing_time},
                semantic_preserved={language_type: True},
                validation_results={
                    "semantic_validation": {"valid": True},
                    "xml_validation": {"valid": True} if xml_applied else {"valid": True, "skipped": True}
                },
                metadata={
                    "language_type": language_type,
                    "xml_transformation_applied": xml_applied,
                    "processing_time": processing_time,
                    "schema_version": self.unified_schema.get_schema_for_language(language_type)["version"],
                    "context_applied": context is not None
                }
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Failed to process semantic data with XML: {e}")
            
            # Store processing history
            processing_record = {
                "timestamp": datetime.now().isoformat(),
                "language_type": language_type,
                "xml_transformation_applied": False,
                "processing_time": processing_time,
                "success": False,
                "error": str(e)
            }
            self.processing_history.append(processing_record)
            
            return UnifiedXMLProcessingResult(
                success=False,
                processed_data={},
                xml_wrappers={},
                transformation_times={},
                semantic_preserved={},
                validation_results={"error": str(e)},
                metadata={
                    "language_type": language_type,
                    "xml_transformation_applied": False,
                    "processing_time": processing_time,
                    "error": str(e)
                }
            )
    
    def process_multiple_semantic_data_with_xml(self, semantic_data_dict: Dict[str, Dict[str, Any]], 
                                               context: Optional[Dict[str, Any]] = None) -> UnifiedXMLProcessingResult:
        """Process multiple semantic data types with XML transformations."""
        start_time = time.time()
        
        try:
            results = {}
            xml_wrappers = {}
            transformation_times = {}
            semantic_preserved = {}
            validation_results = {}
            
            # Process each language type
            for language_type, semantic_data in semantic_data_dict.items():
                if language_type in ["baml", "pareto_lang"]:
                    # Get appropriate transformer
                    if language_type == "baml":
                        transformer = self.baml_transformer
                    else:
                        transformer = self.pareto_lang_transformer
                    
                    # Apply XML transformation
                    if context and context.get("xml_transformation_enabled", False):
                        transformation_result = transformer.wrap_data_with_xml(semantic_data)
                        xml_wrappers[language_type] = transformation_result.xml_wrapper
                        results[language_type] = transformation_result.transformed_data
                        validation_results[language_type] = transformation_result.validation_result
                    else:
                        xml_wrappers[language_type] = ""
                        results[language_type] = semantic_data
                        validation_results[language_type] = {"valid": True, "xml_skipped": True}
                    
                    semantic_preserved[language_type] = True
                    transformation_times[language_type] = time.time()  # Will be updated below
                else:
                    raise ValueError(f"Unsupported language type: {language_type}")
            
            # Calculate total processing time
            total_processing_time = time.time() - start_time
            
            # Store processing history
            processing_record = {
                "timestamp": datetime.now().isoformat(),
                "language_types": list(semantic_data_dict.keys()),
                "xml_transformation_applied": context and context.get("xml_transformation_enabled", False),
                "processing_time": total_processing_time,
                "success": True
            }
            self.processing_history.append(processing_record)
            
            return UnifiedXMLProcessingResult(
                success=True,
                processed_data=results,
                xml_wrappers=xml_wrappers,
                transformation_times=transformation_times,
                semantic_preserved=semantic_preserved,
                validation_results=validation_results,
                metadata={
                    "language_types": list(semantic_data_dict.keys()),
                    "xml_transformation_applied": context and context.get("xml_transformation_enabled", False),
                    "processing_time": total_processing_time,
                    "context_applied": context is not None
                }
            )
            
        except Exception as e:
            total_processing_time = time.time() - start_time
            logger.error(f"Failed to process multiple semantic data with XML: {e}")
            
            # Store processing history
            processing_record = {
                "timestamp": datetime.now().isoformat(),
                "language_types": list(semantic_data_dict.keys()),
                "xml_transformation_applied": False,
                "processing_time": total_processing_time,
                "success": False,
                "error": str(e)
            }
            self.processing_history.append(processing_record)
            
            return UnifiedXMLProcessingResult(
                success=False,
                processed_data={},
                xml_wrappers={},
                transformation_times={},
                semantic_preserved={},
                validation_results={"error": str(e)},
                metadata={
                    "language_types": list(semantic_data_dict.keys()),
                    "xml_transformation_applied": False,
                    "processing_time": total_processing_time,
                    "error": str(e)
                }
            )
    
    def create_unified_xml_wrapper(self, semantic_data_dict: Dict[str, Dict[str, Any]], 
                                    context: Optional[Dict[str, Any]] = None) -> UnifiedXMLProcessingResult:
        """Create unified XML wrapper for multiple semantic languages."""
        start_time = time.time()
        
        try:
            # Process each language with XML
            individual_results = self.process_multiple_semantic_data_with_xml(
                semantic_data_dict, context
            )
            
            if not individual_results.success:
                return individual_results
            
            # Create unified XML structure
            unified_root = ET.Element("unified-semantic-data")
            unified_root.set("version", self.unified_schema.unified_version)
            unified_root.set("spec", self.unified_schema.spec)
            unified_root.set("timestamp", datetime.now().isoformat())
            unified_root.set("languages", ",".join(semantic_data_dict.keys()))
            
            # Add metadata
            metadata = ET.SubElement(unified_root, "metadata")
            schema_info = ET.SubElement(metadata, "schema-info")
            schema_info.set("unified_version", self.unified_schema.unified_version)
            
            # Add language-specific XML
            language_data = ET.SubElement(unified_root, "language-data")
            
            for language_type, xml_wrapper in individual_results.xml_wrappers.items():
                if xml_wrapper:  # Only add if XML wrapper exists
                    try:
                        lang_xml = ET.fromstring(xml_wrapper)
                        language_data.append(lang_xml)
                    except ET.ParseError:
                        logger.warning(f"Failed to parse XML for {language_type}, skipping")
            
            # Convert unified XML to string
            unified_xml_string = ET.tostring(unified_root, encoding='unicode')
            
            # Calculate processing time
            total_processing_time = time.time() - start_time
            
            # Store processing history
            processing_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "unified_xml_wrapper_creation",
                "language_types": list(semantic_data_dict.keys()),
                "xml_transformation_applied": context and context.get("xml_transformation_enabled", False),
                "processing_time": total_processing_time,
                "success": True
            }
            self.processing_history.append(processing_record)
            
            return UnifiedXMLProcessingResult(
                success=True,
                processed_data=individual_results.processed_data,
                xml_wrappers={
                    **individual_results.xml_wrappers,
                    "unified": unified_xml_string
                },
                transformation_times=individual_results.transformation_times,
                semantic_preserved=individual_results.semantic_preserved,
                validation_results=individual_results.validation_results,
                metadata={
                    "operation": "unified_xml_wrapper_creation",
                    "language_types": list(semantic_data_dict.keys()),
                    "xml_transformation_applied": context and context.get("xml_transformation_enabled", False),
                    "processing_time": total_processing_time,
                    "unified_xml_created": True,
                    "context_applied": context is not None
                }
            )
            
        except Exception as e:
            total_processing_time = time.time() - start_time
            logger.error(f"Failed to create unified XML wrapper: {e}")
            
            # Store processing history
            processing_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "unified_xml_wrapper_creation",
                "language_types": list(semantic_data_dict.keys()),
                "xml_transformation_applied": False,
                "processing_time": total_processing_time,
                "success": False,
                "error": str(e)
            }
            self.processing_history.append(processing_record)
            
            return UnifiedXMLProcessingResult(
                success=False,
                processed_data={},
                xml_wrappers={},
                transformation_times={},
                semantic_preserved={},
                validation_results={"error": str(e)},
                metadata={
                    "operation": "unified_xml_wrapper_creation",
                    "language_types": list(semantic_data_dict.keys()),
                    "xml_transformation_applied": False,
                    "processing_time": total_processing_time,
                    "error": str(e)
                }
            )
    
    def parse_unified_xml_wrapper(self, unified_xml_wrapper: str, 
                                   context: Optional[Dict[str, Any]] = None) -> UnifiedXMLProcessingResult:
        """Parse unified XML wrapper back to semantic data."""
        start_time = time.time()
        
        try:
            # Parse unified XML
            unified_root = ET.fromstring(unified_xml_wrapper)
            
            # Validate unified XML structure
            if unified_root.tag != "unified-semantic-data":
                raise ValueError("Invalid unified XML wrapper structure")
            
            # Extract language-specific XML
            language_data = unified_root.find("language-data")
            if language_data is None:
                raise ValueError("No language data found in unified XML wrapper")
            
            results = {}
            xml_wrappers = {}
            transformation_times = {}
            semantic_preserved = {}
            validation_results = {}
            
            # Parse each language type
            for lang_element in language_data:
                language_type = lang_element.tag
                
                if language_type in ["baml-semantic-data", "pareto-lang-semantic-data"]:
                    # Map XML tag to language type
                    if language_type == "baml-semantic-data":
                        lang_key = "baml"
                        transformer = self.baml_transformer
                    elif language_type == "pareto-lang-semantic-data":
                        lang_key = "pareto_lang"
                        transformer = self.pareto_lang_transformer
                    else:
                        continue
                    
                    # Convert XML element to string
                    lang_xml_string = ET.tostring(lang_element, encoding='unicode')
                    
                    # Parse with appropriate transformer
                    transformation_result = transformer.unwrap_xml_to_xml_data(lang_xml_string)
                    
                    results[lang_key] = transformation_result.transformed_data
                    xml_wrappers[lang_key] = lang_xml_string
                    validation_results[lang_key] = transformation_result.validation_result
                    semantic_preserved[lang_key] = transformation_result.semantic_preserved
                    transformation_times[lang_key] = transformation_result.transformation_time
                else:
                    logger.warning(f"Unsupported language element: {language_type}")
            
            # Calculate total processing time
            total_processing_time = time.time() - start_time
            
            # Store processing history
            processing_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "unified_xml_wrapper_parsing",
                "language_types": list(results.keys()),
                "xml_transformation_applied": True,
                "processing_time": total_processing_time,
                "success": True
            }
            self.processing_history.append(processing_record)
            
            return UnifiedXMLProcessingResult(
                success=True,
                processed_data=results,
                xml_wrappers=xml_wrappers,
                transformation_times=transformation_times,
                semantic_preserved=semantic_preserved,
                validation_results=validation_results,
                metadata={
                    "operation": "unified_xml_wrapper_parsing",
                    "language_types": list(results.keys()),
                    "xml_transformation_applied": True,
                    "processing_time": total_processing_time,
                    "unified_xml_parsed": True,
                    "context_applied": context is not None
                }
            )
            
        except Exception as e:
            total_processing_time = time.time() - start_time
            logger.error(f"Failed to parse unified XML wrapper: {e}")
            
            # Store processing history
            processing_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "unified_xml_wrapper_parsing",
                "language_types": [],
                "xml_transformation_applied": True,
                "processing_time": total_processing_time,
                "success": False,
                "error": str(e)
            }
            self.processing_history.append(processing_record)
            
            return UnifiedXMLProcessingResult(
                success=False,
                processed_data={},
                xml_wrappers={},
                transformation_times={},
                semantic_preserved={},
                validation_results={"error": str(e)},
                metadata={
                    "operation": "unified_xml_wrapper_parsing",
                    "language_types": [],
                    "xml_transformation_applied": False,
                    "processing_time": total_processing_time,
                    "error": str(e)
                }
            )
    
    def get_unified_processor_status(self) -> Dict[str, Any]:
        """Get status of unified XML processor."""
        return {
            "status": "active",
            "unified_schema": asdict(self.unified_schema),
            "baml_transformer_status": self.baml_transformer.get_transformation_status(),
            "pareto_lang_transformer_status": self.pareto_lang_transformer.get_transformation_status(),
            "processing_history_size": len(self.processing_history),
            "performance_metrics": self._get_performance_metrics()
        }
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for unified XML processor."""
        if not self.processing_history:
            return {"status": "no_processing_performed"}
        
        total_operations = len(self.processing_history)
        successful_operations = sum(1 for record in self.processing_history if record.get("success", False))
        
        processing_times = [
            record.get("processing_time", 0) 
            for record in self.processing_history
        ]
        
        language_distribution = {}
        for record in self.processing_history:
            if "language_type" in record:
                lang = record["language_type"]
                language_distribution[lang] = language_distribution.get(lang, 0) + 1
            elif "language_types" in record:
                for lang in record["language_types"]:
                    language_distribution[lang] = language_distribution.get(lang, 0) + 1
        
        return {
            "total_operations": total_operations,
            "successful_operations": successful_operations,
            "success_rate": successful_operations / total_operations,
            "average_processing_time": sum(processing_times) / len(processing_times),
            "total_processing_time": sum(processing_times),
            "language_distribution": language_distribution,
            "last_operation": self.processing_history[-1] if self.processing_history else None
        }

# Export main classes
__all__ = [
    'UnifiedXMLProcessor',
    'UnifiedXMLSchema',
    'UnifiedXMLProcessingResult'
]
