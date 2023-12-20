"""Dependencies of the API endpoints, in the FastAPI style

SPDX-FileCopyrightText: 2022 CERT.at GmbH <https://cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import typing
from typing import Generic, Optional, TypeVar

from fastapi import Depends, Header, HTTPException, Response, status

import intelmq_api.config
import intelmq_api.session as session

T = TypeVar("T")


class OneTimeDependency(Generic[T]):
    """Allows one-time explicit initialization of the dependency,
        and then returning it on every usage.

        It emulates the previous behavior that used global variables"""

    def __init__(self) -> None:
        self._value: Optional[T] = None

    def initialize(self, value: T) -> None:
        self._value = value

    def __call__(self) -> Optional[T]:
        return self._value


api_config = OneTimeDependency[intelmq_api.config.Config]()
session_store = OneTimeDependency[session.SessionStore]()


def cached_response(max_age: int):
    """Adds the cache headers to the response"""
    def _cached_response(response: Response):
        response.headers["cache-control"] = f"max-age={max_age}"
    return _cached_response


def token_authorization(authorization: typing.Union[str, None] = Header(default=None),
                        session: session.SessionStore = Depends(session_store)):
    if session is not None:
        if not authorization or not session.verify_token(authorization):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                                "Authentication Required":
                                    "Please provide valid Token verification credentials"
                                })


def startup(config: intelmq_api.config.Config):
    """A starting point to one-time initialization of necessary dependencies. This needs to
        be called by the application on the startup."""
    api_config.initialize(config)
    session_file = config.session_store
    if session_file is not None:
        session_store.initialize(session.SessionStore(str(session_file),
                                                      config.session_duration))
