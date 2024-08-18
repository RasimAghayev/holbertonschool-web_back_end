#!/usr/bin/env python3
""" Auth model SessionAuth
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Dict, Optional
import uuid

UserType = TypeVar('UserType', bound='User')


class SessionAuth(Auth):
    """SessionAuth class for session-based authentication."""

    def __init__(self):
        """Initializes the SessionAuth class"""
        self.user_id_by_session_id: Dict = {}

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """
            Make a new Session and register in the class

            Args:
                user_id: Identificator of the user_id

            Return:
                Session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id: str = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def session_cookie(self, request=None) -> Optional[str]:
        """Returns the session cookie value"""
        if request is None:
            return None
        return request.cookies.get('_my_session_id')

    def user_id_for_session_id(self,
                               session_id: Optional[str] = None
                               ) -> Optional[str]:
        """
            Make a user ID based in session id

            Args:
                session_id: String of the session

            Return:
                User ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        user_id: Optional[str] = self.user_id_by_session_id.get(session_id)

        return user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroy the auth session if this

        Return:
            Destuction
        """
        if request is None:
            return False
        session_id: Optional[str] = self.session_cookie(request)
        if session_id is None:
            return False
        user_id: Optional[str] = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True

    def current_user(self, request=None) -> Optional[UserType]:
        """
            Take the session cookie and the user id
            and show the user

            Args:
                request: Look the request

            Return:
                User instance based in cooikie
        """
        session_id: Optional[str] = self.session_cookie(request)
        if not session_id:
            return None

        user_id: Optional[str] = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        user: Optional[UserType] = User.get(user_id)
        return user
