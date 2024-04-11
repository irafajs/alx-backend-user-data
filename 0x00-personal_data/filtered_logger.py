#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import re
from typing import List as lt


def filter_datum(fields: lt[str], redaction: str, message: str, separator: str) -> str:
    """method to filter words and replace them"""
    for field in fields:
        pattern = re.escape(field) + r"=([^" + re.escape(separator) + r"]+)"
    return re.sub(pattern, field + "=" + redaction, message)
