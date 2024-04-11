#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import logging
import re
from typing import List as lt


def filter_datum(
        fields: lt[str], redaction: str, message: str, separator: str) -> str:
    """method to filter words and replace them"""
    for field in fields:
        pattern = re.escape(field) + r"=([^" + re.escape(separator) + r"]+)"
        message = re.sub(pattern, field + "=" + redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: lt[str]):
        """init method"""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format method"""
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)
