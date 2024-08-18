#!/usr/bin/env python3
""" Module of Authentication """
import os
from flask import request
from typing import List, TypeVar, Optional


class Auth:
    """Class to manage the API authentication"""

    def session_cookie(self, request=None) -> Optional[str]:
        """Returns the value of the session cookie from the request."""
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None

        return request.cookies.get(session_name)

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method for requiring authentication"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True

        # Normalize path by ensuring it has a trailing slash
        if path[-1] != "/":
            path += "/"

            for excluded_path in excluded_paths:
                # Handle wildcard exclusion
                if excluded_path.endswith("*"):
                    if path.startswith(excluded_path[:-1]):
                        return False
                else:
                    if not excluded_path.endswith("/"):
                        excluded_path += "/"
                    if path == excluded_path:
                        return False
            return True

    def authorization_header(self, request=None) -> Optional[str]:
        """Method that handles authorization header"""
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> None:
        """Validates current user"""
        return None
