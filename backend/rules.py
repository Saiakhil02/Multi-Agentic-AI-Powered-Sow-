"""
Simple rules and configuration for SOW compliance checking.
"""

# Basic required fields that should be present in any SOW
REQUIRED_FIELDS = {
    "Project Title": [r'\bproject\s+title\b', r'\btitle\b'],
    "Start Date": [r'\bstart\s+date\b', r'\bbegin\s+date\b'],
    "End Date": [r'\bend\s+date\b', r'\bcompletion\s+date\b'],
    "Scope of Work": [r'\bscope\b', r'\bscope\s+of\s+work\b'],
    "Deliverables": [r'\bdeliverables\b', r'\boutcomes\b'],
    "Payment Terms": [r'\bpayment\b', r'\bpayment\s+terms\b']
}

# Simple compliance rules to check
COMPLIANCE_RULES = {
    "CONF-1": {
        "type": "regex",
        "pattern": r'\bconfidentiality\b',
        "should_exist": True,
        "description": "Confidentiality clause missing",
        "severity": "High"
    },
    "TERM-1": {
        "type": "regex",
        "pattern": r'\btermination\b',
        "should_exist": True,
        "description": "Termination clause missing",
        "severity": "Medium"
    },
    "IP-1": {
        "type": "regex",
        "pattern": r'\bintellectual\s+property\b',
        "should_exist": True,
        "description": "IP rights not defined",
        "severity": "High"
    },
    "LIAB-1": {
        "type": "semantic",
        "keywords": ["liability", "indemnification"],
        "should_exist": True,
        "description": "Liability limits missing",
        "severity": "High"
    }
}

# Basic risk terms to identify in contracts
RISK_TERMS = {
    "unlimited liability": {
        "description": "Unlimited liability without caps",
        "impact": 3
    },
    "best efforts": {
        "description": "Ambiguous performance standard",
        "impact": 1
    },
    "time is of the essence": {
        "description": "Strict timeframe requirement",
        "impact": 2
    },
    "full satisfaction": {
        "description": "Subjective acceptance criteria",
        "impact": 2
    }
}

def calculate_compliance_score(missing_fields_count, compliance_issues_count, risk_level):
    """Calculate simple compliance score"""
    # Base score of 100
    score = 100
    
    # Deduct for missing fields (up to 50 points)
    field_deduction = min(missing_fields_count * 8, 50)
    score -= field_deduction
    
    # Deduct for compliance issues (up to 30 points)
    compliance_deduction = min(compliance_issues_count * 7, 30)
    score -= compliance_deduction
    
    # Deduct for risk level (up to 20 points)
    if risk_level == "High":
        score -= 20
    elif risk_level == "Medium":
        score -= 10
    
    # Ensure score is between 0 and 100
    return max(0, min(100, score))
