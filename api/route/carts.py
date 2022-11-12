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
from utils import get_time_epoch
from api.route.users import auth_with_token

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

@carts_bp.route("/shipping_price", methods=["GET"])
def shipping_price_page():

    auth = request.headers.get("authentication")

    def shipping_price_page_main(userdata):

        data, _ = get_shipping_prices(userdata)

        if len(data) > 0:

            return jsonify({ "message": "success, shipping_price found", "data": data }), 200

        return jsonify({ "message": "error, tidak bisa mengambil metode harga"}), 400

    return auth_with_token(auth, shipping_price_page_main)

@carts_bp.route("/order", methods=["POST"])
def order_page():

    auth = request.headers.get("authentication")
    shipping_method = request.json.get("shipping_method")
    shipping_address = request.json.get("shipping_address")

    def order_page_main(userdata):

        """
        shipping_method
        “Same day”
        
        shipping_address
        {
            "name": "address name",
            "phone_number": "082713626",
            "address" : "22, ciracas, east jakarta",
            "city": "Jakarta
        }
        """
        if shipping_method is not None:
            if shipping_address is not None:
        
                shipping_prices, total = get_shipping_prices(userdata)

                shipping_price_info = None

                for shipping_price in shipping_prices:

                    if shipping_price["name"] == shipping_method.lower():

                        shipping_price_info = shipping_price
                        break

                if shipping_price_info is not None:

                    name = shipping_address["name"] if "name" in shipping_address else None
                    phone_number = shipping_address["phone_number"] if "phone_number" in shipping_address else None
                    address = shipping_address["address"] if "address" in shipping_address else None
                    city = shipping_address["city"] if "city" in shipping_address else None

                    if name is None:

                        return jsonify({ "message": "error, shipping_address.name not found" }), 400

                    if phone_number is None:

                        return jsonify({ "message": "error, shipping_address.phone_number not found" }), 400

                    if address is None:

                        return jsonify({ "message": "error, shipping_address.address not found" }), 400

                    if city is None:

                        return jsonify({ "message": "error, shipping_address.city not found" }), 400

                    cost = total + shipping_price_info["price"]

                    o = sqlx_easy_orm(engine, meta.tables.get("orders"))
                    u = sqlx_easy_orm(engine, meta.tables.get("users"))
                    
                    if o.post(sqlx_gen_uuid(), userdata.id, shipping_method, "waiting", get_time_epoch()):

                        buyer = u.get(userdata.id, balance=0)
                        if buyer.balance < cost:

                            return jsonify({ "message": "error, user balance not enough" }), 400  

                        ## DEBUG
                        ## DEBUG
                        ## DEBUG

                        if u.update(buyer.id, balance=buyer.balance - cost, verify=True):

                            seller = u.get(type=True)

                            if u.update(seller.id, balance=seller.balance + cost, verify=True):

                                return jsonify({ "message": "Order success" }), 200

                        return jsonify({ "message": "error, order cannot process" }), 500

        return jsonify({ "message": "error, order failed" }), 400

    return auth_with_token(auth, order_page_main)