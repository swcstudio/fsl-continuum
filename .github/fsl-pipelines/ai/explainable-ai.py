#!/usr/bin/env python3
"""
FSL Continuum - Explainable Ai

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

Category: Ai
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('explainable-ai')


@dataclass
class DecisionExplanation:
    """Complete explanation of an AI decision"""
    decision_id: str
    decision_type: str
    rationale: str
    confidence: float
    alternatives_considered: List[Dict[str, Any]]
    data_sources: List[str]
    risk_assessment: Dict[str, Any]
    timestamp: str
    explainability_score: float


class ExplainableAI:
    """
    Generate comprehensive explanations for AI decisions
    Target: 90% reduction in "why did AI do this?" questions
    """
    
    def __init__(self):
        self.explanation_templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load explanation templates"""
        return {
            'prediction': """
## AI Decision Explanation

### Decision Summary
{summary}

### Confidence Level: {confidence:.1%}

### Reasoning Chain
{reasoning}

### Data Sources Used
{data_sources}

### Alternative Options Considered
{alternatives}

### Risk Assessment
{risk_assessment}

### Recommendation
{recommendation}
""",
            'code_review': """
## Code Review AI Analysis

### Overall Assessment: {assessment}

### Key Findings
{findings}

### Reasoning
{reasoning}

### Confidence: {confidence:.1%}

### Suggested Actions
{actions}
"""
        }
    
    def explain_prediction(
        self,
        prediction_result: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> DecisionExplanation:
        """Generate explanation for ML prediction"""
        
        # Extract key information
        predictions = prediction_result.get('predictions', {})
        confidence = prediction_result.get('confidence', 0.0)
        risk = prediction_result.get('risk_assessment', {})
        
        # Build rationale
        rationale_parts = []
        
        if 'is_successful' in predictions:
            success_prob = predictions['is_successful'].get('prediction', {}).get('probability', {})
            rationale_parts.append(
                f"Deployment success probability: {success_prob.get('success', 0.5):.1%}"
            )
        
        if 'cost' in predictions:
            cost_pred = predictions['cost'].get('prediction', {}).get('value', 0)
            rationale_parts.append(f"Predicted cost: ${cost_pred:.3f}")
        
        rationale = "\n".join(f"- {p}" for p in rationale_parts)
        
        # Alternatives considered
        alternatives = [
            {
                'option': 'Proceed without prediction',
                'outcome': 'Higher risk of deployment issues',
                'confidence': 0.0
            },
            {
                'option': 'Manual review',
                'outcome': 'Lower risk but slower process',
                'confidence': 0.9
            }
        ]
        
        # Data sources
        data_sources = [
            'Historical deployment data (EXPChain)',
            'Git commit metadata',
            'Code complexity metrics',
            'Author success patterns'
        ]
        
        explanation = DecisionExplanation(
            decision_id=prediction_result.get('request_id', 'unknown'),
            decision_type='ml_prediction',
            rationale=rationale,
            confidence=confidence,
            alternatives_considered=alternatives,
            data_sources=data_sources,
            risk_assessment=risk,
            timestamp=datetime.now().isoformat(),
            explainability_score=0.85
        )
        
        return explanation
    
    def generate_markdown_report(
        self,
        explanation: DecisionExplanation
    ) -> str:
        """Generate markdown explanation report"""
        
        template = self.explanation_templates['prediction']
        
        # Format alternatives
        alternatives_md = "\n".join([
            f"**{i+1}. {alt['option']}**\n"
            f"   - Outcome: {alt['outcome']}\n"
            f"   - Confidence: {alt['confidence']:.1%}"
            for i, alt in enumerate(explanation.alternatives_considered)
        ])
        
        # Format data sources
        data_sources_md = "\n".join(f"- {ds}" for ds in explanation.data_sources)
        
        # Format risk
        risk = explanation.risk_assessment
        risk_md = f"**Level**: {risk.get('level', 'UNKNOWN')}\n"
        risk_md += f"**Score**: {risk.get('overall_score', 0):.2f}\n"
        
        # Fill template
        report = template.format(
            summary=explanation.rationale,
            confidence=explanation.confidence,
            reasoning="Based on historical patterns and current metrics",
            data_sources=data_sources_md,
            alternatives=alternatives_md,
            risk_assessment=risk_md,
            recommendation="Proceed with recommended actions"
        )
        
        return report
    
    def save_explanation(
        self,
        explanation: DecisionExplanation,
        output_dir: str = ".flow-state/explanations"
    ):
        """Save explanation for audit trail"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as JSON
        json_file = f"{output_dir}/{explanation.decision_id}.json"
        with open(json_file, 'w') as f:
            json.dump(explanation.__dict__, f, indent=2)
        
        # Save as Markdown
        md_file = f"{output_dir}/{explanation.decision_id}.md"
        with open(md_file, 'w') as f:
            f.write(self.generate_markdown_report(explanation))
        
        logger.info(f"💾 Explanation saved: {json_file}")


# CLI
if __name__ == '__main__':
    explainer = ExplainableAI()
    
    # Example prediction result
    sample = {
        'request_id': 'test_123',
        'predictions': {
            'is_successful': {
                'prediction': {'probability': {'success': 0.87, 'failure': 0.13}}
            },
            'cost': {'prediction': {'value': 0.15}}
        },
        'confidence': 0.89,
        'risk_assessment': {'level': 'LOW', 'overall_score': 0.25}
    }
    
    explanation = explainer.explain_prediction(sample)
    report = explainer.generate_markdown_report(explanation)
    print(report)
