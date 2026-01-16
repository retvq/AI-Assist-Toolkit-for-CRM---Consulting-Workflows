"""
Input Validators - Validate user inputs before processing
"""
from typing import Tuple, Optional
import pandas as pd
import re


def validate_text_input(
    text: str,
    min_length: int = 50,
    max_length: int = 15000,
    field_name: str = "Input"
) -> Tuple[bool, Optional[str]]:
    """
    Validate text input for processing.
    
    Args:
        text: The input text to validate
        min_length: Minimum required characters
        max_length: Maximum allowed characters
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, f"{field_name} cannot be empty. Please provide some content to analyze."
    
    cleaned_text = text.strip()
    
    if len(cleaned_text) < min_length:
        return False, (
            f"{field_name} is too short ({len(cleaned_text)} characters). "
            f"Please provide at least {min_length} characters for meaningful analysis."
        )
    
    if len(cleaned_text) > max_length:
        return False, (
            f"{field_name} is too long ({len(cleaned_text)} characters). "
            f"Maximum allowed is {max_length} characters."
        )
    
    # Check for gibberish (mostly non-alphanumeric)
    alphanumeric_ratio = sum(c.isalnum() or c.isspace() for c in cleaned_text) / len(cleaned_text)
    if alphanumeric_ratio < 0.6:
        return False, f"{field_name} appears to contain too much non-text content. Please provide readable text."
    
    return True, None


def validate_csv_file(df: pd.DataFrame) -> Tuple[bool, Optional[str], dict]:
    """
    Validate uploaded CSV file structure.
    
    Args:
        df: Pandas DataFrame from uploaded CSV
        
    Returns:
        Tuple of (is_valid, error_message, metadata)
    """
    metadata = {
        "rows": 0,
        "columns": 0,
        "column_names": []
    }
    
    if df is None:
        return False, "No data found in the uploaded file.", metadata
    
    if df.empty:
        return False, "The uploaded file is empty. Please upload a CSV with data.", metadata
    
    if len(df.columns) < 2:
        return False, "The CSV must have at least 2 columns for meaningful analysis.", metadata
    
    if len(df) < 1:
        return False, "The CSV must have at least 1 data row.", metadata
    
    if len(df) > 10000:
        return False, "The CSV has too many rows (>10,000). Please upload a smaller sample.", metadata
    
    metadata = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns)
    }
    
    return True, None, metadata


def detect_email_format(value: str) -> bool:
    """Check if a string looks like a valid email."""
    if not isinstance(value, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, value.strip()))


def detect_phone_format(value: str) -> bool:
    """Check if a string looks like a valid phone number."""
    if not isinstance(value, str):
        return False
    # Remove common separators and check if mostly digits
    cleaned = re.sub(r'[\s\-\(\)\+\.]', '', value)
    return len(cleaned) >= 7 and len(cleaned) <= 15 and cleaned.isdigit()


def detect_date_format(value: str) -> bool:
    """Check if a string looks like a date."""
    if not isinstance(value, str):
        return False
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY or DD/MM/YYYY
        r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY or DD-MM-YYYY
    ]
    return any(re.match(pattern, value.strip()) for pattern in date_patterns)
