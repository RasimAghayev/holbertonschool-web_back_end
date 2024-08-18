#!/usr/bin/env python3
""" User module
"""
import hashlib
from models.base import Base
from typing import Optional


class User(Base):
    """User class"""

    def __init__(self, *args: any, **kwargs: dict[str, any]) -> None:
        """Initialize a User instance"""
        super().__init__(*args, **kwargs)
        self.email: Optional[str] = kwargs.get("email")
        self._password: Optional[str] = kwargs.get("_password")
        self.first_name: Optional[str] = kwargs.get("first_name")
        self.last_name: Optional[str] = kwargs.get("last_name")

    @property
    def password(self) -> Optional[str]:
        """Getter of the password"""
        return self._password

    @password.setter
    def password(self, pwd: Optional[str]) -> None:
        """Setter of a new password: encrypt in SHA256"""
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: Optional[str]) -> bool:
        """Validate a password"""
        if pwd is None or not isinstance(pwd, str):
            return False
        if self.password is None:
            return False
        return hashlib.sha256(
            pwd.encode()).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Display User name based on email/first_name/last_name"""
        if (self.email is None and self.first_name is None
                and self.last_name is None):
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
