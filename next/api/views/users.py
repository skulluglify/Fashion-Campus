#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt

from db import DBInit
from pydantic import BaseModel
from fastapi import APIRouter, Request
from sqlx import sqlx_easy_orm, sqlx_gen_uuid, sqlx_encrypt_pass, sqlx_comp_pass
from sqlx.base import DRow
from sqlx.valid import Validation
from manip import Manip
from util import PasswordChecker, check_password, get_enhance_time_epoch

db = DBInit()
manip = Manip()
engine = db.engine
metadata = db.schema()

router = APIRouter(
    prefix="", 
    tags=["users"], 
    responses={
        404: {
            "message": "error, not found"
        }
    }
)


class UserSignUp(BaseModel):

    name: str
    email: str
    phone_number: str
    password: str


@router.post("/sign-up")
def user_sign_up_page(data: UserSignUp):

    try:

        check_password(data.password)

        if not Validation.email_address(data.email):

            return manip.json_resp({"message": "email not valid"}, 400)

        if not Validation.phone_number(data.phone_number):

            return manip.json_resp({"message": "phone not valid"}, 400)

        u = sqlx_easy_orm(engine, metadata.tables.get("users"))

        if not u.get(name=data.name):

            if u.post(id=sqlx_gen_uuid(), name=data.name, email=data.email, phone=data.phone_number, password=sqlx_encrypt_pass(data.password)):

                return manip.json_resp({"message": "user created"}, 201)  

        return manip.json_resp({"message": "user already exists"}, 400)

    except PasswordChecker as err:

            return manip.json_resp({"message": err.message}, 406)


class UserSignIn(BaseModel):

    email: str
    password: str


@router.post("/sign-in")
def user_sign_up_page(data: UserSignIn):

    if not Validation.email_address(data.email):

        return manip.json_resp({ "message": "error, email not valid" }, 400)

    u = sqlx_easy_orm(engine, metadata.tables.get("users"))

    userdata = u.get(email=data.email)

    if (userdata):

        uuid = userdata.id
        name = userdata.name
        email = userdata.email
        phone = userdata.phone
        passcrypt = userdata.password
        usertype = "buyer" if not userdata.type else "seller"

        if sqlx_comp_pass(data.password, passcrypt):

            tokenjwt = jwt.encode(
                payload={
                    "name": name,
                    "exp": get_enhance_time_epoch(4)
                },
                key=uuid
            )

            if u.update(uuid, token=tokenjwt):

                return manip.json_resp({ 
                
                    "user_information": {

                        "name": name,
                        "email": email,
                        "phone_number": phone,
                        "type": usertype,
                    },
                    "token": tokenjwt,
                    "message": "success, login success" 
                })

            return manip.json_resp({ "message": "error, can`t update jwt token" }, 500)

        return manip.json_resp({ "message": "error, wrong password" }, 401)

    return manip.json_resp({ "message": "error, user not found" }, 404)


@router.get("/user")
def user_info_page(request: Request):

    auth = request.headers.get("Authentication")

    def user_info_main(userdata: DRow):

        data = {
            "name": userdata.name,
            "email": userdata.email,
            "phone_number": userdata.phone,
            "type": "seller" if userdata.type else "buyer",
            "address": userdata.address,
            "city": userdata.city,
            "balance": userdata.balance
        }

        return manip.json_resp({

            "data": data,
            "message": "success, authorized successful"
        })

    return manip.auth_with_token(auth, user_info_main)


