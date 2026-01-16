"""
Module 3: CRM Data Quality & Readiness Check
Identify data issues that could break automation or analytics.
"""
from typing import Dict, List, Tuple
import pandas as pd
import re
from core.llm_client import get_llm_client
from core.validators import validate_csv_file, detect_email_format, detect_phone_format
from core.formatters import format_data_readonly_notice, format_disclaimer


def check_missing_fields(df: pd.DataFrame) -> List[Dict]:
    """Check for missing values in each column."""
    issues = []
    for col in df.columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            severity = "critical" if missing_count / len(df) > 0.1 else "warning"
            issues.append({
                "type": "missing_fields",
                "severity": severity,
                "column": col,
                "affected_count": int(missing_count),
                "total_count": len(df),
                "percentage": round(missing_count / len(df) * 100, 1),
                "description": f"Column '{col}' has {missing_count} missing values ({round(missing_count / len(df) * 100, 1)}%)"
            })
    return issues


def check_duplicates(df: pd.DataFrame) -> List[Dict]:
    """Check for duplicate records."""
    issues = []
    
    # Full row duplicates
    full_duplicates = df.duplicated().sum()
    if full_duplicates > 0:
        issues.append({
            "type": "duplicates",
            "severity": "critical",
            "column": "All Columns",
            "affected_count": int(full_duplicates),
            "total_count": len(df),
            "percentage": round(full_duplicates / len(df) * 100, 1),
            "description": f"Found {full_duplicates} exact duplicate rows"
        })
    
    # Check for potential duplicates based on key fields
    potential_key_columns = []
    for col in df.columns:
        col_lower = col.lower()
        if any(key in col_lower for key in ['email', 'phone', 'id', 'name']):
            potential_key_columns.append(col)
    
    for col in potential_key_columns[:3]:  # Check top 3 potential keys
        if df[col].dtype == 'object':
            # Normalize and check
            normalized = df[col].astype(str).str.lower().str.strip()
            dup_count = normalized.duplicated().sum()
            if dup_count > 0 and dup_count != full_duplicates:
                issues.append({
                    "type": "potential_duplicates",
                    "severity": "warning",
                    "column": col,
                    "affected_count": int(dup_count),
                    "total_count": len(df),
                    "percentage": round(dup_count / len(df) * 100, 1),
                    "description": f"Column '{col}' has {dup_count} duplicate values (potential duplicate records)"
                })
    
    return issues


def check_format_consistency(df: pd.DataFrame) -> List[Dict]:
    """Check for format inconsistencies in email, phone, and date fields."""
    issues = []
    
    for col in df.columns:
        col_lower = col.lower()
        sample_values = df[col].dropna().head(100)
        
        if len(sample_values) == 0:
            continue
        
        # Email format check
        if 'email' in col_lower:
            invalid_emails = 0
            for val in sample_values:
                if not detect_email_format(str(val)):
                    invalid_emails += 1
            if invalid_emails > 0:
                issues.append({
                    "type": "format_inconsistency",
                    "severity": "warning",
                    "column": col,
                    "affected_count": invalid_emails,
                    "total_count": len(sample_values),
                    "percentage": round(invalid_emails / len(sample_values) * 100, 1),
                    "description": f"Column '{col}' has {invalid_emails} values with invalid email format"
                })
        
        # Phone format check
        elif 'phone' in col_lower or 'mobile' in col_lower or 'tel' in col_lower:
            invalid_phones = 0
            for val in sample_values:
                if not detect_phone_format(str(val)):
                    invalid_phones += 1
            if invalid_phones > 0:
                issues.append({
                    "type": "format_inconsistency",
                    "severity": "info",
                    "column": col,
                    "affected_count": invalid_phones,
                    "total_count": len(sample_values),
                    "percentage": round(invalid_phones / len(sample_values) * 100, 1),
                    "description": f"Column '{col}' has {invalid_phones} values with inconsistent phone format"
                })
    
    return issues


def check_anomalies(df: pd.DataFrame) -> List[Dict]:
    """Check for basic anomalies and invalid values."""
    issues = []
    
    for col in df.columns:
        col_lower = col.lower()
        
        # Check for suspiciously short/long text
        if df[col].dtype == 'object':
            non_null = df[col].dropna()
            if len(non_null) > 0:
                lengths = non_null.astype(str).str.len()
                very_short = (lengths < 2).sum()
                very_long = (lengths > 500).sum()
                
                if very_short > len(non_null) * 0.1:
                    issues.append({
                        "type": "anomaly",
                        "severity": "info",
                        "column": col,
                        "affected_count": int(very_short),
                        "total_count": len(non_null),
                        "percentage": round(very_short / len(non_null) * 100, 1),
                        "description": f"Column '{col}' has {very_short} unusually short values (< 2 chars)"
                    })
        
        # Check for negative values in typically positive fields
        if df[col].dtype in ['int64', 'float64']:
            if any(word in col_lower for word in ['amount', 'price', 'revenue', 'count', 'quantity']):
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    issues.append({
                        "type": "anomaly",
                        "severity": "warning",
                        "column": col,
                        "affected_count": int(negative_count),
                        "total_count": len(df),
                        "percentage": round(negative_count / len(df) * 100, 1),
                        "description": f"Column '{col}' has {negative_count} negative values (unexpected for this field type)"
                    })
    
    return issues


def format_issues_report(issues: List[Dict], total_records: int) -> str:
    """Format the deterministic issues into a readable report."""
    if not issues:
        return """
### No Issues Detected

All deterministic checks passed. The data appears to be well-formatted.
"""
    
    # Group by severity
    critical = [i for i in issues if i['severity'] == 'critical']
    warnings = [i for i in issues if i['severity'] == 'warning']
    info = [i for i in issues if i['severity'] == 'info']
    
    output = f"""
### Data Quality Summary

- **Total Records Analyzed:** {total_records}
- **Issues Found:** {len(issues)}
  - Critical: {len(critical)}
  - Warning: {len(warnings)}
  - Info: {len(info)}

---

"""
    
    if critical:
        output += "### Critical Issues\n\n"
        for issue in critical:
            output += f"**{issue['type'].replace('_', ' ').title()}** - {issue['column']}\n"
            output += f"- {issue['description']}\n\n"
    
    if warnings:
        output += "### Warnings\n\n"
        for issue in warnings:
            output += f"**{issue['type'].replace('_', ' ').title()}** - {issue['column']}\n"
            output += f"- {issue['description']}\n\n"
    
    if info:
        output += "### Informational\n\n"
        for issue in info:
            output += f"**{issue['type'].replace('_', ' ').title()}** - {issue['column']}\n"
            output += f"- {issue['description']}\n\n"
    
    return output


AI_EXPLANATION_PROMPT = """You are an AI assistant helping explain CRM data quality issues to business users.

Given a list of data quality issues found in a CRM dataset, explain:
1. Why each type of issue matters for business operations
2. What downstream risks these issues could cause (automation failures, bad analytics, customer impact)
3. Suggested priority order for cleanup

Keep your response:
- Business-focused (not technical jargon)
- Concise but comprehensive
- Actionable
- Do NOT use any emojis

CRITICAL: You are ONLY explaining and advising. You are NOT modifying any data.
"""


def get_ai_explanation(issues: List[Dict]) -> str:
    """Get AI explanation for the data quality issues."""
    if not issues:
        return ""
    
    llm = get_llm_client()
    if not llm.is_available():
        return "\n\n_AI explanation unavailable - LLM not configured._\n"
    
    # Summarize issues for AI
    issues_summary = "Data quality issues found:\n"
    for i, issue in enumerate(issues, 1):
        issues_summary += f"{i}. {issue['type'].replace('_', ' ').title()} in '{issue['column']}': {issue['description']}\n"
    
    prompt = f"""Analyze these CRM data quality issues and provide business-focused explanations:

{issues_summary}

Provide:
1. Business impact explanation for each issue type
2. Downstream risks if not addressed
3. Recommended cleanup priority order

Do NOT use any emojis in your response.
"""

    result = llm.generate(
        prompt=prompt,
        system_prompt=AI_EXPLANATION_PROMPT,
        temperature=0.3,
        max_tokens=1500
    )
    
    if result["success"]:
        return f"""
---

### AI Analysis: Why These Issues Matter

{result["content"]}
"""
    else:
        return f"\n\n_AI explanation unavailable: {result['error']}_\n"


def process_data_quality_check(df: pd.DataFrame) -> Dict:
    """
    Process CRM data and run quality checks.
    
    Args:
        df: Pandas DataFrame from uploaded CSV
        
    Returns:
        Dict with 'success', 'output', and 'error' keys
    """
    # Validate CSV
    is_valid, error, metadata = validate_csv_file(df)
    
    if not is_valid:
        return {
            "success": False,
            "output": None,
            "error": error
        }
    
    # Run all deterministic checks
    all_issues = []
    all_issues.extend(check_missing_fields(df))
    all_issues.extend(check_duplicates(df))
    all_issues.extend(check_format_consistency(df))
    all_issues.extend(check_anomalies(df))
    
    # Sort by severity
    severity_order = {'critical': 0, 'warning': 1, 'info': 2}
    all_issues.sort(key=lambda x: severity_order.get(x['severity'], 3))
    
    # Format deterministic report
    report = f"""
## CRM Data Quality & Readiness Report

**File Summary:**
- Rows: {metadata['rows']}
- Columns: {metadata['columns']}
- Column Names: {', '.join(metadata['column_names'][:10])}{'...' if len(metadata['column_names']) > 10 else ''}

"""
    report += format_issues_report(all_issues, metadata['rows'])
    
    # Add AI explanation if issues found
    if all_issues:
        report += get_ai_explanation(all_issues)
    
    # Add read-only notice
    report += format_data_readonly_notice()
    report += format_disclaimer()
    
    return {
        "success": True,
        "output": report,
        "error": None,
        "issues": all_issues,
        "metadata": metadata
    }


def get_sample_crm_data() -> str:
    """Return sample CRM data as CSV string for demonstration."""
    return """Lead_ID,Company_Name,Contact_Name,Email,Phone,Industry,Deal_Amount,Stage,Last_Contact,Source
1,Acme Corp,John Smith,john@acme.com,555-123-4567,Technology,50000,Qualified,2024-01-15,Website
2,TechStart Inc,Sarah Johnson,sarah@techstart,555-234-5678,Technology,75000,Proposal,2024-01-10,Referral
3,Global Foods,Mike Brown,mike@globalfoods.com,(555) 345-6789,Food & Beverage,30000,Negotiation,2024-01-12,Trade Show
4,Acme Corp,John Smith,john@acme.com,555-123-4567,Technology,50000,Qualified,2024-01-15,Website
5,DataDriven LLC,,contact@datadriven.com,5554567890,Analytics,45000,Discovery,2024-01-08,Cold Call
6,Fast Logistics,Tom Wilson,tom@fastlog.com,555.567.8901,Logistics,-25000,Qualified,2024-01-14,Website
7,Smart Solutions,Amy Chen,amychen@smart.com,555-678-9012,Consulting,60000,Proposal,01/16/2024,Referral
8,,,invalid-email,not-a-phone,Unknown,0,Lead,2024-01-05,Other
9,CloudFirst,David Lee,david@cloudfirst.com,555-789-0123,Technology,80000,Closed Won,2024-01-11,Website
10,NextGen AI,Lisa Park,lisa@nextgenai.com,555-890-1234,AI/ML,120000,Proposal,,Referral
11,BuildRight,Construction Bob,bob@buildright.com,555-901-2345,Construction,35000,Qualified,2024-01-13,Trade Show
12,MediCare Plus,Dr. Nancy Adams,nancy@medicareplus.com,555-012-3456,Healthcare,90000,Discovery,2024-01-09,Cold Call
13,FinServ Global,Robert Chen,rchen@finserv.com,555-111-2222,Finance,150000,Negotiation,2024-01-07,Referral
14,EcoGreen Ltd,Emma Wilson,emma@ecogreen.com,5551112223,Sustainability,25000,Lead,2024-01-16,Website
15,TechStart Inc,Sarah Johnson,SARAH@TECHSTART.COM,555-234-5678,Technology,75000,Closed Lost,2024-01-10,Referral"""
