"""Exception handlers for API

SPDX-FileCopyrightText: 2022 CERT.at GmbH <https://cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import intelmq_api.runctl as runctl


def ctl_error_handler(request: Request, exc: runctl.IntelMQCtlError):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=exc.error_dict)


def handle_generic_error(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


def register(app: FastAPI):
    """A hook to register handlers in the app. Need to be called before startup"""
    app.add_exception_handler(runctl.IntelMQCtlError, ctl_error_handler)
    app.add_exception_handler(StarletteHTTPException, handle_generic_error)
