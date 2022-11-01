#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from flask import Flask

import rt.regis
rt.regis.module_registry(".modules.sqlx")

from route.users import users_bp
# from route.products import products_bp
# from route.carts import carts_bp
from route.admin import admin_bp

# # just for testing
from utils import run_query, call_engine
from schema.schema import *

def create_app():
    app = Flask(__name__)

    blueprints = [ users_bp, admin_bp ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    migration_db = os.path.join(os.path.dirname(__file__), "migration.db")

    if not os.path.exists(migration_db) and not os.path.isfile(migration_db):

        try:
            if run_query("SELECT * FROM test")[0]['name'] == "CONNECTED":
                print("Server Online")
        except:
            import sys
            sys.exit("Server Offline") 

    """ RECREATE TABLES """
    # all_table = ["orders", "carts", "products", "categories", "users", "banners"]
    # all_table = ["orders", "carts", "products", "categories", "users"]
    # drop_table(all_table)

    # recreate_table_users(call_engine())
    # print("FINISHED USERS")
    # recreate_table_categories(call_engine())
    # print("FINISHED CATEGORIES")
    # recreate_table_products(call_engine())
    # print("FINISHED PRODUCTS")
    # recreate_table_carts(call_engine())
    # print("FINISHED CARTS")
    # recreate_table_orders(call_engine())
    # print("FINISHED ORDERS")
    # recreate_table_banners(call_engine())
    # print("FINISHED BANNER")

    return app

app = create_app()
