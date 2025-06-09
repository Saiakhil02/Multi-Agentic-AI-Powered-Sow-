# compliance_checker.py
import spacy
from transformers import pipeline
from datetime import datetime
import json

class ComplianceAgent:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.clause_checker = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            framework="pt",
            device=-1
        )
       
        self.required_fields = [
            "Project Title", "Scope of Work", "Deliverables",
            "Timeline", "Payment Terms", "Confidentiality",
            "Termination", "Limitation of Liability"
        ]

    def validate_structure(self, sow_data):
        """Check for missing fields and basic validation"""
        missing = []
        issues = []
        
        for field in self.required_fields:
            value = sow_data.get(field)
            if not value:
                print(f"MISSING {field}:")
                print(sow_data)
                missing.append(field)
                continue
                
            if isinstance(value, list) and not value:
                issues.append(f"{field.replace('_', ' ').title()} list is empty")
            elif isinstance(value, str) and not value.strip():
                issues.append(f"{field.replace('_', ' ').title()} is empty")
        
        return missing, issues

    def analyze_clauses(self, text):
        """AI-powered clause analysis"""
        clauses = ["confidentiality", "termination", "liability"]
        results = self.clause_checker(text, clauses, multi_label=True)
        
        issues = []
        for label, score in zip(results['labels'], results['scores']):
            if score < 0.6:
                issues.append(f"{label.title()} clause needs strengthening ({score:.1%} confidence)")
        return issues

    def check_language(self, text):
        """Language quality checks"""
        doc = self.nlp(text)
        issues = []
        
        # Passive voice detection
        for sent in doc.sents:
            if any(token.dep_ == "nsubjpass" for token in sent):
                issues.append(f"Passive voice: '{sent.text}'")
        
        # Vague terms check
        vague_terms = ["appropriate", "reasonable", "etc."]
        for term in vague_terms:
            if term in text.lower():
                issues.append(f"Vague term used: '{term}'")
        
        return issues

    def generate_report(self, sow_data):
        """Full compliance analysis"""
        report = {
            "missing_fields": [],
            "structural_issues": [],
            "content_issues": [],
            "language_issues": [],
            "compliance_score": 100,
            "risk_level": "low",
            "recommendations": []
        }
        
        # Structural validation
        report["missing_fields"], report["structural_issues"] = self.validate_structure(sow_data)
        
        # Content analysis
        if "sow_text" in sow_data:
            report["content_issues"].extend(self.analyze_clauses(sow_data["sow_text"]))
            report["language_issues"].extend(self.check_language(sow_data["sow_text"]))
        
        # Calculate score
        penalties = (
            len(report["missing_fields"]) * 5 +
            len(report["structural_issues"]) * 3 +
            len(report["content_issues"]) * 2 +
            len(report["language_issues"]) * 1
        )
        report["compliance_score"] = max(0, 100 - penalties)
        
        # Determine risk level
        if report["compliance_score"] >= 85:
            report["risk_level"] = "low"
        elif report["compliance_score"] >= 60:
            report["risk_level"] = "medium"
        else:
            report["risk_level"] = "high"
            
        # Generate recommendations
        if report["missing_fields"]:
            report["recommendations"].append(f"Add missing fields: {', '.join(report['missing_fields'])}")
        if any("confidentiality" in issue.lower() for issue in report["content_issues"]):
            report["recommendations"].append("Include explicit NDA language in confidentiality clause")
        if report["language_issues"]:
            report["recommendations"].append("Revise vague terms and passive voice constructions")
        
        return report

class FormattingAgent:
    def format_report(self, report):
        """Console-friendly report formatting"""
        return f"""
=== Compliance Report ===
Score: {report['compliance_score']}/100
Risk Level: {report['risk_level'].upper()}

Missing Fields:
{self._format_list(report['missing_fields'])}

Structural Issues:
{self._format_list(report['structural_issues'])}

Content Issues:
{self._format_list(report['content_issues'])}

Language Issues:
{self._format_list(report['language_issues'])}

Recommendations:
{self._format_list(report['recommendations'])}
"""
    
    def _format_list(self, items):
        return "\n".join(f"- {item}" for item in items) if items else "None"

# if __name__ == "__main__":
#     # Sample SOW from drafting agent
#     sample_sow = {
#         "project_title": "E-Commerce Platform",
#         "scope_of_work": "Development of online store",
#         "deliverables": ["Shopping cart", "Product catalog"],
#         "timeline": "2025-09-01 to 2025-12-31",
#         "payment_terms": "$50,000 USD",
#         "sow_text": "The project will involve appropriate measures to ensure quality."
#     }
    
#     # Initialize agents
#     compliance_agent = ComplianceAgent()
#     formatter = FormattingAgent()
    
#     # Process flow
#     report = compliance_agent.generate_report(sample_sow)
#     print(formatter.format_report(report))
