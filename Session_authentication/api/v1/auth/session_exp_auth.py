#!/usr/bin/env python3
"""Session Expiration Authentication module"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Expiration Authentication class"""

    def __init__(self):
        """Initializes the SessionExpAuth class"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """Creates a new session ID with expiration"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user ID for a given session ID with expiration check"""
        if session_id is None:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None
        if self.session_duration <= 0:
            return session_data['user_id']
        created_at = session_data.get('created_at')
        if created_at is None:
            return None
        if datetime.now() > created_at + timedelta(
                seconds=self.session_duration):
            del self.user_id_by_session_id[session_id]
            return None
        return session_data['user_id']
