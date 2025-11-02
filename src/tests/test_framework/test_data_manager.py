"""
FSL Continuum - Test Data Manager

Manages test data and fixtures for semantic language testing.
Provides dynamic test data generation and fixture management.
"""

import os
import json
import yaml
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataType(Enum):
    """Supported test data types."""
    BAML = "baml"
    PARETO_LANG = "pareto_lang"
    XML = "xml"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    ERROR = "error"
    EDGE_CASE = "edge_case"

@dataclass
class TestFixture:
    """Test fixture definition."""
    name: str
    data_type: DataType
    input_data: Any
    expected_output: Any
    metadata: Optional[Dict[str, Any]] = None
    validation_rules: Optional[Dict[str, Any]] = None
    performance_thresholds: Optional[Dict[str, Any]] = None

@dataclass
class TestDataSet:
    """Test data set definition."""
    name: str
    description: str
    data_type: DataType
    fixtures: List[TestFixture]
    metadata: Optional[Dict[str, Any]] = None
    generation_rules: Optional[Dict[str, Any]] = None

class TestDataManager:
    """Manages test data and fixtures for semantic language testing."""
    
    def __init__(self):
        self.test_data_path = Path(__file__).parent.parent / "fixtures" / "test_data"
        self.fixtures_path = Path(__file__).parent.parent / "fixtures"
        self.test_cache = {}
        self.fixture_cache = {}
        self.dynamic_data_generators = self._initialize_data_generators()
        
        # Load all test data
        self.baml_test_data = self._load_baml_test_data()
        self.pareto_lang_test_data = self._load_pareto_lang_test_data()
        self.xml_test_data = self._load_xml_test_data()
        self.integration_test_data = self._load_integration_test_data()
        self.performance_test_data = self._load_performance_test_data()
        self.error_test_data = self._load_error_test_data()
        self.edge_case_test_data = self._load_edge_case_test_data()
        
        logger.info("TestDataManager initialized successfully")
    
    def get_baml_test_fixture(self, fixture_name: str) -> Optional[TestFixture]:
        """Get BAML test fixture by name."""
        return self._get_fixture_from_data(self.baml_test_data, fixture_name, DataType.BAML)
    
    def get_pareto_lang_test_fixture(self, fixture_name: str) -> Optional[TestFixture]:
        """Get Pareto-Lang test fixture by name."""
        return self._get_fixture_from_data(self.pareto_lang_test_data, fixture_name, DataType.PARETO_LANG)
    
    def get_xml_test_fixture(self, fixture_name: str) -> Optional[TestFixture]:
        """Get XML test fixture by name."""
        return self._get_fixture_from_data(self.xml_test_data, fixture_name, DataType.XML)
    
    def get_integration_test_fixture(self, fixture_name: str) -> Optional[TestFixture]:
        """Get integration test fixture by name."""
        return self._get_fixture_from_data(self.integration_test_data, fixture_name, DataType.INTEGRATION)
    
    def get_performance_test_fixture(self, fixture_name: str) -> Optional[TestFixture]:
        """Get performance test fixture by name."""
        return self._get_fixture_from_data(self.performance_test_data, fixture_name, DataType.PERFORMANCE)
    
    def get_error_test_fixture(self, fixture_name: str) -> Optional[TestFixture]:
        """Get error test fixture by name."""
        return self._get_fixture_from_data(self.error_test_data, fixture_name, DataType.ERROR)
    
    def get_edge_case_test_fixture(self, fixture_name: str) -> Optional[TestFixture]:
        """Get edge case test fixture by name."""
        return self._get_fixture_from_data(self.edge_case_test_data, fixture_name, DataType.EDGE_CASE)
    
    def get_baml_test_fixtures(self, category: Optional[str] = None) -> List[TestFixture]:
        """Get all BAML test fixtures, optionally filtered by category."""
        fixtures = []
        for test_set in self.baml_test_data.values():
            if category is None or test_set.metadata.get("category") == category:
                fixtures.extend(test_set.fixtures)
        return fixtures
    
    def get_pareto_lang_test_fixtures(self, category: Optional[str] = None) -> List[TestFixture]:
        """Get all Pareto-Lang test fixtures, optionally filtered by category."""
        fixtures = []
        for test_set in self.pareto_lang_test_data.values():
            if category is None or test_set.metadata.get("category") == category:
                fixtures.extend(test_set.fixtures)
        return fixtures
    
    def get_xml_test_fixtures(self, category: Optional[str] = None) -> List[TestFixture]:
        """Get all XML test fixtures, optionally filtered by category."""
        fixtures = []
        for test_set in self.xml_test_data.values():
            if category is None or test_set.metadata.get("category") == category:
                fixtures.extend(test_set.fixtures)
        return fixtures
    
    def get_integration_test_fixtures(self, category: Optional[str] = None) -> List[TestFixture]:
        """Get all integration test fixtures, optionally filtered by category."""
        fixtures = []
        for test_set in self.integration_test_data.values():
            if category is None or test_set.metadata.get("category") == category:
                fixtures.extend(test_set.fixtures)
        return fixtures
    
    def get_performance_test_fixtures(self, category: Optional[str] = None) -> List[TestFixture]:
        """Get all performance test fixtures, optionally filtered by category."""
        fixtures = []
        for test_set in self.performance_test_data.values():
            if category is None or test_set.metadata.get("category") == category:
                fixtures.extend(test_set.fixtures)
        return fixtures
    
    def get_error_test_fixtures(self, category: Optional[str] = None) -> List[TestFixture]:
        """Get all error test fixtures, optionally filtered by category."""
        fixtures = []
        for test_set in self.error_test_data.values():
            if category is None or test_set.metadata.get("category") == category:
                fixtures.extend(test_set.fixtures)
        return fixtures
    
    def get_edge_case_test_fixtures(self, category: Optional[str] = None) -> List[TestFixture]:
        """Get all edge case test fixtures, optionally filtered by category."""
        fixtures = []
        for test_set in self.edge_case_test_data.values():
            if category is None or test_set.metadata.get("category") == category:
                fixtures.extend(test_set.fixtures)
        return fixtures
    
    def generate_test_data(self, data_type: DataType, parameters: Dict[str, Any]) -> TestFixture:
        """Generate test data dynamically."""
        try:
            generator = self.dynamic_data_generators.get(data_type)
            if generator is None:
                raise ValueError(f"No data generator available for data type: {data_type}")
            
            generated_data = generator(parameters)
            
            # Create test fixture
            fixture_name = f"generated_{data_type.value}_{datetime.now().isoformat()}"
            test_fixture = TestFixture(
                name=fixture_name,
                data_type=data_type,
                input_data=generated_data["input"],
                expected_output=generated_data["expected"],
                metadata=generated_data.get("metadata"),
                validation_rules=generated_data.get("validation_rules"),
                performance_thresholds=generated_data.get("performance_thresholds")
            )
            
            return test_fixture
            
        except Exception as e:
            logger.error(f"Failed to generate test data for {data_type}: {e}")
            raise
    
    def save_test_fixture(self, fixture: TestFixture, file_path: str) -> bool:
        """Save test fixture to file."""
        try:
            fixture_dict = asdict(fixture)
            file_path = Path(file_path)
            
            # Create directory if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save based on file extension
            if file_path.suffix.lower() == '.json':
                with open(file_path, 'w') as f:
                    json.dump(fixture_dict, f, indent=2)
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                with open(file_path, 'w') as f:
                    yaml.dump(fixture_dict, f, default_flow_style=False)
            else:
                # Default to JSON
                with open(file_path.with_suffix('.json'), 'w') as f:
                    json.dump(fixture_dict, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save test fixture: {e}")
            return False
    
    def load_test_fixture(self, file_path: str) -> Optional[TestFixture]:
        """Load test fixture from file."""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"Test fixture file not found: {file_path}")
                return None
            
            # Load based on file extension
            if file_path.suffix.lower() == '.json':
                with open(file_path, 'r') as f:
                    fixture_dict = json.load(f)
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                with open(file_path, 'r') as f:
                    fixture_dict = yaml.safe_load(f)
            else:
                # Try JSON first, then YAML
                with open(file_path.with_suffix('.json'), 'r') as f:
                    fixture_dict = json.load(f)
            
            # Create TestFixture object
            return TestFixture(
                name=fixture_dict["name"],
                data_type=DataType(fixture_dict["data_type"]),
                input_data=fixture_dict["input_data"],
                expected_output=fixture_dict["expected_output"],
                metadata=fixture_dict.get("metadata"),
                validation_rules=fixture_dict.get("validation_rules"),
                performance_thresholds=fixture_dict.get("performance_thresholds")
            )
            
        except Exception as e:
            logger.error(f"Failed to load test fixture: {e}")
            return None
    
    def get_test_data_summary(self) -> Dict[str, Any]:
        """Get summary of all test data."""
        return {
            "baml_test_data": {
                "datasets": len(self.baml_test_data),
                "fixtures": sum(len(test_set.fixtures) for test_set in self.baml_test_data.values()),
                "categories": self._get_data_categories(self.baml_test_data)
            },
            "pareto_lang_test_data": {
                "datasets": len(self.pareto_lang_test_data),
                "fixtures": sum(len(test_set.fixtures) for test_set in self.pareto_lang_test_data.values()),
                "categories": self._get_data_categories(self.pareto_lang_test_data)
            },
            "xml_test_data": {
                "datasets": len(self.xml_test_data),
                "fixtures": sum(len(test_set.fixtures) for test_set in self.xml_test_data.values()),
                "categories": self._get_data_categories(self.xml_test_data)
            },
            "integration_test_data": {
                "datasets": len(self.integration_test_data),
                "fixtures": sum(len(test_set.fixtures) for test_set in self.integration_test_data.values()),
                "categories": self._get_data_categories(self.integration_test_data)
            },
            "performance_test_data": {
                "datasets": len(self.performance_test_data),
                "fixtures": sum(len(test_set.fixtures) for test_set in self.performance_test_data.values()),
                "categories": self._get_data_categories(self.performance_test_data)
            },
            "error_test_data": {
                "datasets": len(self.error_test_data),
                "fixtures": sum(len(test_set.fixtures) for test_set in self.error_test_data.values()),
                "categories": self._get_data_categories(self.error_test_data)
            },
            "edge_case_test_data": {
                "datasets": len(self.edge_case_test_data),
                "fixtures": sum(len(test_set.fixtures) for test_set in self.edge_case_test_data.values()),
                "categories": self._get_data_categories(self.edge_case_test_data)
            }
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get test data manager status."""
        return {
            "status": "active",
            "test_data_path": str(self.test_data_path),
            "fixtures_path": str(self.fixtures_path),
            "data_generators": list(self.dynamic_data_generators.keys()),
            "cache_size": len(self.test_cache) + len(self.fixture_cache),
            "data_summary": self.get_test_data_summary()
        }
    
    def _get_fixture_from_data(self, test_data: Dict[str, TestDataSet], fixture_name: str, data_type: DataType) -> Optional[TestFixture]:
        """Get fixture from test data."""
        for test_set in test_data.values():
            for fixture in test_set.fixtures:
                if fixture.name == fixture_name:
                    return fixture
        return None
    
    def _initialize_data_generators(self) -> Dict[DataType, callable]:
        """Initialize dynamic data generators."""
        return {
            DataType.BAML: self._generate_baml_data,
            DataType.PARETO_LANG: self._generate_pareto_lang_data,
            DataType.XML: self._generate_xml_data,
            DataType.INTEGRATION: self._generate_integration_data,
            DataType.PERFORMANCE: self._generate_performance_data,
            DataType.ERROR: self._generate_error_data,
            DataType.EDGE_CASE: self._generate_edge_case_data
        }
    
    def _generate_baml_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate BAML test data."""
        data_type = parameters.get("data_type", "basic")
        
        if data_type == "basic":
            return {
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
                    "boundaries_count": 1
                },
                "metadata": {"generation_type": "basic_baml"}
            }
        elif data_type == "complex":
            return {
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "boundaries": [
                        {
                            "name": f"test_boundary_{i}",
                            "type": ["data", "process", "system"][i % 3],
                            "ai_enhanced": True
                        }
                        for i in range(parameters.get("boundary_count", 5))
                    ],
                    "connections": [
                        {
                            "source": f"test_boundary_{i}",
                            "target": f"test_boundary_{(i+1) % parameters.get('boundary_count', 5)}",
                            "type": "data_flow"
                        }
                        for i in range(parameters.get("boundary_count", 5))
                    ]
                },
                "expected": {
                    "success": True,
                    "boundaries_count": parameters.get("boundary_count", 5),
                    "connections_count": parameters.get("boundary_count", 5)
                },
                "metadata": {"generation_type": "complex_baml"}
            }
        else:
            raise ValueError(f"Unknown BAML data type: {data_type}")
    
    def _generate_pareto_lang_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Pareto-Lang test data."""
        data_type = parameters.get("data_type", "basic")
        
        if data_type == "basic":
            return {
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "PARETO-SEMANTIC-001",
                    "optimizations": [
                        {
                            "name": "test_optimization",
                            "type": "pareto",
                            "target": "efficiency_maximization",
                            "efficiency": 0.85
                        }
                    ]
                },
                "expected": {
                    "success": True,
                    "optimizations_count": 1
                },
                "metadata": {"generation_type": "basic_pareto_lang"}
            }
        elif data_type == "complex":
            return {
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "PARETO-SEMANTIC-001",
                    "optimizations": [
                        {
                            "name": f"test_optimization_{i}",
                            "type": ["pareto", "resource", "performance"][i % 3],
                            "target": "efficiency_maximization",
                            "efficiency": 0.8 + (i * 0.02)
                        }
                        for i in range(parameters.get("optimization_count", 5))
                    ],
                    "resources": [
                        {
                            "name": f"test_resource_{i}",
                            "type": ["compute", "storage", "network"][i % 3],
                            "capacity": 100 * (i + 1),
                            "utilization": 0.7 + (i * 0.05)
                        }
                        for i in range(parameters.get("resource_count", 3))
                    ]
                },
                "expected": {
                    "success": True,
                    "optimizations_count": parameters.get("optimization_count", 5),
                    "resources_count": parameters.get("resource_count", 3)
                },
                "metadata": {"generation_type": "complex_pareto_lang"}
            }
        else:
            raise ValueError(f"Unknown Pareto-Lang data type: {data_type}")
    
    def _generate_xml_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate XML test data."""
        data_type = parameters.get("data_type", "basic")
        
        if data_type == "basic":
            xml_template = """<baml-semantic-data version="1.0.0-baml-xml" language="baml">
    <metadata>
        <schema type="baml-semantic" version="1.0.0-baml-xml"/>
    </metadata>
    <baml-content>
        <boundaries>
            <boundary name="test_boundary" type="data" ai_enhanced="true"/>
        </boundaries>
    </baml-content>
</baml-semantic-data>"""
            
            return {
                "input": xml_template,
                "expected": {
                    "success": True,
                    "root_element": "baml-semantic-data",
                    "language": "baml"
                },
                "metadata": {"generation_type": "basic_xml"}
            }
        else:
            raise ValueError(f"Unknown XML data type: {data_type}")
    
    def _generate_integration_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate integration test data."""
        return {
            "input": {
                "baml": self._generate_baml_data({"data_type": "basic"})["input"],
                "pareto_lang": self._generate_pareto_lang_data({"data_type": "basic"})["input"]
            },
            "expected": {
                "success": True,
                "integration_result": "unified",
                "languages": ["baml", "pareto_lang"]
            },
            "metadata": {"generation_type": "basic_integration"}
        }
    
    def _generate_performance_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance test data."""
        size = parameters.get("size", "medium")
        
        if size == "small":
            data_size = 10
        elif size == "medium":
            data_size = 100
        elif size == "large":
            data_size = 1000
        else:
            data_size = 100
        
        return {
            "input": {
                "data_size": data_size,
                "baml_data": self._generate_baml_data({"data_type": "complex", "boundary_count": data_size})["input"],
                "pareto_lang_data": self._generate_pareto_lang_data({"data_type": "complex", "optimization_count": data_size})["input"]
            },
            "expected": {
                "success": True,
                "performance_thresholds": {
                    "max_execution_time": 1.0 if size == "small" else (2.0 if size == "medium" else 5.0),
                    "max_memory_usage": 50 if size == "small" else (200 if size == "medium" else 1000)
                }
            },
            "metadata": {"generation_type": "performance", "size": size}
        }
    
    def _generate_error_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate error test data."""
        error_type = parameters.get("error_type", "invalid_structure")
        
        if error_type == "invalid_structure":
            return {
                "input": {
                    "version": "1.0.0-fsl-integration",
                    "spec": "BAML-SEMANTIC-001",
                    "invalid_field": "this should not be here"
                },
                "expected": {
                    "success": False,
                    "error_type": "structure_validation_error"
                },
                "metadata": {"generation_type": "error", "error_type": "invalid_structure"}
            }
        else:
            raise ValueError(f"Unknown error type: {error_type}")
    
    def _generate_edge_case_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate edge case test data."""
        edge_case_type = parameters.get("edge_case_type", "empty_data")
        
        if edge_case_type == "empty_data":
            return {
                "input": {},
                "expected": {
                    "success": True,
                    "edge_case": "empty_data"
                },
                "metadata": {"generation_type": "edge_case", "edge_case_type": "empty_data"}
            }
        elif edge_case_type == "minimal_data":
            return {
                "input": {
                    "version": "1.0.0-fsl-integration"
                },
                "expected": {
                    "success": True,
                    "edge_case": "minimal_data"
                },
                "metadata": {"generation_type": "edge_case", "edge_case_type": "minimal_data"}
            }
        else:
            raise ValueError(f"Unknown edge case type: {edge_case_type}")
    
    def _load_baml_test_data(self) -> Dict[str, TestDataSet]:
        """Load BAML test data from files."""
        return self._load_test_data_from_directory(
            self.test_data_path / "baml_test_data", 
            DataType.BAML
        )
    
    def _load_pareto_lang_test_data(self) -> Dict[str, TestDataSet]:
        """Load Pareto-Lang test data from files."""
        return self._load_test_data_from_directory(
            self.test_data_path / "pareto_lang_test_data", 
            DataType.PARETO_LANG
        )
    
    def _load_xml_test_data(self) -> Dict[str, TestDataSet]:
        """Load XML test data from files."""
        return self._load_test_data_from_directory(
            self.test_data_path / "xml_test_data", 
            DataType.XML
        )
    
    def _load_integration_test_data(self) -> Dict[str, TestDataSet]:
        """Load integration test data from files."""
        return self._load_test_data_from_directory(
            self.test_data_path / "integration_test_data", 
            DataType.INTEGRATION
        )
    
    def _load_performance_test_data(self) -> Dict[str, TestDataSet]:
        """Load performance test data from files."""
        return self._load_test_data_from_directory(
            self.test_data_path / "performance_test_data", 
            DataType.PERFORMANCE
        )
    
    def _load_error_test_data(self) -> Dict[str, TestDataSet]:
        """Load error test data from files."""
        return self._load_test_data_from_directory(
            self.test_data_path / "error_test_data", 
            DataType.ERROR
        )
    
    def _load_edge_case_test_data(self) -> Dict[str, TestDataSet]:
        """Load edge case test data from files."""
        return self._load_test_data_from_directory(
            self.test_data_path / "edge_case_test_data", 
            DataType.EDGE_CASE
        )
    
    def _load_test_data_from_directory(self, directory_path: Path, data_type: DataType) -> Dict[str, TestDataSet]:
        """Load test data from directory."""
        test_data = {}
        
        if not directory_path.exists():
            logger.warning(f"Test data directory not found: {directory_path}")
            return test_data
        
        try:
            for file_path in directory_path.glob("*.yaml"):
                with open(file_path, 'r') as f:
                    data = yaml.safe_load(f)
                    
                    # Convert to TestDataSet
                    fixtures = []
                    for fixture_data in data.get("fixtures", []):
                        fixture = TestFixture(
                            name=fixture_data["name"],
                            data_type=data_type,
                            input_data=fixture_data["input"],
                            expected_output=fixture_data["expected"],
                            metadata=fixture_data.get("metadata"),
                            validation_rules=fixture_data.get("validation_rules"),
                            performance_thresholds=fixture_data.get("performance_thresholds")
                        )
                        fixtures.append(fixture)
                    
                    test_set = TestDataSet(
                        name=data["name"],
                        description=data.get("description", ""),
                        data_type=data_type,
                        fixtures=fixtures,
                        metadata=data.get("metadata"),
                        generation_rules=data.get("generation_rules")
                    )
                    
                    test_set.name = file_path.stem
                    test_data[test_set.name] = test_set
        
        except Exception as e:
            logger.error(f"Failed to load test data from {directory_path}: {e}")
        
        return test_data
    
    def _get_data_categories(self, test_data: Dict[str, TestDataSet]) -> List[str]:
        """Get unique categories from test data."""
        categories = set()
        for test_set in test_data.values():
            if test_set.metadata:
                categories.add(test_set.metadata.get("category", "default"))
        return sorted(list(categories))

# Export main classes
__all__ = [
    'TestDataManager',
    'TestFixture',
    'TestDataSet',
    'DataType'
]
