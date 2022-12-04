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
from api.utils import get_time_epoch, run_query, get_images_url_from_column_images, parse_num, is_num
from .supports import auth_with_token, get_shipping_prices

carts_bp = Blueprint("carts", __name__, url_prefix="/")

@carts_bp.route("/cart", methods=["POST"])
def post_cart():
    auth = request.headers.get("authentication")
    
    def post_cart_main(userdata):
        body = request.json
        try:
            prd_id = body["id"]
        except:
            return jsonify({ "message": "error, item not valid" }), 400
        try:
            if is_num(body["quantity"]):
                quantity = parse_num(body["quantity"])
                if quantity < 1:
                    return jsonify({ "message": "error, please specify the quantity" }), 400
            else:
                raise ValueError("Bruh ...")
        except:
            return jsonify({ "message": "error, quantity not valid" }), 400
        try:
            size = body["size"].upper()
            if size not in ['XS', 'S', 'M', 'L', 'XL', 'XXL']:
                return jsonify({ "message": "error, uncommon size" }), 400
        except:
            return jsonify({ "message": "error, size not valid" }), 400
        usr_id = userdata.id
        cart_id = sqlx_gen_uuid()
        check_cart = run_query(f"SELECT * FROM carts WHERE user_id = '{usr_id}' AND product_id = '{prd_id}' AND size = '{size}' AND NOT is_ordered = TRUE")
        if check_cart == []:
            run_query(f"INSERT INTO carts VALUES ('{cart_id}', '{usr_id}', '{prd_id}', {quantity}, '{size}', false)", True)
        else:
            run_query(f"UPDATE carts SET quantity = (quantity + {quantity}) WHERE user_id = '{usr_id}' AND product_id = '{prd_id}' AND size = '{size}'", True)
        return jsonify({ "message": "success, cart has been update"}), 200
    
    return auth_with_token(auth, post_cart_main)


@carts_bp.route("/cart", methods=["GET"])
def get_cart():
    auth = request.headers.get("authentication")

    def get_cart_main(userdata):
        raw_data = run_query(f"SELECT id, quantity, size, product_id FROM carts WHERE user_id = '{userdata.id}' AND is_ordered != 'true'")
        data = []
        for item in raw_data:
            product_id = item["product_id"]
            prd_dtl = run_query(f"SELECT products.price, products.name, products.images FROM products JOIN categories ON products.category_id = categories.id WHERE products.is_deleted != 'true' AND categories.is_deleted != 'true' AND products.id = '{product_id}'")
            
            images = get_images_url_from_column_images(prd_dtl[0]["images"])
            req = {
                "id": item["id"],
                "details": {
                    "quantity": item["quantity"],
                    "size": item["size"]
                },
                "price": prd_dtl[0]["price"],
                "image": images[0] if len(images) > 0 else "",
                "name": prd_dtl[0]["name"]
            }
            data.append(req)
        return jsonify({ "data": data, "message": "success, cart found" }), 200

    return auth_with_token(auth, get_cart_main)


@carts_bp.route("/cart/<string:cart_id>", methods=["DELETE"])
def delete_cart(cart_id):
    auth = request.headers.get("authentication")
    
    def delete_cart_main(userdata):
        uid = run_query(f"SELECT user_id FROM carts WHERE id = '{cart_id}'")
        if uid != []:
            if userdata.id == uid[0]["user_id"]:
                try:
                    run_query(f"DELETE FROM carts WHERE id = '{cart_id}'", True)
                except:
                    return jsonify({ "message": "error, item not valid"}), 400
                return jsonify({ "message": "Cart deleted"}), 200
            else:
                return jsonify({ "message": "error, user unauthorized"}), 400
        else:
            return jsonify({ "message": "error, item not found"}), 400

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
