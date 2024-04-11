#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import re


def filter_datum(fields, redaction, message, separator):
    """method to filter words and replace them"""
    for field in fields:
        pattern = re.escape(field) + r"=([^" + re.escape(separator) + r"]+)"
    return re.sub(pattern, field + "=" + redaction, message)
