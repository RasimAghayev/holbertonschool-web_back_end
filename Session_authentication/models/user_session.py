#!/usr/bin/env python3
"""User Session Model"""

from models.base import Base
from sqlalchemy import Column, String


class UserSession(Base):
    """User Session class"""

    __tablename__ = 'user_sessions'

    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), primary_key=True, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new UserSession"""
        super().__init__(*args, **kwargs)
        if 'user_id' in kwargs:
            self.user_id = kwargs['user_id']
        if 'session_id' in kwargs:
            self.session_id = kwargs['session_id']
