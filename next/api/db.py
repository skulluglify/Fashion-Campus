#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlalchemy as sqlx

from sqlalchemy.engine import URL, Engine
from sqlalchemy.sql.expression import Executable
from sqlx.valid import Validation
from sqlx import sqlx_encrypt_pass, sqlx_gen_uuid, sqlx_comp_pass, sqlx_create_metadata, sqlx_easy_orm
from typing import List, Optional, Union
from util import Global


class DBInit:

    g = Global()
    env = g.env

    url = URL.create("postgresql+psycopg2",
            username=env.get("POSTGRESQL_USERNAME"),
            password=env.get("POSTGRESQL_PASSWORD"),
            host=env.get("POSTGRESQL_HOST"),
            port=env.get("POSTGRESQL_PORT"),
            database=env.get("POSTGRESQL_DATABASE")
        )

    engine = sqlx.create_engine(url)

    metadata = sqlx_create_metadata()

    banners = sqlx.Table("banners", metadata,
        sqlx.Column("id", sqlx.String(36), primary_key=True),
        sqlx.Column("title", sqlx.String, unique=True, nullable=False),
        sqlx.Column("image", sqlx.String, nullable=False)
    )

    users = sqlx.Table("users", metadata,
        sqlx.Column("id", sqlx.String(36), primary_key=True),
        sqlx.Column("name", sqlx.String, unique=True, nullable=False),
        sqlx.Column("email", sqlx.String, unique=True, nullable=False),
        sqlx.Column("phone", sqlx.String),
        sqlx.Column("password", sqlx.String, nullable=False),
        sqlx.Column("type", sqlx.Boolean, default=False),         # False = 'buyer' AND True = 'seller'
        sqlx.Column("token", sqlx.String),
        sqlx.Column("address", sqlx.String),
        sqlx.Column("city", sqlx.String),
        sqlx.Column("balance", sqlx.Integer, server_default=sqlx.text("0")),
        sqlx.Column("address_name", sqlx.String)
    )

    categories = sqlx.Table("categories", metadata,
        sqlx.Column("id", sqlx.String(36), primary_key=True),
        sqlx.Column("name", sqlx.String, unique=True, nullable=False),
        sqlx.Column("images", sqlx.String, nullable=False),
        sqlx.Column("is_deleted", sqlx.Boolean, default=False)
    )

    products = sqlx.Table("products", metadata,
        sqlx.Column("id", sqlx.String(36), primary_key=True),
        sqlx.Column("name", sqlx.String, nullable=False),
        sqlx.Column("detail", sqlx.String),           # same as description
        sqlx.Column("category_id", sqlx.ForeignKey(categories.c.id)),
        sqlx.Column("images", sqlx.String),    # ["/image/image1", "/image/image2"] ## /image/image1,/image/image2
        sqlx.Column("price", sqlx.Integer),
        sqlx.Column("condition", sqlx.String),        # new / used
        sqlx.Column("is_deleted", sqlx.Boolean, default=False)
    )

    carts = sqlx.Table("carts", metadata,
        sqlx.Column("id", sqlx.String(36), primary_key=True),
        sqlx.Column("user_id", sqlx.ForeignKey(users.c.id), nullable=False),
        sqlx.Column("product_id", sqlx.ForeignKey(products.c.id), nullable=False),
        sqlx.Column("quantity", sqlx.Integer, nullable=False),
        sqlx.Column("size", sqlx.String, nullable=False),
        sqlx.Column("is_ordered", sqlx.Boolean, default=False)
    )

    orders = sqlx.Table("orders", metadata,
        sqlx.Column("id", sqlx.String(36), primary_key=True),
        sqlx.Column("user_id", sqlx.ForeignKey(users.c.id), nullable=False),
        sqlx.Column("shipping_method", sqlx.String),
        sqlx.Column("name", sqlx.String),
        sqlx.Column("phone", sqlx.String),
        sqlx.Column("address", sqlx.String),
        sqlx.Column("city", sqlx.String),
        sqlx.Column("status", sqlx.String, default="waiting"),
        sqlx.Column("created_at", sqlx.BigInteger, nullable=False)
    )

    def __init__(self, *args, **kwargs):

        self.metadata.create_all(self.engine, checkfirst=True)

    def execute(self, query: Union[Executable, str], commit: bool = False) -> List[dict]:

        if isinstance(query, str):

            query = sqlx.text(query)

        with self.engine.connect() as conn:

            if not commit:
            
                return [ dict(row) for row in conn.execute(query) ]
            
            else:
            
                conn.execute(query)