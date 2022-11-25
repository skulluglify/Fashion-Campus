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

import views.users

from base import UnicornException
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse


app = FastAPI()

cwd = os.getcwd()

@app.get("/")
async def index_page():

    return {"message": f"success, Hello, World!"} # noqa


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):

    return JSONResponse({"message": f"error, {exc.message}"}, status_code=exc.status_code)


def mount_file_static(src: str, dist: str):

    @app.get(dist, response_class=FileResponse)
    def file_static():

        return src


mount_file_static(os.path.join(cwd, "static", "favicon.ico"), "/favicon.ico")

app.mount("/static", StaticFiles(directory=os.path.join(cwd, "static")), name="static")
app.include_router(views.users.router)


if str(__name__).upper() in ("__MAIN__",):

    config = uvicorn.Config(app, 
        host="0.0.0.0", 
        port=5000, 
        server_header=False, 
        date_header=False,
        interface='asgi3',
        debug=False, 
        reload=True, 
        workers=4, 
        headers=[
            ("Server", "ArvonServer v1.0"),
            ("Access-Control-Allow-Origin", "*")
        ], 
        log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()
