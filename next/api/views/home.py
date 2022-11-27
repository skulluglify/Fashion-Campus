#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import jwt

from db import DBInit
# from pydantic import BaseModel
from fastapi import APIRouter#, Request
# from sqlx import sqlx_easy_orm, sqlx_gen_uuid, sqlx_encrypt_pass, sqlx_comp_pass
# from sqlx.base import DRow
# from sqlx.valid import Validation
from manip import Manip
# from util import PasswordChecker, check_password, get_enhance_time_epoch

db = DBInit()
manip = Manip()
engine = db.engine
metadata = db.metadata

router = APIRouter(
    prefix="", 
    tags=["home"], 
    responses={
        404: {
            "message": "error, not found"
        }
    }
)

@router.get("/home/banner", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "id": "uuid",
                            "image": "string",
                            "title": "string"
                        }
                    ],
                    "message": "string"
                }
            }
        }
    }
})
def home_banner_page():

    pass


@router.get("/home/category", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "id": "uuid",
                            "image": "string",
                            "title": "string"
                        }
                    ],
                    "message": "string"
                }
            }
        }
    }
})
def home_category_page():

    pass