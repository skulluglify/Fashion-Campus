#!/usr/bin/env python3
#-*- coding: utf-8 -*-


from flask import Blueprint, jsonify
from schema.meta import engine, meta
from sqlx import sqlx_easy_orm
from api.utils import sqlx_rows_norm_expand, get_images_url_from_column_images, rows_info_exclude_table_info, run_query

home_bp = Blueprint("home", __name__, url_prefix="/home")

@home_bp.route("/banner", methods=["GET"])
def banner_page():

    b = sqlx_easy_orm(engine, meta.tables.get("banners"))

    rows = b.getall()

    rows = sqlx_rows_norm_expand(rows)

    if rows is not None:

        rows = rows_info_exclude_table_info(rows)

        return jsonify({ "message": "success, banner found", "data": rows }), 200

    return jsonify({ "message": "error, banner not found" }), 400

## prefix sudah di set /home/
@home_bp.route("/category", methods=["GET"])
def category_page():

    b = sqlx_easy_orm(engine, meta.tables.get("categories"))

    # rows = b.getall(["id", "name"], b.c.is_deleted != True)
    rows = b.getall(["id", b.c.name.label("title"), "images"], b.c.is_deleted != True)
    # rows = run_query("SELECT id, images, name as title FROM categories WHERE NOT is_deleted='true'")

    rows = sqlx_rows_norm_expand(rows)

    if rows is not None:

        rows = rows_info_exclude_table_info(rows)

        data = []

        limit = 10
        
        for (index, row) in enumerate(rows):

            if index == limit:

                break

            if row["title"] in ("Ankle_Boot",):

                limit += 1
                continue

            row = dict(row)
            row["images"] = get_images_url_from_column_images(row["images"])
            row["image"] = row["images"][0] if len(row["images"]) > 0 else None

            data += [row]

        return jsonify({ "message": "success, category found", "data": data }), 200

    return jsonify({ "message": "error, category not found" }), 400