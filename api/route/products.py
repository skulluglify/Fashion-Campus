"""
TODO
1. GET Product List
2. GET Product Details
3. GET Category
(OPTIONAL) all about products & categories
"""
import sqlalchemy as sqlx

from flask import Blueprint, request, jsonify
from schema.meta import engine, meta
from sqlx import sqlx_easy_orm
from utils import get_images_url_from_column_images

products_bp = Blueprint("products", __name__, url_prefix="/")

@products_bp.route("/products/search_image", methods=["POST"])
def search_image_page():

    image = request.args.get("image")

    if image is not None:

        if isinstance(image, str):

            if image.startswith("data:image/"):

                header, body = image.split(",", 1)

                if ";" in header:

                    a = header.index(":")
                    b = header.index(";")

                    ext = header[a+1:b]

                    if len(body) > 0:

                        ## TEAM AI

                        ##>>>>>>>>

                        ## TEAM AI

                        c = sqlx_easy_orm(engine, meta.tables.get("categories"))
                        row = c.get(["id"], name="paijo")

                        if row is not None:

                            return jsonify({ "message": "success, pencarian berhasil", "category_id": row.id }), 200

    return jsonify({ "message": "error, gagal pencarian gambar" }), 400

@products_bp.route("/products/<string:product_id>", methods=["POST"])
def product_detail_page(product_id):

    """
    id
    title
    size
    product_detail
    price
    images_url
    category_id
    category_name
    """

    p = sqlx_easy_orm(engine, meta.tables.get("products"))
    c = sqlx_easy_orm(engine, meta.tables.get("categories"))

    j = sqlx.join(p.table, c.table, p.c.category_id == c.c.id)
    
    row = p.get(
        [
            "products.id",
            "products.name",
            "products.detail",
            "products.price",
            "products.images",
            "categories.id",
            "categories.name",
        ],
        p.c.is_deleted != True, 
        j, 
        id=product_id
    )

    if row is not None:

        products = row.products
        categories = row.categories

        if products is not None:
            if categories is not None:

                data = {}

                data["id"] = products.id
                data["title"] = products.name
                data["size"] = [ "S", "M", "L", "XL" ]
                data["product_detail"] = products.detail
                data["price"] = products.price
                data["images_url"] = get_images_url_from_column_images(products.images)
                data["category_id"] = categories.id
                data["category_name"] = categories.name

                return jsonify({ "message": "success, product found", "data": data }), 200

    return jsonify({ "message": "error, product unknown" }), 400