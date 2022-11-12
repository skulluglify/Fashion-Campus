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
from api.route.users import auth_with_token
from schema.meta import engine, meta
from utils import get_images_url_from_column_images, get_sort_columns, get_sort_rules, is_seller, parse_num, run_query, sqlx_rows_norm_expand, base64_to_image_file

from typing import Callable, Optional

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

            return jsonify({ "message": "error, bukan admin tidak boleh masok" }), 401

        product_name = request.json.get("product_name")
        description = request.json.get("description")
        images = request.json.get("images") or [] ## base64 decode save as file in folder
        condition = request.json.get("condition")
        category_id = request.json.get("category")
        price = parse_num(request.json.get("price"))

        p = sqlx_easy_orm(engine, meta.tables.get("products"))

        if type(images) is not list:

            images = [ images ]

        ## images is List<Image> as Array<String>
        for image in images:

            if type(image) is not str:

                images.remove(image)

        ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        if not p.get(p.c.name == product_name):

            product_id = sqlx_gen_uuid()

            for (index, image) in enumerate([*images]):

                im_filename = str(product_name + str(index)).replace(" ", "-")

                imagepath = base64_to_image_file(im_filename, image)

                if imagepath is not None:

                    images[index] = os.path.join("/images/", os.path.basename(imagepath))
                    continue
                
                images[index] = image

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

                return jsonify({ "message": "success, product added" }), 201

            return jsonify({ "message": "error, product fail added"}), 406 ## di tolak

        return jsonify({ "message": "bruh, product has been added" }), 200

    return auth_with_token(auth, products_page_main)

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

        page = parse_num(_page)
        page_size = parse_num(_page_size)

        o = sqlx_easy_orm(engine, meta.tables.get("orders"))
        c = sqlx_easy_orm(engine, meta.tables.get("carts"))
        p = sqlx_easy_orm(engine, meta.tables.get("products"))
        u = sqlx_easy_orm(engine, meta.tables.get("users"))

        if is_seller(userdata):

            offset: int
            offset = (page - 1) * page_size

            orders = o.get(
                [
                    "orders.shipping_method",
                    "orders.status",
                    "orders.created_at",
                    "users.id",
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
                
                offset=offset,
                size=page_size
            )

            orders = sqlx_rows_norm_expand(orders)

            ## jika data orders kosong
            if orders is None or not orders:

                return jsonify({

                    "message": "success, data kosong",
                    "data": []
                }), 200

            ## normalize
            orders = sqlx_rows_norm_expand(orders)

            data = []

            for order in orders:

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
                created_at = order.created_at


                user = order.users
                user_id = user.id

                cart = order.carts
                cart_id = cart.id
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

                data += [
                    {
                        "id": cart_id,
                        "title": product_title,
                        "size": size,
                        "price": product_price,
                        "created_at": created_at,
                        "detail": product_detail,
                        "product_detail": product_detail,
                        "shipping_method": shipping_method,
                        "shipping_status": status,
                        "method": shipping_method,
                        "status": status,
                        "email": user_email,
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
