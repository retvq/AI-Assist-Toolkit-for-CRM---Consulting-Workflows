"""
Module 1: Lead/Opportunity Intelligence
Reduce time spent understanding messy lead information.
"""
from typing import Dict
from core.llm_client import get_llm_client
from core.validators import validate_text_input
from core.formatters import (
    format_draft_header,
    format_section_header,
    format_disclaimer
)


SYSTEM_PROMPT = """You are an AI assistant helping consultants understand lead/opportunity information.
Your role is to analyze messy, unstructured lead data and produce clear, actionable summaries.

CRITICAL RULES:
1. CLEARLY SEPARATE facts (directly stated in input) from inferences (your interpretations)
2. NEVER fabricate details not present in the input
3. If information is missing or unclear, explicitly state uncertainty
4. Format output for CRM compatibility
5. Be concise and professional
6. Do NOT use any emojis in your output

OUTPUT FORMAT (use exactly this structure):
## Business Summary
[2-3 sentence summary of the lead/opportunity]

## Explicit Pain Points (Observed)
[List ONLY pain points directly mentioned in the input, quote when possible]
- "..." 
- "..."

## Inferred Client Intent
[Your interpretations based on context - clearly label these as inferences]
- [Inference]: [Your reasoning]

## Suggested Next Actions
[Actionable recommendations based on the analysis]
- Action 1
- Action 2

## Uncertainty / Missing Information
[What couldn't be determined from the input]
- Missing: [item]
- Unclear: [item]
"""


def process_lead_intelligence(input_text: str) -> Dict:
    """
    Process lead/opportunity information and generate structured output.
    
    Args:
        input_text: Raw lead notes, email threads, or call summaries
        
    Returns:
        Dict with 'success', 'output', and 'error' keys
    """
    # Validate input
    is_valid, error = validate_text_input(
        input_text,
        min_length=50,
        max_length=15000,
        field_name="Lead information"
    )
    
    if not is_valid:
        return {
            "success": False,
            "output": None,
            "error": error
        }
    
    # Get LLM client
    llm = get_llm_client()
    
    if not llm.is_available():
        return {
            "success": False,
            "output": None,
            "error": "LLM service is not configured. Please set GROQ_API_KEY in your .env file."
        }
    
    # Construct prompt
    user_prompt = f"""Analyze the following lead/opportunity information and provide a structured summary.

---
INPUT:
{input_text}
---

Remember:
- Separate OBSERVED facts from INFERRED insights
- Quote directly from input when citing pain points
- Be explicit about what's uncertain or missing
- Keep the summary CRM-ready and professional
- Do NOT use any emojis
"""

    # Generate response
    result = llm.generate(
        prompt=user_prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.3,
        max_tokens=2048
    )
    
    if not result["success"]:
        return {
            "success": False,
            "output": None,
            "error": result["error"]
        }
    
    # Format final output
    formatted_output = format_draft_header()
    formatted_output += result["content"]
    formatted_output += format_disclaimer()
    
    return {
        "success": True,
        "output": formatted_output,
        "error": None
    }


def get_sample_lead_data() -> str:
    """Return sample lead data for demonstration."""
    return """Email Thread - Lead: TechStart Solutions

From: Sarah Chen <sarah@techstart.io>
To: sales@ourcompany.com
Subject: RE: Your CRM Platform Demo Request

Hi,

Thanks for reaching out. We're currently using Salesforce but honestly it's been a nightmare for our team of 25 sales reps. The main issues:

1. Data entry takes forever - reps spend 2+ hours daily just logging calls
2. Our reports are always wrong because nobody updates opportunities properly
3. We tried Salesforce automation but it broke more things than it fixed
4. Management wants real-time pipeline visibility but we can only do weekly exports

We're growing fast (just closed Series B - $15M) and need something that actually works with our workflow, not against it. Our sales cycle is typically 3-6 months for enterprise deals.

Budget isn't the main concern - we just need something that our team will actually use. Previous tools failed because of poor adoption.

Can we schedule a demo for next Tuesday or Wednesday? I'll bring our VP of Sales and our RevOps lead.

Best,
Sarah Chen
Head of Sales Operations
TechStart Solutions

---

Call Notes (Internal):
- Sarah seemed frustrated with current solution
- Mentioned they've looked at HubSpot and Pipedrive but worried about migration
- VP of Sales is the decision maker, Sarah influences
- They have a dedicated RevOps person which is unusual for their size
- Timeline: Want to make decision by end of Q1
- Current contract with SF ends in 4 months
"""
