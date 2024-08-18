#!/usr/bin/env python3
"""Session DB Authentication module"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """Session DB Authentication class"""

    def __init__(self):
        """Initializes the SessionDBAuth class"""
        super().__init__()
        self.engine = create_engine('sqlite:///sessions.db')
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        """Creates tables if they do not exist"""
        Base.metadata.create_all(self.engine)

    def create_session(self, user_id=None):
        """Creates a new session ID and stores it in the database"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session_db = self.Session()
        session_db.add(session)
        session_db.commit()
        session_db.close()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user ID for a given session ID from the database"""
        if session_id is None:
            return None
        session_db = self.Session()
        session = session_db.query(UserSession).filter_by(
            session_id=session_id).first()
        session_db.close()
        if session is None:
            return None
        if self.session_duration > 0:
            created_at = session.created_at
            if datetime.now() > created_at + timedelta(
                    seconds=self.session_duration):
                self.destroy_session(session_id)
                return None
        return session.user_id

    def destroy_session(self, request=None):
        """Destroys a session based on the Session ID from the request cookie"""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        session_db = self.Session()
        session = session_db.query(UserSession).filter_by(
            session_id=session_id).first()
        if session:
            session_db.delete(session)
            session_db.commit()
        session_db.close()
