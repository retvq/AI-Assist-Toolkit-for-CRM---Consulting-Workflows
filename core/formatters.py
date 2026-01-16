"""
Output Formatters - Format AI and analysis outputs for display
"""
from typing import Dict, List, Optional
from datetime import datetime


def format_draft_header() -> str:
    """Generate the standard draft header warning."""
    return """
⚠️ **DRAFT – REQUIRES HUMAN REVIEW**

_This output is AI-generated and should be verified before use._

---
"""


def format_confidence_indicator(level: str) -> str:
    """
    Format a confidence level indicator.
    
    Args:
        level: One of 'high', 'medium', 'low', 'uncertain'
    """
    indicators = {
        "high": "🟢 **High Confidence**",
        "medium": "🟡 **Medium Confidence**",
        "low": "🟠 **Low Confidence**",
        "uncertain": "🔴 **Uncertain**"
    }
    return indicators.get(level.lower(), "⚪ **Unknown**")


def format_section_header(title: str, icon: str = "📋") -> str:
    """Format a section header with icon."""
    return f"\n### {icon} {title}\n"


def format_observed_fact(fact: str) -> str:
    """Format a fact that was directly observed in the input."""
    return f"✓ _{fact}_"


def format_inference(inference: str) -> str:
    """Format an AI inference with clear labeling."""
    return f"💡 **[Inferred]** {inference}"


def format_uncertainty(item: str) -> str:
    """Format an uncertain or missing item."""
    return f"❓ {item}"


def format_action_item(action: str) -> str:
    """Format a suggested action item."""
    return f"→ {action}"


def format_data_quality_issue(
    severity: str,
    category: str,
    description: str,
    affected_count: int,
    total_count: int
) -> str:
    """
    Format a data quality issue.
    
    Args:
        severity: 'critical', 'warning', or 'info'
        category: Type of issue (e.g., 'Missing Fields')
        description: Details about the issue
        affected_count: Number of affected records
        total_count: Total number of records
    """
    severity_icons = {
        "critical": "🔴",
        "warning": "🟠",
        "info": "🔵"
    }
    icon = severity_icons.get(severity.lower(), "⚪")
    percentage = (affected_count / total_count * 100) if total_count > 0 else 0
    
    return f"""
{icon} **{category}**
- {description}
- Affected: {affected_count} records ({percentage:.1f}%)
"""


def format_user_story(
    stakeholder: str,
    goal: str,
    benefit: str,
    acceptance_criteria: List[str]
) -> str:
    """Format a user story with acceptance criteria."""
    criteria_formatted = "\n".join([f"  ✓ {c}" for c in acceptance_criteria])
    return f"""
**As a** {stakeholder}
**I want** {goal}
**So that** {benefit}

**Acceptance Criteria:**
{criteria_formatted}
"""


def format_task_breakdown(tasks: List[Dict]) -> str:
    """
    Format a task breakdown.
    
    Args:
        tasks: List of dicts with 'title' and optional 'subtasks' keys
    """
    output = []
    for i, task in enumerate(tasks, 1):
        output.append(f"☐ **Task {i}:** {task.get('title', 'Untitled')}")
        subtasks = task.get('subtasks', [])
        for subtask in subtasks:
            output.append(f"    └ {subtask}")
    return "\n".join(output)


def format_timestamp() -> str:
    """Get formatted current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_disclaimer() -> str:
    """Generate the standard footer disclaimer."""
    return f"""
---
_Generated at {format_timestamp()} | Session-only data - not stored_
"""


def format_data_readonly_notice() -> str:
    """Notice that data was not modified."""
    return """
---
⚠️ **READ-ONLY ANALYSIS** - No data was modified or stored.
"""
