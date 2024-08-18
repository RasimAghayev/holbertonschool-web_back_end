#!/usr/bin/env python3
""" Module of Authentication """
from flask import request
from typing import List, TypeVar


class Auth:
    """Class to manage the API authentication"""

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

    def authorization_header(self, request=None) -> str:
        """Method that handles authorization header"""
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """Validates current user"""
        return None
