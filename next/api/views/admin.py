#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import jwt

from db import DBInit
from pydantic import BaseModel
from fastapi import APIRouter, Header, Path#, Request
# from sqlx import sqlx_easy_orm, sqlx_gen_uuid, sqlx_encrypt_pass, sqlx_comp_pass
# from sqlx.base import DRow
# from sqlx.valid import Validation
from manip import Manip
# from util import PasswordChecker, check_password, get_enhance_time_epoch
from typing import List

db = DBInit()
manip = Manip()
engine = db.engine
metadata = db.metadata

router = APIRouter(
    prefix="", 
    tags=["admin"], 
    responses={
        404: {
            "message": "error, not found"
        }
    }
)

@router.get("/user/order", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "id": "uuid",
                            "user_name": "string",
                            "created_at": "string",
                            "user_id": "uuid",
                            "user_email": "string",
                            "total": 0
                        }
                    ],
                    "message": "string"
                }
            }
        }
    }
})
def orders_page(sort_by: str, page: int, page_size: int, authentication: str = Header(default=None)):

    pass


class AddProduct(BaseModel):
    product_name: str
    description: str
    images: List[str]
    condition: str
    category: str
    price: int


@router.post("/products", responses={
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
def add_product_page(product: AddProduct, authentication: str = Header(default=None)):

    pass


class ProductUpdate(BaseModel):
    product_name: str
    description: str
    images: List[str]
    condition: str
    category: str
    price: int
    product_id: int


@router.put("/products", responses={
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
def product_update_page(product: ProductUpdate, authentication: str = Header(default=None)):

    pass



@router.delete("/products/{id}", responses={
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
def remove_product_page(id: str = Path(default=None), authentication: str = Header(default=None)):

    pass


class Category(BaseModel):
    category_name: str


@router.post("/categories", responses={
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
def add_category_page(category: Category, authentication: str = Header(default=None)):

    pass


@router.put("/categories/{id}", responses={
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
def category_update_page(category: Category, id: str = Path(default=None), authentication: str = Header(default=None)):

    pass


@router.delete("/categories/{id}", responses={
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
def remove_category_page(id: str = Path(default=None), authentication: str = Header(default=None)):

    pass


@router.get("/sales", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "data": {
                        "total": 0
                    },
                    "message": "string"
                }
            }
        }
    }
})
def get_sales_page(category: Category, id: str = Path(default=None), authentication: str = Header(default=None)):

    pass

