"""
TODO
1. Get Orders
2. Create Product
3. Update Product
4. Delete Product
5. Create Category
6. Update Category
7. Delete Category
8. Get Total Sales
"""

import os
import sqlalchemy as sqlx
from sqlx import sqlx_easy_orm, sqlx_gen_uuid

from flask import Blueprint, request, jsonify
from .supports import auth_with_token
from schema.meta import engine, meta
from api.utils import get_images_url_from_column_images, get_sort_columns, get_sort_rules, is_seller, parse_num, sqlx_rows_norm_expand, base64_to_image_file, convert_epoch_to_datetime, run_query

admin_bp = Blueprint("admin", __name__, url_prefix="")

"""
sort_by Price a_z, Price z_a

page 1

page_size 25

is_admin True(boolean)

Created_at
User_id
email

data
{
    "data": [
   	 {
   		 "id": "uuid",
   		 "title": "Nama product",
   		 "size": [
   			 "S",
   			 "M",
   			 "L"
   		 ],
   		 "created_at": "Tue, 25 august 2022",
   		 "product_detail": "lorem ipsum",
   		 "email": "raihan@gmail.com",
   		 "images_url": [
   			 "/image/image1",
   			 "/image/image2"
   		 ],
   		 "user_id": "uuid",
   		 "total": 1000
   	 }
    ]
}

"""

@admin_bp.route("/products", methods=["POST"])
def products_page():

    auth = request.headers.get("authentication")

    def products_page_main(userdata):

        if not is_seller(userdata):

            return jsonify({ "message": "error, unauthorized account" }), 401

        product_name = request.json.get("product_name")
        description = request.json.get("description")
        images = request.json.get("images") or [] ## base64 decode save as file in folder
        condition = request.json.get("condition")
        category_id = request.json.get("category")

        ctg_safe = [x["id"] for x in run_query("SELECT id FROM categories WHERE is_deleted != true")]
        
        if category_id not in ctg_safe or category_id == "":
            return jsonify({ "message": "error, category not found"}), 404
        
        price = parse_num(request.json.get("price"))
        if price in [None, 0]:
            return jsonify({ "message": "error, price hasn't been settled"}), 400

        p = sqlx_easy_orm(engine, meta.tables.get("products"))

        if type(images) is not list:

            images = [ images ]

        ## images is List<Image> as Array<String>
        for image in images:

            if type(image) is not str:

                images.remove(image)

        ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        ## default condition

        if type(condition) is None:

            condition = "New"

        if not p.get(p.c.name == product_name):

            product_id = sqlx_gen_uuid()

            for (index, image) in enumerate([*images]):

                im_filename = str(product_name + str(index)).replace(" ", "-")

                imagepath = base64_to_image_file(im_filename, image)

                if imagepath is not None:

                    ## change route from /images to /image
                    images[index] = os.path.join("/image/", os.path.basename(imagepath))
                    continue
                
                images[index] = image

            if type(condition) is str:

                condition = condition.lower()

            if p.post(
                product_id, 
                name = product_name, 
                detail = description, 
                category_id = category_id, 
                images = ",".join(images),
                price = price, 
                condition = condition, 
                is_deleted = False
            ):

                return jsonify({ "message": "Product added" }), 201

            return jsonify({ "message": "error, product fail added"}), 406 ## di tolak

        # return jsonify({ "message": "success, product has been added" }), 200
        return jsonify({ "message": "error, product already exists" }), 400

    return auth_with_token(auth, products_page_main)

@admin_bp.route("/products", methods=["PUT"])
def products_update_page():

    """
    product_name Product 1
    
    description Lorem ipsum
    
    images [image_1, image_2, image_3]
    
    condition new
    
    category category_id
    
    price 10000

    product_id product_id
    """

    auth = request.headers.get("authentication")

    def products_update_page_main(userdata):

        if not is_seller(userdata):

            return jsonify({ "message": "error, unauthorized account" }), 401

        product_id = request.json.get("product_id")
        # prd_info = run_query(f"SELECT * FROM products WHERE id = '{product_id}'")[0]
        # try:
        product_name = request.json.get("product_name")
        #     product_name = request.json.get("product_name")
        #     if product_name == "":
        #         return jsonify({ "message": "error, invalid name" }), 400
        # except:
        #     product_name = prd_info["name"]
        # try:
        description = request.json.get("description")
        #     description = request.json.get("description")
        # except:
        #     description = prd_info["detail"]
        # try:
        images = request.json.get("images")
        #     images = request.json.get("images") # or [] ## base64 decode save as file in folder
        # except:
        #     images = prd_info["images"]
        # try:
        condition = request.json.get("condition")
        #     condition = request.json.get("condition").lower()
        #     if condition not in ["new", "used"]:
        #         return jsonify({ "message": "error, invalid condition" }), 400
        # except:
        #     condition = prd_info["condition"]
        # try:
        category_id = request.json.get("category")
        #     category_id = request.json.get("category")
        ctg_safe = [x["id"] for x in run_query("SELECT id FROM categories WHERE is_deleted != true")]
        if category_id not in ctg_safe:
            return jsonify({ "message": "error, category not found"}), 404
        # except:
        #     category_id = prd_info["category_id"]
        

        if type(product_id) is not str \
            or product_id == '':
            
            return jsonify({ "message": "error, product_id not found" }), 400
        
        # try:
        price = parse_num(request.json.get("price"))
        if price <= 0:
            return jsonify({ "message": "error, invalid price" }), 400
        #     price = parse_num(request.json.get("price"))
        #     if price in [None, 0]:
        #         return jsonify({ "message": "error, price hasn't been settled" }), 400
        # except:
        #     category_id = prd_info["price"]

        p = sqlx_easy_orm(engine, meta.tables.get("products"))

        if type(images) is not list:

            images = [ images ]

        ## images is List<Image> as Array<String>
        for image in images:

            if type(image) is not str:

                images.remove(image)

        ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        product = p.get(product_id)

        if product:

            for (index, image) in enumerate([*images]):

                if image.startswith("data:"):

                    im_filename = str(product_name + str(index)).replace(" ", "-")

                    imagepath = base64_to_image_file(im_filename, image)

                    if imagepath is not None:

                        ## change route from /images to /image
                        images[index] = os.path.join("/image/", os.path.basename(imagepath))
                        continue
                    
                    images[index] = image

            if type(product_name) is None:

                product_name = product.name

            if type(description) is None:

                description = product.description

            if type(images) is None \
                or not images:

                images = get_images_url_from_column_images(product.images)

            if type(price) is None:
                
                price = product.price

            if type(condition) is None:

                condition = product.condition

            if type(condition) is str:

                condition = condition.lower()

            if p.update(
                product_id, 
                name = product_name, 
                detail = description, 
                category_id = category_id, 
                images = ",".join(images),
                price = price, 
                condition = condition
            ):

                return jsonify({ "message": "Product updated" }), 201

            return jsonify({ "message": "error, product failed to update"}), 406 ## di tolak

        return jsonify({ "message": "error, product unknown" }), 200

    return auth_with_token(auth, products_update_page_main)

@admin_bp.route("/orders", methods=["GET"])
def order_page():

    # sort_by Price a_z, Price z_a
    sort_by = request.args.get("sort_by")

    # page 1
    _page = request.args.get("page")

    # page_size 25
    _page_size = request.args.get("page_size")

    # is_admin True(boolean)
    is_admin = request.args.get("is_admin")

    # auth
    auth = request.headers.get("authentication")

    def order_page_main(userdata):

        # Created_at
        # User_id
        # email

        ##

        ##

        page = parse_num(_page) or 1
        page_size = parse_num(_page_size) or 100

        o = sqlx_easy_orm(engine, meta.tables.get("orders"))
        c = sqlx_easy_orm(engine, meta.tables.get("carts"))
        p = sqlx_easy_orm(engine, meta.tables.get("products"))
        u = sqlx_easy_orm(engine, meta.tables.get("users"))

        if is_seller(userdata):

            offset: int
            offset = (page - 1) * page_size

            rows = o.getall(
                [
                    "orders.id",
                    "orders.shipping_method",
                    "orders.status",
                    "orders.created_at",
                    "users.id",
                    "users.name",
                    "users.email",
                    "carts.id",
                    "carts.quantity",
                    "carts.size",
                    # "carts.is_deleted",
                    "products.id",
                    "products.name",
                    "products.detail",
                    "products.images",
                    "products.price",
                    "products.is_deleted",
                ],
                get_sort_columns(
                    p.table, 
                    *get_sort_rules(sort_by)
                ),
                sqlx.join(
                    o.table, 
                    u.table, 
                    o.c.get("user_id") == u.c.get("id")
                )\
                .join(
                    c.table, 
                    u.c.get("id") == c.c.get("user_id")
                )\
                .join(
                    p.table,
                    c.c.get("product_id") == p.c.get("id")
                ),

                ## order have checkout
                ## no check soft delete
                # p.c.is_deleted != True,

                c.c.is_ordered == True,
                
                offset=offset,
                size=page_size
            )

            rows = sqlx_rows_norm_expand(rows)

            ## jika data orders kosong
            if rows is None or not rows:

                return jsonify({

                    "message": "success, data kosong",
                    "data": []
                }), 200

            data = []

            for order in rows:

                # id
                # title
                # size
                # created_at
                # product_detail
                # email
                # images_url
                # user_id
                # total

                user_email = order.users.email

                status = order.status
                shipping_method = order.shipping_method
                created_at = convert_epoch_to_datetime(order.created_at)


                user = order.users
                user_id = user.id

                cart = order.carts
                cart_quantity = cart.quantity
                # size = cart.size or [ "S", "M", "L" ]
                # size = cart.size or [ "?" ]
                size = cart.size or "L"

                product = order.products

                product_detail = product.detail
                product_title = product.name
                product_price = product.price
                product_total = product_price * cart_quantity

                images_url = get_images_url_from_column_images(product.images)

                """
                    {
                        "data": [
                        {
                            "id": "order_id(uuid)",
                            "user_name": "nama user",
                            "created_at": "Tue, 25 august 2022",
                            "user_id": "uuid",
                            "user_email": "user@gmail.com",
                            "total": 1000
                        }
                        ]
                    }
                """

                data += [
                    {
                        "id": order.id,
                        "user_name": user.name,
                        "title": product_title,
                        "size": size,
                        "price": product_price,
                        "created_at": created_at,
                        "detail": product_detail,
                        "product_detail": product_detail,
                        "shipping_method": shipping_method,
                        "shipping_status": status,
                        "status": status,
                        "method": shipping_method,
                        "status": status,
                        "email": user_email,
                        "user_email": user_email,
                        "images_url": images_url,
                        "user_id": user_id,
                        "total": product_total,
                    }
                ]

            ##

            return jsonify({
                "message": "success, data bisa diambil yee",
                "data": data
            }), 200

        return jsonify({ "message": "error, selain admin belum di implemented" }), 401

    return auth_with_token(auth, order_page_main)


@admin_bp.route("/categories",methods=["POST"])
def category():
    auth = request.headers.get("Authentication")

    def create_category(userdata):
        if not is_seller(userdata):
            return jsonify({"message": "error, unauthorized account"}), 401
        try:
            id = request.json.get("id") or sqlx_gen_uuid()
            name = request.json.get("category_name")
            if name == '':
                 return jsonify({"message": "error, invalid name"}), 400
            # images = request.json.get("images") ## base64 decode save as file in folder
            is_deleted = request.json.get("is_deleted") or False
        except:
            return jsonify({"message": "Bad Request"}), 400
        
        # if type(images) is not list:
        #     images = [ images ]
        # ## images is List<Image> as Array<String>
        # for images in images:
        #     if type(images) is not str:
        #         images.remove(images)
        
        if run_query(f"SELECT * FROM categories WHERE name='{name}'") == []:
            run_query(f"INSERT INTO categories (id, name, images, is_deleted) VALUES ('{id}', '{name}', '', '{is_deleted}')", True)
            return jsonify({"message": "Category added"}), 200
        else:
            return jsonify({"message": "error, category already exists"}), 400
            
    return auth_with_token(auth, create_category)

@admin_bp.route("/categories/<string:category_id>",methods=["PUT"])
def update_category_page(category_id):
    auth = request.headers.get("Authentication")
    cat_id = category_id

    def update_category(userdata):
        if not is_seller(userdata):
            return jsonify({"message": "error, unauthorized account"}), 401
        try:
            # id = request.json.get("category_id")
            name = request.json.get("category_name")
            # images = request.json.get("images") or [] ## base64 decode save as file in folder
            # is_deleted = request.json.get("is_deleted")
        except:
            return jsonify({"message": "Bad Request"}), 400

        # if type(images) is not list:
        #     images = [ images ]
        # ## images is List<Image> as Array<String>
        # for images in images:
        #     if type(images) is not str:
        #         images.remove(images)

        if run_query(f"SELECT * FROM categories WHERE id='{cat_id}'") != []:
            run_query(f"UPDATE categories SET name='{name}' WHERE id='{cat_id}'", True)
            return jsonify({"message": "Category updated"}), 200
        else:
            return jsonify({"message": "error, invalid id"}), 400
            
    return auth_with_token(auth, update_category)

@admin_bp.route("/categories/<string:category_id>",methods=["DELETE"])
def category_id_delete(category_id):
    auth = request.headers.get("Authentication")
    cat_id = category_id

    def delete_category(userdata):
        if not is_seller(userdata):
            return jsonify({"message": "error, unauthorized account"}), 401
        # try:
        #     id = request.json.get("id")
        # except:
        #     return jsonify({"message": "Bad Request"}), 400
            
        if run_query(f"SELECT FROM categories WHERE id='{cat_id}'") != []:
            run_query(f"UPDATE categories SET is_deleted=true WHERE id='{cat_id}'", True)
            return jsonify({"message": "Category deleted"}), 200
        else:
            return jsonify({"message": "error, invalid category"}), 400
            
    return auth_with_token(auth, delete_category)

@admin_bp.route("/products/<string:product_id>",methods=["DELETE"])
def product_id_delete(product_id):
    auth = request.headers.get("Authentication")
    prd_id = product_id

    def delete_product(userdata):
        if not is_seller(userdata):
            return jsonify({"message": "error, unauthorized account"}), 401
        # try:
        #     id = request.json.get("id")
        # except:
        #     return jsonify({"message": "Bad Request"}), 400

        if run_query(f"SELECT FROM products WHERE id='{prd_id}'") != []:
            run_query(f"UPDATE products SET is_deleted=true WHERE id='{prd_id}'", True)
            return jsonify({"message": "Product deleted"}),200
        else:
            return jsonify({"message": "error, invalid product"}),400
    
    return auth_with_token(auth, delete_product)

@admin_bp.route("/sales",methods=["GET"])
def sales():
    auth = request.headers.get("Authentication")

    def get_total_sales(userdata):
        if not is_seller(userdata):
            return jsonify({"message": "error, unauthorized account"}), 401
        
        return jsonify ({ "data": { "total": userdata.balance } }), 200

    return auth_with_token(auth, get_total_sales)
