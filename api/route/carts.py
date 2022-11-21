"""
TODO
1. Add to Cart
2. GET user Cart
3. GET Shipping Price
4. Shipping
5. Create Order
"""
import sqlalchemy as sqlx

from flask import Blueprint, request, jsonify
from schema.meta import engine, meta
from sqlx import sqlx_gen_uuid, sqlx_easy_orm
from sqlx.base import DRow
from api.utils import get_time_epoch, run_query
from .supports import auth_with_token

carts_bp = Blueprint("carts", __name__, url_prefix="/")

def get_shipping_prices(userdata: DRow):

    c = sqlx_easy_orm(engine, meta.tables.get("carts"))
    p = sqlx_easy_orm(engine, meta.tables.get("products"))

    j = sqlx.join(c.table, p.table, c.c.product_id == p.c.id)

    row = c.get(
        [
            sqlx.func.sum(p.c.price * c.c.quantity).label("total")
        ],
        [
            c.c.user_id
        ],
        j,
        user_id = userdata.id
    )

    if row is not None:

        total = row.total

        if isinstance(total, int):

            """
            regular

            < 200 15%

            >= 200 20%

            next day

            < 300 20%
            >= 300 25%
            """
            data = []

            ## flooring number

            ## regular
            regular = {
                "name": "regular",
                "price": int(total * .2 if 200 <= total else total * .15)
            }

            data += [regular]

            ## next day
            next_day = {
                "name": "next day",
                "price": int(total * .25 if 300 <= total else total * .2)
            }

            data += [next_day]

            return data, total

    return [], 0


@carts_bp.route("/cart", methods=["GET"])
def get_cart():
    auth = request.headers.get("authentication")

    def get_cart_main(userdata):
        raw_data = run_query(f"SELECT id, quantity, size, product_id FROM carts WHERE user_id = '{userdata.id}' AND is_ordered != 'true'")
        data = []
        for item in raw_data:
            product_id = item["product_id"]
            prd_dtl = run_query(f"SELECT products.price, products.name, products.images FROM products JOIN categories ON products.category_id = categories.id WHERE products.is_deleted != 'true' AND categories.is_deleted != 'true' AND products.id = '{product_id}'")
            req = {
                "id": item["id"],
                "details": {
                    "quantity": item["quantity"],
                    "size": item["size"]
                },
                "price": prd_dtl[0]["price"],
                "image": prd_dtl[0]["images"],
                "name": prd_dtl[0]["name"]
            }
            data.append(req)
        return jsonify({ "data": data, "message": "success, cart found" }), 200

    return auth_with_token(auth, get_cart_main)


@carts_bp.route("/cart/<string:cart_id>", methods=["DELETE"])
def delete_cart(cart_id):
    auth = request.headers.get("authentication")
    
    def delete_cart_main(cart_id):
        try:
            run_query(f"DELETE FROM carts WHERE id = '{cart_id}'", True)
        except:
            return jsonify({ "message": "error, item not valid"}), 400
        return jsonify({ "message": "Cart deleted"}), 200

    return auth_with_token(auth, delete_cart_main)


@carts_bp.route("/shipping_price", methods=["GET"])
def shipping_price_page():

    auth = request.headers.get("authentication")

    def shipping_price_page_main(userdata):

        data, _ = get_shipping_prices(userdata)

        if len(data) > 0:

            return jsonify({ "message": "success, shipping_price found", "data": data }), 200

        return jsonify({ "message": "error, cart kosong"}), 400

    return auth_with_token(auth, shipping_price_page_main)
