"""
TODO
1. GET Product List
2. GET Product Details
3. GET Category
(OPTIONAL) all about products & categories
"""
import io
import base64
import sqlalchemy as sqlx

from flask import Blueprint, request, jsonify
from schema.meta import engine, meta
from sqlx import sqlx_easy_orm
from api.utils import get_images_url_from_column_images, run_query
from ai.impred import Impred

impred = Impred()
products_bp = Blueprint("products", __name__, url_prefix="/")

## sudah ada di router home.py
# @products_bp.route("/home/category", methods=["GET"])
# def get_category():
#     data = run_query("SELECT id, images, name as title FROM categories WHERE NOT is_deleted='true'")
#     data = {"data": data}
#     return jsonify(data), 200


@products_bp.route("/categories", methods=["GET"])
def get_categories():
    data = run_query("SELECT id, name as title FROM categories WHERE NOT is_deleted='true'")
    data = {"data": data}
    return jsonify(data), 200


@products_bp.route("/products", methods=["GET"])
def get_products():
    body = request.args
    body_sort_by, body_category, body_price, body_condition, body_product_name = "Price a_z", None, None, "new", None
    try:
        body_page = int(body["page"])
    except:
        body_page = 1
        # return jsonify({ "message": "error, page not valid" }), 400
    try:
        body_page_size = int(body["page_size"])
    except:
        body_page_size = 100
        # return jsonify({ "message": "error, page size not valid" }), 400
    try:
        body_sort_by = body["sort_by"]
    except:
        pass
    try:
        body_category = body["category"].split(",") or body.getlist("cat")
    except:
        body_category = [x["id"] for x in run_query("SELECT id FROM categories WHERE is_deleted != true")]
        # return jsonify({ "message": "error, category not valid" }), 400
        # pass
     
    min_price, max_price = 0, 10000000
    # ikut FE
    try:
        min_price = body["prcStart"]
        max_price = body["prcEnd"]
    except:
        pass
    # ikut API req
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

    if type(body_product_name) is str:

        body_product_name = body_product_name.strip()

    # data = run_query(f"SELECT * FROM products WHERE is_deleted != true AND category_id = ANY (SELECT id FROM categories WHERE is_deleted != true)")
    data = run_query(f"SELECT products.id, products.name, products.images, products.price, products.condition, products.category_id FROM products JOIN categories ON products.category_id = categories.id WHERE products.is_deleted != true AND categories.is_deleted != true")

    for i in range(len(data)):
        single_data = data[i]
        if body_product_name != None:
            if body_product_name != "":
                if not single_data["name"].lower().startswith(body_product_name.lower()):
                    data[i] = "KOSONG"
                    continue

        if body_price != None:
            if min_price <= single_data["price"] <= max_price:
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

        ## +images handler
        single_data["images"] = get_images_url_from_column_images(single_data["images"])

    # return data
    # data = set(data)
    while "KOSONG" in data:
        data.remove("KOSONG")

    if not data:
    
        out = {"data": data, "total_rows": 0}
        return jsonify(out), 200
    
    if body_sort_by[-1] == 'z':
        data.sort(key = lambda x: x["price"])
    else:
        data.sort(key = lambda x: x["price"], reverse=True)
    
    ## +image handler
    data = [{"id": item["id"], "image": item["images"][0] if len(item["images"]) > 0 else "", "title": item["name"], "price": item["price"]} for item in data]
    
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
    image_from_payload = request.json.get("image")

    if image is not None or image_from_payload is not None:

        body = ""

        if isinstance(image, str) and image != "":
            if image.startswith("data:image/"):

                header, body = image.split(",", 1)

                if ";" in header:

                    a = header.index(":")
                    b = header.index(";")

                    ext = header[a+1:b]

                    if ext not in ("image/png", "image/jpeg", "image/x-icon"):

                        return jsonify({ "message": "error, extension not supported" }), 400

            else:

                body = image

        if isinstance(image_from_payload, str) and image_from_payload != "":
            if image_from_payload.startswith("data:image/"):

                header, body = image_from_payload.split(",", 1)

                if ";" in header:

                    a = header.index(":")
                    b = header.index(";")

                    ext = header[a+1:b]

                    if ext not in ("image/png", "image/jpeg", "image/x-icon"):

                        return jsonify({ "message": "error, extension not supported" }), 400

            else:

                body = image_from_payload

        if len(body) > 0:

            try:

                data = base64.b64decode(body)
                
                buffer = io.BytesIO(data)

                cat_pred = impred.classes_predict_by_image(buffer)
                
                c = sqlx_easy_orm(engine, meta.tables.get("categories"))
                
                row = c.get(["id"], name=cat_pred)

                if row is not None:

                    return jsonify({ "message": "success, search found", "category_id": row.id }), 200
                
                return jsonify({ "message": "error, failed search" }), 400

            except:

                return jsonify({ "message": "error, search category cannot be processed" }), 200

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
