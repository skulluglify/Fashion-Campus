#!/usr/bin/env python3
#-*- coding: utf-8 -*-

## IMPORT MY RT
import rt.regis

## REGISTRY MY PACKAGE
rt.regis.module_registry(".modules.sqlx")

## GO BOOM

import os

from flask import Flask

# from route.users import users.bp
# from route.products import products.bp
# from route.carts import carts.bp
# from route.admin-page import admin-page.bp

# just for testing
from utils import run_query, call_engine
from schema.schema import *

from route.users import users_bp

def create_app():
    app = Flask(__name__)

    blueprints = [ users_bp ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # for testing able to connect with db or not
    # go to Fashion-Campus/api then run "python3 main.py"

    ## Bruh, what is that, /( -_-)/

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
