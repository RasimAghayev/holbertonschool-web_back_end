#!/usr/bin/env python3
""" Ofuscated and replace with regex """
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            Set the format of the record
            Args:
                record: Log record of a event
            Return:
                The function overloaded to make a new log with all items
        """
        record.msg = filter_datum(self.__fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)

        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Filter and obfuscated the string
    Args:
    fields: a list of strings representing all fields to obfuscate
            ["password", "date_of_birth"]
    redaction: a string representing by what the
               field will be obfuscated
               "XXXXX"
    message: a string representing the log line
            ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;"]
            ["name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]
    separator: a string representing by which character is
            separating all fields in the log line (message)
            ";"
    Return:
    String with string ofuscated
    """
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message
