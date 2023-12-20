"""Main entrypoint for the IntelMQ server application

SPDX-FileCopyrightText: 2022 CERT.at GmbH <https://cert.at>, 2023 Filip Pokorný
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import os
import gunicorn.app.base
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.workers import UvicornH11Worker

from intelmq.version import __version__
import intelmq.app.dependencies
import intelmq.app.api.exceptions

from intelmq.app.config import Config
from intelmq.app.api.router import router as api_router


class IntelMQUvicornWorker(UvicornH11Worker):
    pass


class IntelMQGunicornApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load_config(self):
        cfg = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in cfg.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


config = Config()

app = FastAPI(
    title="IntelMQ",
    version=__version__,
    root_path=os.environ.get("ROOT_PATH", ""),
)


@app.on_event("startup")
def init_app():
    intelmq.app.dependencies.startup(config)


app.add_middleware(CORSMiddleware, allow_origins=config.allow_origins, allow_methods=("GET", "POST"))
app.include_router(api_router, prefix="/api/v1")

intelmq.app.api.exceptions.register(app)


def run(host: str = None, port: int = None, debug: bool = None, workers: int = None):

    host = host if host is not None else config.host
    port = int(port) if port is not None else config.port
    debug = debug if debug is not None else config.debug
    workers = workers if workers is not None else config.workers

    if debug:
        return uvicorn.run(
            app="intelmq.app.server:app",
            host=config.host,
            reload=True,
            port=config.port,
        )

    else:
        return IntelMQGunicornApplication(
            application="intelmq.app.server:app",
            options={
                "bind": '%s:%s' % (host, port),
                "workers": workers,
                "worker_class": "intelmq.app.server.IntelMQUvicornWorker",
                "preload_app": True,
                "accesslog": str(config.access_log)
            }).run()
