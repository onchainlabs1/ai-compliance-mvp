"""
Compliance Analysis Tools

Tools for analyzing code compliance with AI regulations and standards.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

class ComplianceChecker:
    """
    Tool to check code for compliance with AI regulations and standards.
    """
    
    def __init__(self):
        self.ai_act_requirements = {
            "high_risk_systems": [
                "biometric_identification",
                "critical_infrastructure",
                "education_training",
                "employment_worker_management",
                "essential_services",
                "law_enforcement",
                "migration_asylum",
                "administration_justice"
            ],
            "documentation_requirements": [
                "technical_documentation",
                "risk_assessment",
                "data_governance",
                "human_oversight",
                "accuracy_metrics",
                "logging_capabilities",
                "transparency_information"
            ],
            "prohibited_systems": [
                "subliminal_manipulation",
                "vulnerability_exploitation",
                "social_scoring",
                "real_time_biometric_identification"
            ]
        }
        
        self.iso_42001_requirements = {
            "governance": [
                "ai_policy",
                "roles_responsibilities",
                "risk_management_process",
                "continuous_improvement"
            ],
            "documentation": [
                "ai_inventory",
                "data_quality_assessment",
                "model_validation",
                "implementation_records",
                "performance_monitoring"
            ],
            "operational_controls": [
                "change_management",
                "incident_response",
                "data_protection",
                "supplier_management",
                "training_awareness"
            ]
        }
    
    def analyze_code(self, code_content: str, file_type: str = "py") -> Dict[str, Any]:
        """
        Analyze code for potential compliance issues.
        
        Args:
            code_content: The content of the code file to analyze
            file_type: The type of file (py, js, etc.)
            
        Returns:
            Dictionary with compliance findings
        """
        findings = {
            "ai_act": self._analyze_ai_act_compliance(code_content, file_type),
            "iso_42001": self._analyze_iso_42001_compliance(code_content, file_type)
        }
        
        # Calculate overall risk level
        risk_levels = [finding.get("risk_level", 0) for category in findings.values() 
                      for finding in category if isinstance(finding, dict)]
        
        if "high" in risk_levels:
            findings["overall_risk"] = "high"
        elif "medium" in risk_levels:
            findings["overall_risk"] = "medium"
        else:
            findings["overall_risk"] = "low"
            
        findings["summary"] = self._generate_compliance_summary(findings)
        
        return findings
    
    def _analyze_ai_act_compliance(self, code_content: str, file_type: str) -> List[Dict[str, Any]]:
        """Analyze code for AI Act compliance issues"""
        findings = []
        
        # Check for high-risk indicators
        for high_risk in self.ai_act_requirements["high_risk_systems"]:
            if high_risk in code_content.lower():
                findings.append({
                    "type": "high_risk_system",
                    "category": high_risk,
                    "risk_level": "high",
                    "description": f"Potential high-risk AI system identified: {high_risk}",
                    "recommendation": "Conduct a full impact assessment and ensure all documentation requirements are met"
                })
        
        # Check for documentation indicators
        missing_docs = []
        for doc_req in self.ai_act_requirements["documentation_requirements"]:
            # Simple heuristic check for documentation mentions
            if doc_req not in code_content.lower() and f"document_{doc_req}" not in code_content.lower():
                missing_docs.append(doc_req)
        
        if missing_docs:
            findings.append({
                "type": "documentation",
                "missing_elements": missing_docs,
                "risk_level": "medium",
                "description": f"Missing documentation elements: {', '.join(missing_docs)}",
                "recommendation": "Add comments or documentation addressing these missing elements"
            })
        
        # Check for prohibited systems indicators
        for prohibited in self.ai_act_requirements["prohibited_systems"]:
            if prohibited in code_content.lower():
                findings.append({
                    "type": "prohibited_system",
                    "category": prohibited,
                    "risk_level": "high",
                    "description": f"Potential prohibited AI practice identified: {prohibited}",
                    "recommendation": "Remove or substantially modify this functionality to comply with AI Act"
                })
        
        return findings
    
    def _analyze_iso_42001_compliance(self, code_content: str, file_type: str) -> List[Dict[str, Any]]:
        """Analyze code for ISO 42001 compliance issues"""
        findings = []
        
        # Check for governance indicators
        missing_governance = []
        for gov_req in self.iso_42001_requirements["governance"]:
            if gov_req not in code_content.lower():
                missing_governance.append(gov_req)
        
        if missing_governance:
            findings.append({
                "type": "governance",
                "missing_elements": missing_governance,
                "risk_level": "medium",
                "description": f"Missing governance elements: {', '.join(missing_governance)}",
                "recommendation": "Implement governance controls for these elements"
            })
        
        # Check for documentation indicators
        missing_docs = []
        for doc_req in self.iso_42001_requirements["documentation"]:
            if doc_req not in code_content.lower():
                missing_docs.append(doc_req)
        
        if missing_docs:
            findings.append({
                "type": "documentation",
                "missing_elements": missing_docs,
                "risk_level": "low",
                "description": f"Missing ISO 42001 documentation elements: {', '.join(missing_docs)}",
                "recommendation": "Add documentation for these elements"
            })
        
        # Check for operational controls
        missing_controls = []
        for control in self.iso_42001_requirements["operational_controls"]:
            if control not in code_content.lower():
                missing_controls.append(control)
        
        if missing_controls:
            findings.append({
                "type": "operational_controls",
                "missing_elements": missing_controls,
                "risk_level": "medium",
                "description": f"Missing operational controls: {', '.join(missing_controls)}",
                "recommendation": "Implement operational controls for these elements"
            })
        
        return findings
    
    def _generate_compliance_summary(self, findings: Dict[str, Any]) -> str:
        """Generate a summary of compliance findings"""
        ai_act_issues = len(findings.get("ai_act", []))
        iso_issues = len(findings.get("iso_42001", []))
        overall_risk = findings.get("overall_risk", "unknown")
        
        summary = f"Compliance Analysis Summary:\n"
        summary += f"- Overall Risk Level: {overall_risk.upper()}\n"
        summary += f"- EU AI Act Issues: {ai_act_issues}\n"
        summary += f"- ISO 42001 Issues: {iso_issues}\n\n"
        
        if overall_risk == "high":
            summary += "URGENT: This code contains high-risk elements that require immediate attention for regulatory compliance."
        elif overall_risk == "medium":
            summary += "ATTENTION NEEDED: Several compliance issues need to be addressed before production deployment."
        else:
            summary += "MINOR ISSUES: Low-risk compliance issues identified, consider addressing them in future updates."
            
        return summary

def get_compliance_checker() -> ComplianceChecker:
    """Get an instance of the compliance checker tool"""
    return ComplianceChecker()

def generate_compliance_report(findings: Dict[str, Any], output_path: Optional[str] = None) -> str:
    """
    Generate a detailed compliance report from findings.
    
    Args:
        findings: Compliance findings from the checker
        output_path: Optional path to save the report to
        
    Returns:
        Path to the generated report
    """
    report = {
        "timestamp": str(Path.now()),
        "findings": findings,
        "recommendations": _generate_recommendations(findings)
    }
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        return output_path
    
    return json.dumps(report, indent=2)

def _generate_recommendations(findings: Dict[str, Any]) -> List[str]:
    """Generate actionable recommendations based on findings"""
    recommendations = []
    
    # Extract all recommendations from findings
    for category in ["ai_act", "iso_42001"]:
        for finding in findings.get(category, []):
            if isinstance(finding, dict) and "recommendation" in finding:
                recommendations.append(finding["recommendation"])
    
    # Add general recommendations based on risk level
    if findings.get("overall_risk") == "high":
        recommendations.append("Conduct a full Data Protection Impact Assessment (DPIA)")
        recommendations.append("Implement a complete AI governance framework")
        recommendations.append("Consider seeking external certification or audit")
    elif findings.get("overall_risk") == "medium":
        recommendations.append("Document all AI system components and their purpose")
        recommendations.append("Implement risk monitoring and mitigation procedures")
    
    return recommendations 