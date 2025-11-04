"""
XML Processing Module

XML transformation, validation, and semantic preservation for
FSL Continuum semantic language operations.
"""

from typing import Dict, Any, List, Optional, Tuple
import re
from datetime import datetime


class XMLProcessor:
    """Core XML processing engine."""
    
    def __init__(self, namespace: str = "https://supercompute.me/xml/context-patterns"):
        self.namespace = namespace
        self.processing_history = []
    
    def process(self, content: Any, operation: str = 'wrap') -> str:
        """Process content with XML operations."""
        if operation == 'wrap':
            return self.wrap(content)
        elif operation == 'unwrap':
            return self.unwrap(str(content))
        return str(content)
    
    def wrap(self, content: Any, tags: Dict[str, str] = None) -> str:
        """Wrap content with XML tags."""
        tags = tags or {}
        tag_name = tags.get('root', 'content')
        attributes = tags.get('attributes', {})
        
        attr_str = ' '.join([f'{k}="{v}"' for k, v in attributes.items()])
        namespace_attr = f'xmlns="{self.namespace}"'
        
        xml = f'<{tag_name} {namespace_attr} {attr_str}>\n'
        xml += f'  <![CDATA[{content}]]>\n'
        xml += f'</{tag_name}>'
        
        self.processing_history.append({
            'operation': 'wrap',
            'timestamp': datetime.now().isoformat()
        })
        
        return xml
    
    def unwrap(self, xml_content: str) -> Any:
        """Unwrap content from XML."""
        # Extract CDATA content
        cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', xml_content, re.DOTALL)
        if cdata_match:
            return cdata_match.group(1)
        
        # Fallback: extract content between tags
        content_match = re.search(r'<\w+[^>]*>(.*?)</\w+>', xml_content, re.DOTALL)
        if content_match:
            return content_match.group(1).strip()
        
        return xml_content
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'total_operations': len(self.processing_history),
            'namespace': self.namespace
        }


class XMLValidator:
    """XML validation engine."""
    
    def __init__(self):
        self.validation_rules = {
            'well_formed': True,
            'namespace_required': True,
            'strict_mode': False
        }
        self.validation_history = []
    
    def validate(self, xml_content: str, strict: bool = False) -> Tuple[bool, List[str]]:
        """Validate XML content."""
        errors = []
        
        # Check well-formedness
        if not self._is_well_formed(xml_content):
            errors.append("XML is not well-formed")
        
        # Check namespace
        if self.validation_rules['namespace_required'] and 'xmlns=' not in xml_content:
            errors.append("Missing namespace declaration")
        
        # Strict mode checks
        if strict:
            strict_errors = self._strict_validation(xml_content)
            errors.extend(strict_errors)
        
        is_valid = len(errors) == 0
        
        self.validation_history.append({
            'timestamp': datetime.now().isoformat(),
            'valid': is_valid,
            'errors': errors
        })
        
        return is_valid, errors
    
    def _is_well_formed(self, xml_content: str) -> bool:
        """Check if XML is well-formed."""
        # Basic well-formedness checks
        open_tags = re.findall(r'<(\w+)[^/>]*>', xml_content)
        close_tags = re.findall(r'</(\w+)>', xml_content)
        
        # Check if tags match
        open_tags = [tag for tag in open_tags if tag not in ['?xml', '!DOCTYPE']]
        
        return len(open_tags) == len(close_tags)
    
    def _strict_validation(self, xml_content: str) -> List[str]:
        """Perform strict validation."""
        errors = []
        
        # Check for proper indentation (basic check)
        lines = xml_content.split('\n')
        if len(lines) > 1 and not any(line.startswith(' ') or line.startswith('\t') for line in lines[1:-1]):
            errors.append("Improper indentation")
        
        return errors
    
    def validate_against_schema(self, xml_content: str, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate XML against a schema."""
        errors = []
        
        # Check required elements
        for element in schema.get('required_elements', []):
            if f'<{element}' not in xml_content:
                errors.append(f"Missing required element: {element}")
        
        # Check forbidden elements
        for element in schema.get('forbidden_elements', []):
            if f'<{element}' in xml_content:
                errors.append(f"Forbidden element present: {element}")
        
        return len(errors) == 0, errors


class XMLTransformer:
    """XML transformation engine."""
    
    def __init__(self):
        self.transformations = []
        self.transformation_cache = {}
    
    def transform(self, xml_content: str, transformation: Dict[str, Any]) -> str:
        """Transform XML content."""
        transform_type = transformation.get('type', 'identity')
        
        if transform_type == 'identity':
            return xml_content
        elif transform_type == 'add_namespace':
            return self._add_namespace(xml_content, transformation.get('namespace', ''))
        elif transform_type == 'remove_namespace':
            return self._remove_namespace(xml_content)
        elif transform_type == 'reformat':
            return self._reformat(xml_content)
        
        return xml_content
    
    def _add_namespace(self, xml_content: str, namespace: str) -> str:
        """Add namespace to XML."""
        # Find first tag and add namespace
        match = re.search(r'<(\w+)([^>]*)>', xml_content)
        if match:
            tag_name, attributes = match.groups()
            new_tag = f'<{tag_name} xmlns="{namespace}"{attributes}>'
            return xml_content.replace(match.group(0), new_tag, 1)
        return xml_content
    
    def _remove_namespace(self, xml_content: str) -> str:
        """Remove namespace from XML."""
        return re.sub(r'\s+xmlns="[^"]*"', '', xml_content)
    
    def _reformat(self, xml_content: str) -> str:
        """Reformat XML for readability."""
        # Basic reformatting - in production use proper XML parser
        return xml_content.strip()
    
    def create_pipeline(self, transformations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a transformation pipeline."""
        pipeline = {
            'id': len(self.transformations),
            'transformations': transformations,
            'created_at': datetime.now().isoformat()
        }
        self.transformations.append(pipeline)
        return pipeline
    
    def execute_pipeline(self, xml_content: str, pipeline_id: int) -> str:
        """Execute a transformation pipeline."""
        if pipeline_id >= len(self.transformations):
            return xml_content
        
        pipeline = self.transformations[pipeline_id]
        result = xml_content
        
        for transformation in pipeline['transformations']:
            result = self.transform(result, transformation)
        
        return result


class XMLSchemaManager:
    """Manage XML schemas."""
    
    def __init__(self):
        self.schemas = {}
        self.default_namespace = "https://supercompute.me/xml/context-patterns"
    
    def create_schema(self, name: str, schema_def: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new XML schema."""
        schema = {
            'name': name,
            'namespace': schema_def.get('namespace', self.default_namespace),
            'required_elements': schema_def.get('required_elements', []),
            'optional_elements': schema_def.get('optional_elements', []),
            'forbidden_elements': schema_def.get('forbidden_elements', []),
            'attributes': schema_def.get('attributes', {}),
            'created_at': datetime.now().isoformat()
        }
        self.schemas[name] = schema
        return schema
    
    def get_schema(self, name: str) -> Optional[Dict[str, Any]]:
        """Get schema by name."""
        return self.schemas.get(name)
    
    def update_schema(self, name: str, updates: Dict[str, Any]) -> bool:
        """Update an existing schema."""
        if name not in self.schemas:
            return False
        
        self.schemas[name].update(updates)
        self.schemas[name]['updated_at'] = datetime.now().isoformat()
        return True
    
    def delete_schema(self, name: str) -> bool:
        """Delete a schema."""
        if name in self.schemas:
            del self.schemas[name]
            return True
        return False
    
    def list_schemas(self) -> List[str]:
        """List all schema names."""
        return list(self.schemas.keys())
    
    def validate_xml_against_schema(self, xml_content: str, schema_name: str) -> Tuple[bool, List[str]]:
        """Validate XML against a named schema."""
        schema = self.get_schema(schema_name)
        if not schema:
            return False, [f"Schema not found: {schema_name}"]
        
        validator = XMLValidator()
        return validator.validate_against_schema(xml_content, schema)


class XMLRoundTripProcessor:
    """Process XML with round-trip guarantees."""
    
    def __init__(self):
        self.round_trips = []
    
    def to_xml(self, data: Any, format_hint: str = 'auto') -> str:
        """Convert data to XML."""
        if isinstance(data, dict):
            return self._dict_to_xml(data)
        elif isinstance(data, list):
            return self._list_to_xml(data)
        else:
            return f'<data><![CDATA[{data}]]></data>'
    
    def from_xml(self, xml_content: str, target_format: str = 'auto') -> Any:
        """Convert XML back to original format."""
        # Extract CDATA if present
        cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', xml_content, re.DOTALL)
        if cdata_match:
            return cdata_match.group(1)
        
        # Try to parse as dict
        if '<dict>' in xml_content or '<item' in xml_content:
            return self._xml_to_dict(xml_content)
        
        return xml_content
    
    def _dict_to_xml(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to XML."""
        xml = '<dict>\n'
        for key, value in data.items():
            xml += f'  <item key="{key}">{value}</item>\n'
        xml += '</dict>'
        return xml
    
    def _list_to_xml(self, data: List[Any]) -> str:
        """Convert list to XML."""
        xml = '<list>\n'
        for item in data:
            xml += f'  <item>{item}</item>\n'
        xml += '</list>'
        return xml
    
    def _xml_to_dict(self, xml_content: str) -> Dict[str, Any]:
        """Convert XML to dictionary."""
        result = {}
        items = re.findall(r'<item key="([^"]*)">(.*?)</item>', xml_content)
        for key, value in items:
            result[key] = value
        return result
    
    def verify_round_trip(self, original_data: Any) -> Dict[str, Any]:
        """Verify round-trip conversion."""
        xml = self.to_xml(original_data)
        recovered = self.from_xml(xml)
        
        round_trip = {
            'original': original_data,
            'xml': xml,
            'recovered': recovered,
            'successful': str(original_data) == str(recovered),
            'timestamp': datetime.now().isoformat()
        }
        
        self.round_trips.append(round_trip)
        return round_trip


class XMLSemanticPreservation:
    """Preserve semantic meaning in XML transformations."""
    
    def __init__(self):
        self.preservation_log = []
        self.semantic_markers = {}
    
    def preserve(self, xml_content: str, semantic_markers: Dict[str, Any]) -> str:
        """Add semantic preservation markers to XML."""
        # Store semantic markers
        marker_id = len(self.preservation_log)
        self.semantic_markers[marker_id] = semantic_markers
        
        # Add preservation metadata to XML
        preservation_meta = f'<!-- semantic-preservation id="{marker_id}" -->\n'
        preserved_xml = preservation_meta + xml_content
        
        self.preservation_log.append({
            'id': marker_id,
            'markers': semantic_markers,
            'timestamp': datetime.now().isoformat()
        })
        
        return preserved_xml
    
    def restore_semantics(self, xml_content: str) -> Tuple[str, Dict[str, Any]]:
        """Restore semantic information from XML."""
        # Extract preservation ID
        id_match = re.search(r'<!-- semantic-preservation id="(\d+)" -->', xml_content)
        if id_match:
            marker_id = int(id_match.group(1))
            markers = self.semantic_markers.get(marker_id, {})
            
            # Remove preservation metadata
            clean_xml = re.sub(r'<!-- semantic-preservation id="\d+" -->\n?', '', xml_content)
            
            return clean_xml, markers
        
        return xml_content, {}
    
    def validate_preservation(self, original_xml: str, transformed_xml: str) -> Dict[str, Any]:
        """Validate that semantic meaning is preserved."""
        _, original_markers = self.restore_semantics(original_xml)
        _, transformed_markers = self.restore_semantics(transformed_xml)
        
        preserved = original_markers == transformed_markers
        
        return {
            'preserved': preserved,
            'original_markers': original_markers,
            'transformed_markers': transformed_markers,
            'timestamp': datetime.now().isoformat()
        }
    
    def add_semantic_tags(self, xml_content: str, tags: List[str]) -> str:
        """Add semantic tags to XML."""
        tags_xml = '<semantic-tags>\n'
        for tag in tags:
            tags_xml += f'  <tag>{tag}</tag>\n'
        tags_xml += '</semantic-tags>\n'
        
        # Insert after first tag
        match = re.search(r'(<[^?][^>]*>)', xml_content)
        if match:
            pos = match.end()
            return xml_content[:pos] + '\n' + tags_xml + xml_content[pos:]
        
        return tags_xml + xml_content
    
    def extract_semantic_tags(self, xml_content: str) -> List[str]:
        """Extract semantic tags from XML."""
        tags = re.findall(r'<tag>(.*?)</tag>', xml_content)
        return tags
