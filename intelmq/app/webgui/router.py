# SPDX-FileCopyrightText: 2023 IntelMQ Team
# SPDX-License-Identifier: AGPL-3.0-or-later
import collections
import pathlib

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from intelmq.app.config import Config
from intelmq.app.dependencies import app_config

router = APIRouter(default_response_class=HTMLResponse)
templates_dir = pathlib.Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=templates_dir)
Page = collections.namedtuple("Page", ["name", "title", "url", "icon_url"])


def get_pages(request: Request):
    return [
        Page(
            name="configs",
            title="Configuration",
            url=request.url_for('get_configuration'),
            icon_url=request.url_for('static', path='images/configuration.png'),
        ),
        Page(
            name="management",
            title="Management",
            url=request.url_for('get_management'),
            icon_url=request.url_for('static', path='images/management.png'),
        ),
        Page(
            name="monitor",
            title="Monitor",
            url=request.url_for('get_monitor'),
            icon_url=request.url_for('static', path='images/monitor.png'),
        ),
        Page(
            name="check",
            title="Check",
            url=request.url_for('get_check'),
            icon_url=request.url_for('static', path='images/check.png'),
        ),
        Page(
            name="about",
            title="About",
            url=request.url_for('get_about'),
            icon_url=request.url_for('static', path='images/about.png'),
        )
    ]


@router.get("/", include_in_schema=False)
async def get_index(request: Request, config: Config = Depends(app_config)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "pages": get_pages(request),
        "config": config
    })


@router.get("/configuration", include_in_schema=False)
async def get_configuration(request: Request, config: Config = Depends(app_config)):
    return templates.TemplateResponse("configuration.html", {
        "request": request,
        "pages": get_pages(request),
        "config": config
    })


@router.get("/management", include_in_schema=False)
def get_management(request: Request, config: Config = Depends(app_config)):
    return templates.TemplateResponse("management.html", {
        "request": request,
        "pages": get_pages(request),
        "config": config
    })


@router.get("/monitor", include_in_schema=False)
def get_monitor(request: Request, config: Config = Depends(app_config)):
    return templates.TemplateResponse("monitor.html", {
        "request": request,
        "pages": get_pages(request),
        "config": config
    })


@router.get("/check", include_in_schema=False)
def get_check(request: Request, config: Config = Depends(app_config)):
    return templates.TemplateResponse("check.html", {
        "request": request,
        "pages": get_pages(request),
        "config": config
    })


@router.get("/about", include_in_schema=False)
def get_about(request: Request, config: Config = Depends(app_config)):
    return templates.TemplateResponse("about.html", {
        "request": request,
        "pages": get_pages(request),
        "config": config
    })
