#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt
import sqlalchemy as sqlx

from db import DBInit
from fastapi import status
from fastapi.responses import JSONResponse
from sqlx import sqlx_easy_orm
from sqlx.base import DRow
from typing import Callable
from util import get_payload_jwt, get_time_epoch


class Manip:

    db = DBInit()

    engine = db.engine
    metadata = db.metadata

    def json_resp(self, data: dict, code: int = 200) -> JSONResponse:

        return JSONResponse(data, status_code=code)

    def auth_with_token(self, auth, fn: Callable[[DRow], JSONResponse]) -> JSONResponse:

        if type(auth) is str:

            engine = self.engine
            metadata = self.metadata
            json_resp = self.json_resp

            if auth != "":

                timestamp = get_time_epoch()

                header = jwt.get_unverified_header(auth)
                algorithms = header["alg"] if "alg" in header else "HS256"

                payload = get_payload_jwt(auth)

                name = payload["name"] if "name" in payload else None
                expired = payload["exp"] if "exp" in payload else None

                if name is not None and expired is not None:

                    u = sqlx_easy_orm(engine, metadata.tables.get("users"))

                    userdata = u.get(name=name)

                    if userdata is not None:

                        uuid = userdata.id
                        token = userdata.token

                        if auth != token:

                            return json_resp({ "message": "error, token not accepted" }, status.HTTP_406_NOT_ACCEPTABLE)

                        try:

                            jwt.decode(auth, key=uuid, algorithms=[algorithms])

                            if expired < timestamp:

                                return json_resp({ "message": "error, token was expired" }, status.HTTP_422_UNPROCESSABLE_ENTITY)

                            return fn(userdata)

                        except jwt.ExpiredSignatureError as _:

                            return json_resp({ "message": "error, token was expired" }, status.HTTP_422_UNPROCESSABLE_ENTITY)

                        except Exception as _:

                            print(_)

                            return json_resp({ "message": "error, something get wrong" }, status.HTTP_500_INTERNAL_SERVER_ERROR)

                    return json_resp({ "message": "error, user not found" }, status.HTTP_404_NOT_FOUND)

                return json_resp({ "message": "error, token not valid" }, status.HTTP_406_NOT_ACCEPTABLE)
        
        return json_resp({ "message": "error, bad request" }, status.HTTP_400_BAD_REQUEST)

    def get_shipping_prices(self, userdata: DRow):

        engine = self.engine
        metadata = self.metadata

        c = sqlx_easy_orm(engine, metadata.tables.get("carts"))
        p = sqlx_easy_orm(engine, metadata.tables.get("products"))

        j = sqlx.join(c.table, p.table, c.c.product_id == p.c.id)

        row = c.get(
            [
                sqlx.func.sum(p.c.price * c.c.quantity).label("total")
            ],
            [
                c.c.user_id
            ],
            j,
            c.c.is_ordered != True,
            user_id = userdata.id
        )

        if row is not None:

            total = row.total

            if isinstance(total, int):

                data = []

                ## flooring number

                ## regular
                regular = {
                    "name": "regular",
                    "price": int(total * .2 if 200 <= total else total * .15)
                }

                data += [regular]

                ## next day
                next_day = {
                    "name": "next day",
                    "price": int(total * .25 if 300 <= total else total * .2)
                }

                data += [next_day]

                return data, total

        return [], 0