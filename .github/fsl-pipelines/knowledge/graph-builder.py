#!/usr/bin/env python3
"""
FSL Continuum - Graph Builder

SPEC:000 - Tools & Scripts Migration
Part of FSL Continuum v2.1 - Terminal Velocity CI/CD

Multi-Market Engineering Principles:
- US: Innovation & rapid iteration
- CN: Scale & performance optimization  
- IN: Quality assurance & cost-effectiveness
- JP: Craftsmanship (Monozukuri, Kaizen, Wa, Ringi, Anshin)

Japanese Principles:
- Monozukuri (ものづくり): Craftsmanship in manufacturing/code
- Kaizen (改善): Continuous improvement
- Wa (和): Harmony and teamwork
- Ringi (稟議): Consensus-based decision making
- Anshin (安心): Peace of mind through security

Category: Knowledge
"""

import json
import sys
import argparse
import logging
import hashlib
import ast
import re
from datetime import datetime
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass, asdict, field
from pathlib import Path
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Entity:
    """Knowledge graph entity (node)"""
    id: str
    type: str  # 'function', 'class', 'module', 'concept'
    name: str
    source_file: str
    line_number: int
    attributes: Dict = field(default_factory=dict)
    embedding: Optional[List[float]] = None


@dataclass
class Relationship:
    """Knowledge graph relationship (edge)"""
    id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str  # 'calls', 'imports', 'inherits', 'uses', 'depends_on'
    confidence: float  # 0.0-1.0
    verified_at_source: bool = False  # Gemba verification


@dataclass
class Pattern:
    """Discovered pattern in codebase"""
    id: str
    pattern_type: str  # 'design_pattern', 'anti_pattern', 'best_practice'
    description: str
    occurrences: List[str]  # Entity IDs
    confidence: float


class GembaSourceVerifier:
    """
    Japanese Gemba: Go to source for verification
    Always verify relationships at the source code
    """
    
    def __init__(self):
        self.verification_cache = {}
    
    def verify_at_source(
        self,
        relationship: Relationship,
        entities: Dict[str, Entity]
    ) -> bool:
        """
        Verify relationship by examining source code directly
        Gemba principle: Truth is at the source
        """
        source_entity = entities.get(relationship.source_entity_id)
        target_entity = entities.get(relationship.target_entity_id)
        
        if not source_entity or not target_entity:
            return False
        
        # Read source file directly (Gemba)
        try:
            source_file = Path(source_entity.source_file)
            if not source_file.exists():
                return False
            
            with open(source_file, 'r') as f:
                source_code = f.read()
            
            # Verify relationship exists in source
            if relationship.relationship_type == 'calls':
                # Check if target function is called
                pattern = rf'\b{target_entity.name}\s*\('
                found = re.search(pattern, source_code) is not None
                
            elif relationship.relationship_type == 'imports':
                # Check if target is imported
                pattern = rf'from .* import .*{target_entity.name}|import .*{target_entity.name}'
                found = re.search(pattern, source_code) is not None
                
            elif relationship.relationship_type == 'inherits':
                # Check if class inherits
                pattern = rf'class {source_entity.name}\([^)]*{target_entity.name}[^)]*\)'
                found = re.search(pattern, source_code) is not None
                
            else:
                found = False
            
            if found:
                logger.info(f"✅ Gemba: Verified '{relationship.relationship_type}' at source")
            else:
                logger.warning(f"⚠️ Gemba: Could not verify '{relationship.relationship_type}' at source")
            
            return found
            
        except Exception as e:
            logger.error(f"Gemba verification failed: {e}")
            return False


class PatternRecognizer:
    """
    Pattern recognition engine
    US research: ML-based pattern discovery
    """
    
    def __init__(self):
        self.known_patterns = {
            'singleton': self._detect_singleton,
            'factory': self._detect_factory,
            'observer': self._detect_observer,
            'god_class': self._detect_god_class
        }
    
    def recognize_patterns(
        self,
        entities: Dict[str, Entity],
        relationships: Dict[str, Relationship]
    ) -> List[Pattern]:
        """
        Recognize design patterns and anti-patterns
        """
        logger.info("🔍 Recognizing patterns in codebase...")
        
        discovered_patterns = []
        
        for pattern_name, detector in self.known_patterns.items():
            pattern = detector(entities, relationships)
            if pattern:
                discovered_patterns.append(pattern)
                logger.info(f"   Found: {pattern_name} pattern ({len(pattern.occurrences)} occurrences)")
        
        return discovered_patterns
    
    def _detect_singleton(
        self,
        entities: Dict[str, Entity],
        relationships: Dict[str, Relationship]
    ) -> Optional[Pattern]:
        """Detect singleton pattern"""
        singletons = []
        
        for entity_id, entity in entities.items():
            if entity.type == 'class':
                # Simple heuristic: class with _instance attribute and getInstance method
                if '_instance' in str(entity.attributes.get('methods', [])):
                    singletons.append(entity_id)
        
        if singletons:
            return Pattern(
                id=hashlib.md5(f"singleton_{len(singletons)}".encode()).hexdigest(),
                pattern_type='design_pattern',
                description='Singleton pattern: Ensures only one instance of a class exists',
                occurrences=singletons,
                confidence=0.8
            )
        return None
    
    def _detect_factory(
        self,
        entities: Dict[str, Entity],
        relationships: Dict[str, Relationship]
    ) -> Optional[Pattern]:
        """Detect factory pattern"""
        factories = []
        
        for entity_id, entity in entities.items():
            if entity.type == 'function' and 'create' in entity.name.lower():
                factories.append(entity_id)
        
        if factories:
            return Pattern(
                id=hashlib.md5(f"factory_{len(factories)}".encode()).hexdigest(),
                pattern_type='design_pattern',
                description='Factory pattern: Creates objects without specifying exact class',
                occurrences=factories,
                confidence=0.7
            )
        return None
    
    def _detect_observer(
        self,
        entities: Dict[str, Entity],
        relationships: Dict[str, Relationship]
    ) -> Optional[Pattern]:
        """Detect observer pattern"""
        observers = []
        
        for entity_id, entity in entities.items():
            if entity.type == 'class' and any(
                keyword in str(entity.attributes)
                for keyword in ['notify', 'subscribe', 'observer']
            ):
                observers.append(entity_id)
        
        if observers:
            return Pattern(
                id=hashlib.md5(f"observer_{len(observers)}".encode()).hexdigest(),
                pattern_type='design_pattern',
                description='Observer pattern: Defines one-to-many dependency between objects',
                occurrences=observers,
                confidence=0.75
            )
        return None
    
    def _detect_god_class(
        self,
        entities: Dict[str, Entity],
        relationships: Dict[str, Relationship]
    ) -> Optional[Pattern]:
        """Detect god class anti-pattern"""
        god_classes = []
        
        for entity_id, entity in entities.items():
            if entity.type == 'class':
                # Count relationships
                rel_count = sum(
                    1 for r in relationships.values()
                    if r.source_entity_id == entity_id or r.target_entity_id == entity_id
                )
                
                # God class: too many relationships (>20)
                if rel_count > 20:
                    god_classes.append(entity_id)
        
        if god_classes:
            return Pattern(
                id=hashlib.md5(f"god_class_{len(god_classes)}".encode()).hexdigest(),
                pattern_type='anti_pattern',
                description='God Class: Class with too many responsibilities',
                occurrences=god_classes,
                confidence=0.85
            )
        return None


class KaizenGraphOptimizer:
    """
    Japanese Kaizen: Continuous graph improvement
    0.1% quality improvement per iteration
    """
    
    def __init__(self):
        self.baseline_quality = 0.0
        self.improvement_history = []
    
    def calculate_graph_quality(
        self,
        entities: Dict[str, Entity],
        relationships: Dict[str, Relationship]
    ) -> float:
        """
        Calculate overall graph quality score
        """
        # Quality metrics
        entity_count = len(entities)
        relationship_count = len(relationships)
        
        # Verified relationships (Gemba)
        verified_count = sum(1 for r in relationships.values() if r.verified_at_source)
        verification_rate = verified_count / relationship_count if relationship_count > 0 else 0
        
        # Average relationship confidence
        avg_confidence = (
            sum(r.confidence for r in relationships.values()) / relationship_count
            if relationship_count > 0 else 0
        )
        
        # Graph density (relationships per entity)
        density = relationship_count / entity_count if entity_count > 0 else 0
        
        # Overall quality score
        quality = (
            verification_rate * 0.4 +
            avg_confidence * 0.3 +
            min(density / 10, 1.0) * 0.3  # Normalize density
        )
        
        return quality
    
    def apply_kaizen_improvement(
        self,
        entities: Dict[str, Entity],
        relationships: Dict[str, Relationship]
    ) -> Dict:
        """
        Apply Kaizen continuous improvement
        Target: 0.1% improvement
        """
        current_quality = self.calculate_graph_quality(entities, relationships)
        
        if self.baseline_quality == 0.0:
            self.baseline_quality = current_quality
            kaizen_target = current_quality * 1.001
        else:
            kaizen_target = self.baseline_quality * 1.001
        
        # Check if improvement achieved
        if current_quality >= kaizen_target:
            improvement_pct = ((current_quality - self.baseline_quality) / self.baseline_quality * 100)
            logger.info(f"✅ Kaizen: {improvement_pct:.3f}% graph quality improvement")
            
            self.baseline_quality = current_quality
            self.improvement_history.append({
                'timestamp': datetime.now().isoformat(),
                'quality': current_quality,
                'improvement_pct': improvement_pct
            })
            
            return {
                'kaizen_achieved': True,
                'improvement_pct': improvement_pct,
                'current_quality': current_quality,
                'next_target': current_quality * 1.001
            }
        else:
            remaining = kaizen_target - current_quality
            logger.info(f"📈 Kaizen opportunity: {remaining:.4f} quality points to target")
            return {
                'kaizen_achieved': False,
                'current_quality': current_quality,
                'target_quality': kaizen_target,
                'remaining': remaining
            }


class KnowledgeGraphBuilder:
    """
    Self-evolving knowledge graph builder
    4-market integration for world-class knowledge management
    """
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[str, Relationship] = {}
        self.patterns: List[Pattern] = []
        
        self.gemba_verifier = GembaSourceVerifier()
        self.pattern_recognizer = PatternRecognizer()
        self.kaizen_optimizer = KaizenGraphOptimizer()
    
    def extract_entities_from_file(self, file_path: Path) -> List[Entity]:
        """
        Extract entities from Python file
        Gemba: Direct source examination
        """
        entities = []
        
        try:
            with open(file_path, 'r') as f:
                source_code = f.read()
            
            # Parse AST
            tree = ast.parse(source_code)
            
            # Extract classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    entity_id = hashlib.md5(f"{file_path}:{node.name}".encode()).hexdigest()
                    
                    # Extract methods
                    methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                    
                    entity = Entity(
                        id=entity_id,
                        type='class',
                        name=node.name,
                        source_file=str(file_path),
                        line_number=node.lineno,
                        attributes={'methods': methods}
                    )
                    entities.append(entity)
                
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:  # Top-level function
                    entity_id = hashlib.md5(f"{file_path}:{node.name}".encode()).hexdigest()
                    
                    entity = Entity(
                        id=entity_id,
                        type='function',
                        name=node.name,
                        source_file=str(file_path),
                        line_number=node.lineno,
                        attributes={'args': [arg.arg for arg in node.args.args]}
                    )
                    entities.append(entity)
            
            logger.info(f"   Extracted {len(entities)} entities from {file_path.name}")
            
        except Exception as e:
            logger.error(f"Error extracting entities from {file_path}: {e}")
        
        return entities
    
    def discover_relationships(self, file_path: Path) -> List[Relationship]:
        """
        Discover relationships from source code
        """
        relationships = []
        
        try:
            with open(file_path, 'r') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            
            # Discover function calls
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        # Simple function call
                        rel_id = hashlib.md5(f"call:{node.func.id}".encode()).hexdigest()
                        # Note: In production, resolve entity IDs properly
                        relationships.append(Relationship(
                            id=rel_id,
                            source_entity_id='unknown',  # Would resolve from context
                            target_entity_id=node.func.id,
                            relationship_type='calls',
                            confidence=0.9
                        ))
            
        except Exception as e:
            logger.error(f"Error discovering relationships: {e}")
        
        return relationships
    
    def build_from_codebase(self, codebase_path: str) -> Dict:
        """
        Build knowledge graph from entire codebase
        Chinese efficiency: High-performance processing
        """
        logger.info("=" * 60)
        logger.info("🧠 KNOWLEDGE GRAPH CONSTRUCTION - 4-MARKET INTEGRATION")
        logger.info("   US 🇺🇸 | China 🇨🇳 | India 🇮🇳 | Japan 🇯🇵")
        logger.info("=" * 60)
        
        codebase = Path(codebase_path)
        
        # Find all Python files
        python_files = list(codebase.rglob('*.py'))
        logger.info(f"Found {len(python_files)} Python files")
        
        # Extract entities
        logger.info("\n📦 Extracting entities (Gemba: at source)...")
        for file_path in python_files[:20]:  # Limit for demo
            entities = self.extract_entities_from_file(file_path)
            for entity in entities:
                self.entities[entity.id] = entity
        
        logger.info(f"✅ Extracted {len(self.entities)} entities")
        
        # Discover relationships
        logger.info("\n🔗 Discovering relationships...")
        for file_path in python_files[:20]:
            relationships = self.discover_relationships(file_path)
            for rel in relationships[:100]:  # Limit for demo
                self.relationships[rel.id] = rel
        
        logger.info(f"✅ Discovered {len(self.relationships)} relationships")
        
        # Gemba verification
        logger.info("\n🔍 Gemba: Verifying relationships at source...")
        verified_count = 0
        for rel_id, rel in list(self.relationships.items())[:50]:  # Sample
            if self.gemba_verifier.verify_at_source(rel, self.entities):
                rel.verified_at_source = True
                verified_count += 1
        
        logger.info(f"✅ Verified {verified_count} relationships")
        
        # Pattern recognition
        logger.info("\n🎯 Recognizing patterns...")
        self.patterns = self.pattern_recognizer.recognize_patterns(
            self.entities,
            self.relationships
        )
        logger.info(f"✅ Found {len(self.patterns)} patterns")
        
        # Kaizen optimization
        logger.info("\n📈 Kaizen: Continuous quality improvement...")
        kaizen_result = self.kaizen_optimizer.apply_kaizen_improvement(
            self.entities,
            self.relationships
        )
        
        if kaizen_result['kaizen_achieved']:
            logger.info(f"✅ Kaizen target achieved!")
        else:
            logger.info(f"📊 Current quality: {kaizen_result['current_quality']:.4f}")
        
        return {
            'entity_count': len(self.entities),
            'relationship_count': len(self.relationships),
            'pattern_count': len(self.patterns),
            'verified_relationships': verified_count,
            'kaizen_status': kaizen_result,
            'timestamp': datetime.now().isoformat()
        }
    
    def export_graph(self, output_path: str):
        """Export knowledge graph to JSON"""
        graph_data = {
            'entities': [asdict(e) for e in self.entities.values()],
            'relationships': [asdict(r) for r in self.relationships.values()],
            'patterns': [asdict(p) for p in self.patterns],
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'entity_count': len(self.entities),
                'relationship_count': len(self.relationships),
                'pattern_count': len(self.patterns)
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(graph_data, f, indent=2, default=str)
        
        logger.info(f"✅ Knowledge graph exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Self-Evolving Knowledge Graph Builder (4-Market Integration)'
    )
    parser.add_argument(
        '--codebase',
        type=str,
        default='/home/ubuntu/src/repos/github-actions',
        help='Path to codebase'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='knowledge-graph.json',
        help='Output file for knowledge graph'
    )
    
    args = parser.parse_args()
    
    try:
        builder = KnowledgeGraphBuilder()
        results = builder.build_from_codebase(args.codebase)
        builder.export_graph(args.output)
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 KNOWLEDGE GRAPH CONSTRUCTION COMPLETE!")
        logger.info(f"   Entities: {results['entity_count']}")
        logger.info(f"   Relationships: {results['relationship_count']}")
        logger.info(f"   Patterns: {results['pattern_count']}")
        logger.info(f"   Kaizen status: {results['kaizen_status']['kaizen_achieved']}")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Knowledge graph construction failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
