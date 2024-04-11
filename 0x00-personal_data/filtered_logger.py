#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import logging
import mysql.connector
import os
import re
from typing import List as lt


LOG_FILE = 'user_data.log'
PII_FIELDS = ('name', 'email', 'phone', 'address', 'credit_card')


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


def get_logger() -> logging.Logger:
    """method to get logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """method to connect to the db using env variables"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
