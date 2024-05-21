import re
import streamlit as st

def extract_sql_blocks(text: str) -> str:
    """
    Extract sql code from a generated query
    """
    pattern = r'```sql\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)