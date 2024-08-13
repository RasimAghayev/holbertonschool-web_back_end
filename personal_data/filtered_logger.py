#!/usr/bin/env python3
""" Ofuscated and replace with regex """
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
        Args:
            fields: a list of strings representing all fields to obfuscate
            redaction: a string representing by what the
                       field will be obfuscated
            message: a string representing the log line
            separator: a string representing by which character is
                    separating all fields in the log line (message)
        Return:
            String with string ofuscated
    """
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        Description: Update the class to accept a list of strings fields
                     constructor argument.

        Implement the format method to filter values in incoming log records
        using filter_datum. Values for fields in fields should be filtered.

        DO NOT extrapolate FORMAT manually. The format method should be less
        than 5 lines long
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor Method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_datum """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)
