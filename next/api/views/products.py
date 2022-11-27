#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import jwt

from db import DBInit
from fastapi import Header, Path
from pydantic import BaseModel
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
    tags=["products"], 
    responses={
        404: {
            "message": "error, not found"
        }
    }
)

@router.get("/products", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "id": "uuid",
                            "image": "string",
                            "title": "string",
                            "price": 0
                        }
                    ],
                    "total_rows": 0,
                    "message": "string"
                }
            }
        }
    }
})
def products_page(page: int, page_size: int, sort_by: str, category: str, price: str, condition: str, product_name: str):

    pass


@router.get("/categories", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "id": "uuid",
                            "title": "string"
                        }
                    ],
                    "message": "string"
                }
            }
        }
    }
})
def categories_page(page: int, page_size: int, sort_by: str, category: str, price: str, condition: str, product_name: str):

    pass


@router.get("/products/{id}", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "data": {
                        "id": "uuid",
                        "title": "string",
                        "size": [],
                        "product_detail": "string",
                        "price": 0,
                        "category_id": "uuid",
                        "category_name": "string"
                    },
                    "message": "string"
                }
            }
        }
    }
})
def get_product_page(id: str = Path(default=None)):

    pass


class SearchImage(BaseModel):

	image: str


@router.get("/products/search_image", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "category_id": "string",
                    "message": "string"
                }
            }
        }
    }
})
def search_category_page():

    pass


class AddCart(BaseModel):
	
	id: str
	quantity: int
	size: str


@router.post("/cart", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    }
})
def add_cart_page(cart: AddCart, authentication: str = Header(default=None)):

    pass


@router.get("/cart", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "id": "uuid",
                            "details": {
                                "quantity": 0,
                                "size": "string"
                            },
                            "price": 0,
                            "image": "string",
                            "name": "string"
                        }
                    ],
                    "message": "string"
                }
            }
        }
    }
})
def cart_page(authentication: str = Header(default=None)):

    pass


@router.delete("/cart/{id}", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    }
})
def remove_cart_page(id: str = Path(default=None), authentication: str = Header(default=None)):

    pass


