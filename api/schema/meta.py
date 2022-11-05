#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from utils import call_engine, call_local_engine
from sqlalchemy import MetaData, Table, Column, String, Boolean, ForeignKey, Integer, BigInteger, text

def db_init():

    engine = call_engine()
    # engine = call_local_engine()

    metadata = MetaData()

    banners = Table("banners", metadata,
        Column("id", String(36), primary_key=True),
        Column("title", String, unique=True, nullable=False),
        Column("image", String, nullable=False)
    )

    users = Table("users", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("email", String, unique=True, nullable=False),
        Column("phone", String),
        Column("password", String, nullable=False),
        Column("type", Boolean, default=False),         # False = 'buyer' AND True = 'seller'
        Column("token", String),
        Column("address", String),
        # Column("country", String),
        Column("city", String),
        Column("balance", Integer, server_default=text("0"))
    )

    categories = Table("categories", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("images", String, nullable=False),
        Column("is_deleted", Boolean, default=False)
    )

    products = Table("products", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, nullable=False),
        # Column("brand", String),
        Column("detail", String),           # same as description
        Column("category_id", ForeignKey(categories.c.id)),
        Column("images", String),    # ["/image/image1", "/image/image2"] ## /image/image1,/image/image2
        Column("price", Integer),
        Column("condition", String),        # new / used
        Column("is_deleted", Boolean, default=False)
    )

    carts = Table("carts", metadata,
        Column("id", String(36), primary_key=True),
        Column("user_id", ForeignKey(users.c.id), nullable=False),
        Column("product_id", ForeignKey(products.c.id), nullable=False),
        Column("quantity", Integer, nullable=False),
        Column("size", String, nullable=False),
        # Column("is_deleted", Boolean, default=False)
    )

    orders = Table("orders", metadata,
        Column("id", String(36), primary_key=True),
        Column("user_id", ForeignKey(users.c.id), nullable=False),
        Column("shipping_method", String),
        Column("status", String, default="waiting"),
        Column("created_at", BigInteger, nullable=False)
    )

    metadata.create_all(engine, checkfirst=True)

    return engine, metadata

## ALREADY CALLED
engine, meta = db_init()