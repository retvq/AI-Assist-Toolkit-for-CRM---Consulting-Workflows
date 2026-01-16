"""
Module 2: Requirement to Delivery Translation
Convert client discussions into execution-ready drafts.
"""
from typing import Dict
from core.llm_client import get_llm_client
from core.validators import validate_text_input
from core.formatters import format_draft_header, format_disclaimer


SYSTEM_PROMPT = """You are an AI assistant helping consultants translate client requirements into execution-ready documentation.
Your role is to convert informal discussions into structured user stories and task breakdowns.

CRITICAL RESTRICTIONS (NEVER DO THESE):
- Do NOT estimate timelines or deadlines
- Do NOT assign ownership or resources
- Do NOT propose technical architecture
- Do NOT make delivery commitments
- Do NOT assume requirements not explicitly stated
- Do NOT use any emojis in your output

YOUR TASK:
- Extract user stories from the stakeholder perspective
- Write plain-language acceptance criteria
- Create logical task breakdowns
- Flag ambiguities that need clarification

OUTPUT FORMAT (use exactly this structure):
## User Stories

### Story 1: [Title]
**As a** [stakeholder/user type]
**I want** [goal/feature]
**So that** [benefit/value]

**Acceptance Criteria:**
- [ ] [Criterion 1 - plain language]
- [ ] [Criterion 2 - plain language]

[Repeat for each story]

## Task Breakdown

### [Feature/Epic Name]
- [ ] Task 1: [Description]
  - [ ] Subtask 1.1
  - [ ] Subtask 1.2
- [ ] Task 2: [Description]

## Clarifications Needed
[List any ambiguous requirements that need client confirmation]
- Question 1
- Question 2

## Explicit Exclusions
The following were intentionally NOT included:
- Timeline estimates (requires team input)
- Resource assignments (requires PM decision)
- Technical architecture (requires technical review)
- Delivery commitments (requires stakeholder approval)
"""


def process_requirement_translation(input_text: str) -> Dict:
    """
    Process client requirements and generate structured documentation.
    
    Args:
        input_text: Discovery notes, informal requirements, or client messages
        
    Returns:
        Dict with 'success', 'output', and 'error' keys
    """
    # Validate input
    is_valid, error = validate_text_input(
        input_text,
        min_length=50,
        max_length=15000,
        field_name="Requirements"
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
    user_prompt = f"""Translate the following client requirements into structured documentation.

---
CLIENT INPUT:
{input_text}
---

Remember:
- Write user stories from the END USER's perspective
- Keep acceptance criteria testable and specific
- Break down tasks logically
- Flag anything ambiguous
- Do NOT include timelines, assignments, or architecture decisions
- Do NOT use any emojis
"""

    # Generate response
    result = llm.generate(
        prompt=user_prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.3,
        max_tokens=3000
    )
    
    if not result["success"]:
        return {
            "success": False,
            "output": None,
            "error": result["error"]
        }
    
    # Format final output with prominent draft warning
    formatted_output = format_draft_header()
    formatted_output += result["content"]
    formatted_output += "\n\n---\n"
    formatted_output += "**REMINDER:** This is a draft requiring human review. "
    formatted_output += "No timelines, assignments, or commitments have been made.\n"
    formatted_output += format_disclaimer()
    
    return {
        "success": True,
        "output": formatted_output,
        "error": None
    }


def get_sample_requirements_data() -> str:
    """Return sample requirements data for demonstration."""
    return """Discovery Call Notes - Client: GreenLeaf Organics

Meeting Date: Last Thursday
Attendees: Maria (CEO), James (Operations Manager), Us

Context:
GreenLeaf is a mid-size organic food distributor. They supply to ~200 restaurants and grocery stores in the metro area. Currently everything is manual - orders come in via phone, email, and sometimes text messages.

What they said they need:

Maria: "We're losing orders because things fall through the cracks. Last month we missed a $5,000 order from our biggest client because the email got buried. I need to see all orders in one place."

James: "The drivers don't know their routes until the morning. They come in, I hand them paper sheets, and they figure it out. It's chaos. We need something on their phones."

Maria: "I want to know in real-time where my trucks are. When a restaurant calls asking where their delivery is, I have to call the driver. It's embarrassing."

James: "Also inventory - we're always either overstocked on greens or running out. Can't it predict what we need?"

Maria: "Oh, and invoicing. We still mail paper invoices. It's 2024. Some clients have been asking for online payment."

Current pain points:
- Missed orders due to scattered communication channels
- No route optimization for 12 delivery trucks
- Manual inventory tracking in Excel
- Paper-based invoicing, slow payment collection
- No visibility into delivery status

Their priorities (in order per Maria):
1. Order management - consolidate everything
2. Driver mobile app with routes
3. Real-time tracking
4. "The other stuff can come later"

Budget: "We're not a tech company, so nothing crazy. But we know we need to invest to grow."

Timeline hint: Want to start pilot before summer busy season (3 months away)
"""
