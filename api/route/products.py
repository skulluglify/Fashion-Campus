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
from api.utils import get_images_url_from_column_images, run_query

products_bp = Blueprint("products", __name__, url_prefix="/")

@products_bp.route("/home/category", methods=["GET"])
def get_category():
    data = run_query("SELECT id, images, name as title FROM categories WHERE NOT is_deleted='true'")
    data = {"data": data}
    return jsonify(data), 200


@products_bp.route("/categories", methods=["GET"])
def get_categories():
    data = run_query("SELECT id, name as title FROM categories WHERE NOT is_deleted='true'")
    data = {"data": data}
    return jsonify(data), 200


@products_bp.route("/products", methods=["GET"])
def get_products():
    body = request.args
    body_sort_by, body_category, body_price, body_condition, body_product_name = "Price a_z", "category_testing", None, "new", None
    try:
        body_page = int(body["page"])
    except:
        return jsonify({ "message": "error, page not valid" }), 400
    try:
        body_page_size = int(body["page_size"])
    except:
        return jsonify({ "message": "error, page size not valid" }), 400
    try:
        body_sort_by = body["sort_by"]
    except:
        pass
    try:
        body_category = body["category"].split(",")
    except:
        # return jsonify({ "message": "error, category not valid" }), 400
        pass
    try:
        body_price = body["price"]
        min_price, max_price = [int(x) for x in body_price.split(",")]
    except:
        pass
    try:
        body_condition = body["condition"].lower()
    except:
        # return jsonify({ "message": "error, condition not valid" }), 400
        pass
    try:
        body_product_name = body["product_name"]
    except:
        pass

    data = run_query(f"SELECT * FROM products WHERE NOT is_deleted='true' AND category_id = ANY(SELECT id FROM categories WHERE NOT is_deleted='true')")
    
    for i in range(len(data)):
        single_data = data[i]
        if body_product_name != None:
            if single_data["name"] != body_product_name:
                data[i] = "KOSONG"
                continue

        if body_price != None:
            if min_price <= single_data[i]["price"] <= max_price:
                pass
            else:
                data[i] = "KOSONG"
                continue

        if len(body_condition) > 5:
            pass
        else:
            if single_data["condition"].lower() != body_condition:
                data[i] = "KOSONG"
                continue

        if single_data["category_id"] not in body_category:
            data[i] = "KOSONG"
            continue

    # return data
    # data = set(data)
    while "KOSONG" in data:
        data.remove("KOSONG")
    
    if body_sort_by[-1] == 'z':
        data.sort(key = lambda x: x["price"])
    else:
        data.sort(key = lambda x: x["price"], reverse=True)
    
    data = [{"id": item["id"], "image": item["images"], "title": item["name"], "price": item["price"]} for item in data]

    def divide_chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    separated_data = list(divide_chunks(data, body_page_size))
    
    try:
        final_data = {"data": separated_data[int(body_page) - 1], "total_rows": len(data)}
    except:
        return jsonify({ "message": "error, page not found" }), 400    

    return jsonify(final_data), 200


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

@products_bp.route("/products/<string:product_id>", methods=["GET"])
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