#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

import rt.regis
rt.regis.module_registry(".modules.sqlx")

#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

import os
import uvicorn
# import pydantic
# import datetime as dt
import importlib as imports

from base import UnicornException
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from util import Global

app = FastAPI()


g = Global()

STATIC_FOLDER = g.env.get("STATIC_FOLDER") or os.path.join(g.cwd, "static")
IMAGES_FOLDER = g.env.get("IMAGE_FOLDER") or os.path.join(g.cwd, "images")

@app.get("/")
async def index_page():

    return {"message": f"success, Hello, World!"} # noqa


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):

    return JSONResponse({"message": f"error, {exc.message}"}, status_code=exc.status_code)


def mount_file_static(src: str, dist: str):

    @app.get(dist, response_class=FileResponse, responses={
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {},
                "image/x-icon": {}
            }
        }
    })
    def file_static():

        return src


mount_file_static(os.path.join(STATIC_FOLDER, "favicon.ico"), "/favicon.ico")

app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")
app.mount("/image", StaticFiles(directory=IMAGES_FOLDER), name="images")


def load_router(module: str):

    view = imports.import_module(module)

    if view is not None:

        router = getattr(view, "router", None)

        if router is not None:

            app.include_router(router)


load_router("views.users")
load_router("views.home")
load_router("views.products")


if str(__name__).upper() in ("__MAIN__",):

    config = uvicorn.Config(app, 
        host="0.0.0.0", 
        port=8080, 
        server_header=False, 
        date_header=False,
        interface='asgi3',
        debug=False, 
        reload=True, 
        workers=4, 
        headers=[
            ("Server", "ArvonServer v1.0"),
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Headers", "Authentication, Content-Type, Content-Length, Content-Encoding, Content-Language, Content-Location"),
            ("Access-Control-Allow-Methods", "GET, POST, PUT, UPDATE, DELETE"),
            ("Access-Control-Max-Age", "86400"),
        ], 
        log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()
