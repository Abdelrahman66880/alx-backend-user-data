#!/usr/bin/env python3
"""
Module for authentication using Session auth
"""


from .auth import Auth

from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session Auth mechanism"""
    pass

