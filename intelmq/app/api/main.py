"""Main entrypoint for the API application

SPDX-FileCopyrightText: 2022 CERT.at GmbH <https://cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import intelmq_api.config
import intelmq_api.dependencies
import intelmq_api.exceptions

from .api import api

config = intelmq_api.config.Config(os.environ.get("INTELMQ_API_CONFIG"))

app = FastAPI(root_path=os.environ.get("ROOT_PATH", ""))


@app.on_event("startup")
def init_app():
    intelmq_api.dependencies.startup(config)


app.add_middleware(CORSMiddleware, allow_origins=config.allow_origins,
                   allow_methods=("GET", "POST"))
app.include_router(api, prefix="/v1")
intelmq_api.exceptions.register(app)
