"""
FSL Continuum - AI-Powered Test Data Generator

Generates comprehensive test data for semantic languages (BAML, Pareto-Lang),
XML transformations, and other test scenarios using AI assistance.
"""

import json
import random
import string
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict

from rich.console import Console
from rich.progress import Progress, TaskID

console = Console()


@dataclass
class GeneratedTestData:
    """Container for generated test data."""
    schema_type: str
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    generation_time: datetime
    data_size: int


@dataclass
class DataGenerationConfig:
    """Configuration for test data generation."""
    num_records: int = 100
    complexity_level: str = "medium"  # simple, medium, complex
    include_edge_cases: bool = True
    seed: Optional[int] = None
    max_depth: int = 3
    locale: str = "en_US"


class TestDataGenerator:
    """AI-powered test data generator for semantic languages and testing scenarios."""
    
    def __init__(self, config: Optional[DataGenerationConfig] = None):
        self.config = config or DataGenerationConfig()
        self.generators = {}
        self._setup_random_seed()
        self._register_generators()
        
    def _setup_random_seed(self):
        """Setup random seed for reproducible generation."""
        if self.config.seed:
            random.seed(self.config.seed)
            console.print(f"[green]🔑 Using seed: {self.config.seed}[/green]")
    
    def _register_generators(self):
        """Register all data generators."""
        self.generators = {
            'baml': self._generate_baml_data,
            'pareto_lang': self._generate_pareto_lang_data,
            'xml': self._generate_xml_test_cases,
            'json': self._generate_json_data,
            'test_scenarios': self._generate_test_scenarios,
            'mock_data': self._generate_mock_data
        }
    
    def generate_data(self, schema_type: str, schema: Optional[Dict[str, Any]] = None) -> GeneratedTestData:
        """Generate test data for the specified schema type."""
        console.print(f"[blue]🎲 Generating {schema_type} test data...[/blue]")
        start_time = datetime.now()
        
        if schema_type not in self.generators:
            raise ValueError(f"Unsupported schema type: {schema_type}. "
                           f"Supported types: {list(self.generators.keys())}")
        
        try:
            with Progress() as progress:
                task = progress.add_task("Generating data...", total=100)
                
                # Generate data
                data = self.generators[schema_type](schema or {}, progress, task)
                progress.update(task, completed=100)
            
            # Create result container
            result = GeneratedTestData(
                schema_type=schema_type,
                data=data,
                metadata={
                    'num_records': len(data),
                    'complexity_level': self.config.complexity_level,
                    'include_edge_cases': self.config.include_edge_cases,
                    'generation_config': asdict(self.config)
                },
                generation_time=start_time,
                data_size=len(json.dumps(data).encode())
            )
            
            console.print(f"[green]✅ Generated {len(data)} records of type {schema_type}[/green]")
            return result
            
        except Exception as e:
            console.print(f"[red]❌ Failed to generate {schema_type} data: {e}[/red]")
            raise
    
    def _generate_baml_data(self, schema: Dict[str, Any], progress: Progress, task: TaskID) -> List[Dict[str, Any]]:
        """Generate test data for BAML schemas."""
        progress.update(task, advance=20)
        
        # BAML-specific data generation patterns
        field_types = {
            'string': self._generate_strings,
            'number': self._generate_numbers,
            'boolean': self._generate_booleans,
            'array': self._generate_arrays,
            'object': self._generate_objects,
            'enum': self._generate_enums,
            'date': self._generate_dates,
            'email': self._generate_emails,
            'url': self._generate_urls
        }
        
        progress.update(task, advance=30)
        
        # Generate test records
        data = []
        for i in range(self.config.num_records):
            record = {}
            
            # Generate based on schema or use default BAML structure
            if schema and 'fields' in schema:
                for field in schema['fields']:
                    field_type = field.get('type', 'string')
                    field_name = field.get('name', f'field_{i}')
                    
                    if field_type in field_types:
                        record[field_name] = field_types[field_type](field_name)
            else:
                # Default BAML test structure
                record = {
                    'id': f"baml_{i:06d}",
                    'name': self._generate_strings('name'),
                    'description': self._generate_strings('description', length=50),
                    'type': random.choice(['entity', 'relation', 'attribute', 'constraint']),
                    'properties': self._generate_objects(),
                    'metadata': {
                        'created_at': self._generate_dates(),
                        'version': f"1.{random.randint(0, 9)}.{random.randint(0, 99)}",
                        'validated': random.choice([True, False])
                    }
                }
            
            # Add edge cases if requested
            if self.config.include_edge_cases and i % 20 == 0:
                record = self._add_edge_case(record, 'baml')
            
            data.append(record)
            progress.update(task, advance=50 / self.config.num_records)
        
        progress.update(task, completed=100)
        return data
    
    def _generate_pareto_lang_data(self, schema: Dict[str, Any], progress: Progress, task: TaskID) -> List[Dict[str, Any]]:
        """Generate test data for Pareto-Lang schemas."""
        progress.update(task, advance=20)
        
        # Pareto-Lang specific patterns (80/20 rule optimization)
        pareto_patterns = {
            'priority': lambda: random.choices(['high', 'medium', 'low'], weights=[0.2, 0.3, 0.5])[0],
            'impact': lambda: random.choices(['high', 'medium', 'low'], weights=[0.2, 0.3, 0.5])[0],
            'value': lambda: random.uniform(1.0, 100.0),
            'effort': lambda: random.uniform(1.0, 10.0),
            'confidence': lambda: random.uniform(0.0, 1.0)
        }
        
        progress.update(task, advance=30)
        
        data = []
        for i in range(self.config.num_records):
            record = {
                'id': f"pareto_{i:06d}",
                'name': self._generate_strings('feature'),
                'description': self._generate_strings('description', length=100),
                'category': random.choice(['ui', 'backend', 'data', 'integration', 'performance']),
                'priority': pareto_patterns['priority'](),
                'impact': pareto_patterns['impact'](),
                'value': pareto_patterns['value'](),
                'effort': pareto_patterns['effort'](),
                'confidence': pareto_patterns['confidence'](),
                'metrics': {
                    'users_affected': random.randint(1, 10000),
                    'revenue_impact': random.uniform(0, 1000000),
                    'time_saved': random.uniform(0, 100),
                    'error_reduction': random.uniform(0, 50)
                },
                'requirements': self._generate_arrays('requirement'),
                'dependencies': self._generate_arrays('dependency'),
                'status': random.choice(['proposed', 'in_progress', 'completed', 'on_hold'])
            }
            
            # Add edge cases
            if self.config.include_edge_cases and i % 25 == 0:
                record = self._add_edge_case(record, 'pareto_lang')
            
            data.append(record)
            progress.update(task, advance=50 / self.config.num_records)
        
        progress.update(task, completed=100)
        return data
    
    def _generate_xml_test_cases(self, schema: Dict[str, Any], progress: Progress, task: TaskID) -> List[str]:
        """Generate XML test cases from XSD schema or default patterns."""
        progress.update(task, advance=20)
        
        xml_templates = [
            '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n{content}\n</root>',
            '<{tag}>\n{content}\n</{tag}>',
            '<element attr="{attr}">{value}</element>',
            '<container>\n{items}\n</container>'
        ]
        
        progress.update(task, advance=30)
        
        xml_cases = []
        for i in range(self.config.num_records):
            template = random.choice(xml_templates)
            
            if '{tag}' in template:
                xml_case = template.format(
                    tag=random.choice(['item', 'element', 'node', 'record']),
                    attr=self._generate_strings('attribute'),
                    value=self._generate_strings('value')
                )
            elif '{content}' in template:
                content_items = [
                    f'<field>{self._generate_strings("field")}</field>'
                    for _ in range(random.randint(1, 5))
                ]
                xml_case = template.format(content='\n'.join(content_items))
            else:
                xml_case = template
            
            # Add edge cases
            if self.config.include_edge_cases and i % 30 == 0:
                xml_case = self._add_xml_edge_case(xml_case)
            
            xml_cases.append(xml_case)
            progress.update(task, advance=50 / self.config.num_records)
        
        progress.update(task, completed=100)
        return xml_cases
    
    def _generate_json_data(self, schema: Dict[str, Any], progress: Progress, task: TaskID) -> List[Dict[str, Any]]:
        """Generate JSON test data with nested structures."""
        progress.update(task, advance=20)
        
        data = []
        for i in range(self.config.num_records):
            record = {
                'id': i,
                'name': self._generate_strings('name'),
                'nested': self._generate_nested_objects(),
                'array_field': self._generate_arrays('item'),
                'timestamp': datetime.now().isoformat(),
                'metadata': self._generate_objects()
            }
            data.append(record)
            progress.update(task, advance=80 / self.config.num_records)
        
        progress.update(task, completed=100)
        return data
    
    def _generate_test_scenarios(self, schema: Dict[str, Any], progress: Progress, task: TaskID) -> List[Dict[str, Any]]:
        """Generate comprehensive test scenarios."""
        progress.update(task, advance=20)
        
        scenario_types = [
            'happy_path',
            'error_case',
            'edge_case',
            'performance_case',
            'security_case',
            'integration_case'
        ]
        
        scenarios = []
        for i in range(self.config.num_records):
            scenario_type = random.choice(scenario_types)
            scenario = {
                'id': f"scenario_{i:06d}",
                'name': self._generate_strings('scenario'),
                'type': scenario_type,
                'description': self._generate_strings('description', length=100),
                'preconditions': self._generate_arrays('precondition'),
                'steps': self._generate_arrays('step'),
                'expected_result': self._generate_objects(),
                'test_data': self._generate_objects(),
                'priority': random.choice(['critical', 'high', 'medium', 'low']),
                'tags': self._generate_arrays('tag'),
                'automatable': random.choice([True, False])
            }
            scenarios.append(scenario)
            progress.update(task, advance=80 / self.config.num_records)
        
        progress.update(task, completed=100)
        return scenarios
    
    def _generate_mock_data(self, schema: Dict[str, Any], progress: Progress, task: TaskID) -> List[Dict[str, Any]]:
        """Generate mock data for testing external services."""
        progress.update(task, advance=20)
        
        service_types = ['api', 'database', 'filesystem', 'network', 'cache']
        mock_services = []
        
        for i in range(self.config.num_records):
            service_type = random.choice(service_types)
            mock_service = {
                'service_name': f"{service_type}_{i}",
                'service_type': service_type,
                'endpoints': self._generate_arrays('endpoint'),
                'responses': self._generate_arrays('response'),
                'delay_ms': random.randint(10, 1000),
                'error_rate': random.uniform(0.0, 0.1),
                'status': random.choice(['active', 'inactive', 'maintenance']),
                'config': {
                    'timeout': random.randint(5, 60),
                    'retries': random.randint(0, 5),
                    'cache_ttl': random.randint(60, 3600)
                }
            }
            mock_services.append(mock_service)
            progress.update(task, advance=80 / self.config.num_records)
        
        progress.update(task, completed=100)
        return mock_services
    
    # Helper methods for data generation
    def _generate_strings(self, context: str = "", length: int = 10) -> str:
        """Generate random strings."""
        chars = string.ascii_letters + string.digits + " _-."
        return ''.join(random.choices(chars, k=length))
    
    def _generate_numbers(self, context: str = "") -> Union[int, float]:
        """Generate random numbers."""
        if random.choice([True, False]):
            return random.randint(1, 1000)
        else:
            return round(random.uniform(0.1, 1000.0), 2)
    
    def _generate_booleans(self, context: str = "") -> bool:
        """Generate random booleans."""
        return random.choice([True, False])
    
    def _generate_arrays(self, item_type: str = "item") -> List[Any]:
        """Generate random arrays."""
        array_length = random.randint(0, 5)
        return [self._generate_strings(f"{item_type}_{i}") for i in range(array_length)]
    
    def _generate_objects(self, depth: int = 0) -> Dict[str, Any]:
        """Generate random nested objects."""
        if depth >= self.config.max_depth:
            return self._generate_strings("value")
        
        obj = {}
        num_fields = random.randint(1, 4)
        for i in range(num_fields):
            field_type = random.choice(['string', 'number', 'boolean', 'array', 'object'])
            field_name = f"field_{i}"
            
            if field_type == 'string':
                obj[field_name] = self._generate_strings(field_name)
            elif field_type == 'number':
                obj[field_name] = self._generate_numbers(field_name)
            elif field_type == 'boolean':
                obj[field_name] = self._generate_booleans(field_name)
            elif field_type == 'array':
                obj[field_name] = self._generate_arrays(field_name)
            elif field_type == 'object':
                obj[field_name] = self._generate_objects(depth + 1)
        
        return obj
    
    def _generate_enums(self, context: str = "") -> str:
        """Generate random enum values."""
        return random.choice(['ACTIVE', 'INACTIVE', 'PENDING', 'COMPLETED', 'CANCELLED'])
    
    def _generate_dates(self, context: str = "") -> str:
        """Generate random dates."""
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        random_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        return random_date.isoformat()
    
    def _generate_emails(self, context: str = "") -> str:
        """Generate random email addresses."""
        domains = ['example.com', 'test.org', 'mock.net', 'fake.email']
        username = self._generate_strings('user', length=8)
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    def _generate_urls(self, context: str = "") -> str:
        """Generate random URLs."""
        protocols = ['http', 'https']
        domains = ['example.com', 'test.org', 'api.mock.net']
        paths = ['api/v1', 'service', 'resource', 'data']
        
        protocol = random.choice(protocols)
        domain = random.choice(domains)
        path = random.choice(paths)
        resource = self._generate_strings('resource', length=8)
        
        return f"{protocol}://{domain}/{path}/{resource}"
    
    def _generate_nested_objects(self, depth: int = 0) -> Dict[str, Any]:
        """Generate nested objects for JSON."""
        if depth >= 2:  # Limit nesting depth
            return self._generate_strings('value')
        
        return {
            'level1': self._generate_objects(depth + 1),
            'level2': self._generate_arrays('item'),
            'level3': self._generate_numbers('number')
        }
    
    def _add_edge_case(self, record: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """Add edge cases to test records."""
        edge_record = record.copy()
        
        if data_type == 'baml':
            edge_record.update({
                'id': None,  # Null ID
                'name': '',  # Empty string
                'properties': {},  # Empty object
                'metadata': None  # Null metadata
            })
        elif data_type == 'pareto_lang':
            edge_record.update({
                'priority': 'invalid_priority',  # Invalid enum
                'impact': None,  # Null impact
                'value': -1,  # Negative value
                'confidence': 2.0  # Invalid confidence > 1.0
            })
        
        edge_record['is_edge_case'] = True
        return edge_record
    
    def _add_xml_edge_case(self, xml_case: str) -> str:
        """Add edge cases to XML test cases."""
        # Add problematic XML structures
        edge_cases = [
            xml_case.replace('>', '/>'),  # Self-closing tag
            xml_case + '\x00',  # Null character
            '<?xml version="1.0" encoding="UTF-8"?>\n<root></root>' + xml_case,  # Duplicate root
            xml_case.replace('"', "'") + "'",  # Quote mismatch
        ]
        return random.choice(edge_cases)
    
    def save_to_file(self, test_data: GeneratedTestData, output_path: str):
        """Save generated test data to file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': asdict(test_data.metadata),
                'generation_time': test_data.generation_time.isoformat(),
                'data': test_data.data
            }, f, indent=2, default=str)
        
        console.print(f"[green]💾 Saved {len(test_data.data)} records to {output_path}[/green]")
    
    def get_generation_report(self) -> Dict[str, Any]:
        """Get report of last data generation."""
        return {
            'generator_version': '1.0.0',
            'supported_types': list(self.generators.keys()),
            'config': asdict(self.config),
            'last_generation': datetime.now().isoformat()
        }


# Utility functions for standalone usage
def generate_test_data(schema_type: str, num_records: int = 100, 
                    output_file: Optional[str] = None) -> GeneratedTestData:
    """Utility function to generate test data."""
    config = DataGenerationConfig(num_records=num_records)
    generator = TestDataGenerator(config)
    
    test_data = generator.generate_data(schema_type)
    
    if output_file:
        generator.save_to_file(test_data, output_file)
    
    return test_data


if __name__ == "__main__":
    # Example usage
    console.print("[bold blue]🎲 FSL Continuum Test Data Generator[/bold blue]")
    
    # Generate BAML test data
    baml_data = generate_test_data('baml', 50, 'test_baml_data.json')
    
    # Generate Pareto-Lang test data  
    pareto_data = generate_test_data('pareto_lang', 30, 'test_pareto_data.json')
    
    # Generate XML test cases
    xml_cases = generate_test_data('xml', 25, 'test_xml_cases.json')
    
    console.print("[green]✅ Test data generation complete![/green]")
