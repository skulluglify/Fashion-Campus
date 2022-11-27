"""
TODO
1. Sign-up
2. Sign-in with JWT
3. User Details
4. Top-up Balance
5. Get user Shipping Address
(OPTIONAL) table user need edit
"""

import jwt
import sqlalchemy as sqlx

from flask import Blueprint, request, jsonify
from api.valid import Validation
from schema.meta import engine, meta
from sqlx import sqlx_gen_uuid, sqlx_encrypt_pass, sqlx_comp_pass, sqlx_easy_orm
from api.utils import PasswordChecker, check_password, get_time_epoch_exp, get_value, get_time_epoch, parse_num, get_sort_columns, get_sort_rules, convert_epoch_to_datetime, get_images_url_from_column_images, sqlx_rows_norm_expand
from .supports import auth_with_token, get_shipping_prices

users_bp = Blueprint("users", __name__, url_prefix="")

## POST ONLY
"""
http://127.0.0.1:5000/sign-up
{
    "name": "udin",
    "email": "udin@mail.co",
    "phone_number": "+62 812 345 678 89",
    "password": "Udin1234"
}

http://127.0.0.1:5000/sign-in
{
    "email": "udin@mail.co",
    "password": "Udin1234"
}
"""


################################################################################################
################################################################################################

"""
EXAMPLE:

    auth = request.headers.get("authentication")

    def user_info_main(userdata):

        name = userdata.name
        email = userdata.email
        phone = userdata.phone

        return jsonify({ "message": "success, authorized" }), 200

    return auth_with_token(auth, user_info_main)

    return jsonify({ "message": "error, bad request" }), 400
"""

################################################################################################
################################################################################################

@users_bp.route("/sign-up", methods=["POST"])
def sign_up():

    payload = request.get_json()

    if payload is not None:

        name = get_value(payload, "name")
        email = get_value(payload, "email")
        phone_number = get_value(payload, "phone_number")
        password = get_value(payload, "password")

        if name is not None and email is not None and password is not None:

            try:

                check_password(password)

                if not Validation.email_address(email):

                    return jsonify({ "message": "error, email not valid" }), 400

                if not Validation.phone_number(phone_number):

                    return jsonify({ "message": "error, phone number not valid" }), 400

                u = sqlx_easy_orm(engine, meta.tables.get("users"))

                if (not u.get(name=name)):

                    if (u.put(id=sqlx_gen_uuid(), name=name, email=email, phone=phone_number, password=sqlx_encrypt_pass(password))):

                        return jsonify({ "message": "success, user created" }), 201  

                return jsonify({ "message": "error, user already exists" }), 400

            except PasswordChecker as e:

                return jsonify({ "message": "error, " + e.message }), 400

    return jsonify({ "message": "error, bad request" }), 400

@users_bp.route("/sign-in", methods=["POST"])
def sign_in():

    payload = request.get_json()

    if payload is not None:

        email = get_value(payload, "email")
        password = get_value(payload, "password")

        if email is not None and password is not None:

            if not Validation.email_address(email):

                return jsonify({ "message": "error, email not valid" }), 400

            u = sqlx_easy_orm(engine, meta.tables.get("users"))

            userdata = u.get(email=email)

            if (userdata):

                uuid = userdata.id
                name = userdata.name
                email = userdata.email
                phone = userdata.phone
                passcrypt = userdata.password
                usertype = "buyer" if not userdata.type else "seller"

                if sqlx_comp_pass(password, passcrypt):

                    tokenjwt = jwt.encode(
                        payload={
                            "name": name,
                            "exp": get_time_epoch_exp(4) ## just 4 hours activated
                            # "exp": get_time_epoch()
                        },
                        key=uuid ## uuid was randomly generated, and static
                    )

                    if u.update(uuid, token=tokenjwt):

                        return jsonify({ 
                        
                            "user_information": {

                                "name": name,
                                "email": email,
                                "phone_number": phone,
                                "type": usertype,
                            },
                            "token": tokenjwt,
                            "message": "success, login success" 
                        }), 200

                    return jsonify({ "message": "error, can`t update jwt token" }), 500

                return jsonify({ "message": "error, wrong password" }), 401

            return jsonify({ "message": "error, user not found" }), 404

    return jsonify({ "message": "error, bad request" }), 400

@users_bp.route("/user", methods=["GET"])
def user_info():

    auth = request.headers.get("authentication")

    def user_info_main(userdata):

        data = {
            "name": userdata.name,
            "email": userdata.email,
            "phone_number": userdata.phone,
            "type": "seller" if userdata.type else "buyer",
            "address": userdata.address,
            # "country": userdata.country,
            "city": userdata.city,
            "balance": userdata.balance
        }

        return jsonify({

            "data": data,
            "message": "success, authorized"
            
        }), 200

    return auth_with_token(auth, user_info_main)

@users_bp.route("/user/shipping_address", methods=["GET", "POST"])
def user_ship_address():

    auth = request.headers.get("authentication")

    def user_ship_address_main(userdata):

        if request.method == "GET":

            data = {
                "id": userdata.id,
                "name": userdata.address_name,
                "phone_number": userdata.phone,
                "address": userdata.address,
                "city": userdata.city
            }

            return jsonify({ "data": data, "message": "success, authorized" }), 200

        if request.method == "POST":

            payload = request.get_json()

            if payload is not None:

                ## CATCH name, phone_number, address, city
                name = payload["name"] if "name" in payload else None
                phone_number = payload["phone_number"] if "phone_number" in payload else None
                address = payload["address"] if "address" in payload else None
                country = payload["country"] if "country" in payload else None
                city = payload["city"] if "city" in payload else None

                data = {}

                ## FILTERING DATA, ONLY CATCH name, phone_number, address, city
                if name is not None: data["address_name"] = name
                if phone_number is not None: data["phone"] = phone_number
                if address is not None: data["address"] = address
                if country is not None: data["country"] = country
                if city is not None: data["city"] = city

                if data:

                    u = sqlx_easy_orm(engine, meta.tables.get("users"))

                    if u.update(userdata.id, **data):

                        return jsonify({ "message": "success, user data was updated" }), 200

                    return jsonify({ "message": "error, something get wrong" }), 500  

                return jsonify({ "message": "error, payload not set" }), 400      

            return jsonify({ "message": "error, bad request" }), 400        

        return jsonify({ "message": "success, nothing todo" }), 200

    return auth_with_token(auth, user_ship_address_main)

@users_bp.route("/user/balance", methods=["GET"])
def user_balance_detail():

    auth = request.headers.get("authentication")

    def user_balance_detail_main(userdata):

        return jsonify({ "message": "success, get user balance", "data": { "balance": userdata.balance or 0 } }), 200

    return auth_with_token(auth, user_balance_detail_main)

@users_bp.route("/user/balance", methods=["POST"])
def user_topup():

    auth = request.headers.get("authentication")

    def user_topup_main(userdata):

        amount = request.args.get("amount") or request.json.get("amount")

        if amount is not None:

            balance = parse_num(amount)
            if balance <= 0:
                return jsonify({ "message": "error, invalid amount" }), 400
            balance += userdata.balance or 0

            u = sqlx_easy_orm(engine, meta.tables.get("users"))

            if u.update(userdata.id, balance=balance):

                return jsonify({ "message": "Top Up balance success" }), 200

            return jsonify({ "message": "error, something get wrong" }), 500

        return jsonify({ "message": "error, amount not set" }), 400

    return auth_with_token(auth, user_topup_main)

def user_order():

    auth = request.headers.get("authentication")

    shipping_method = request.json.get("shipping_method") or "regular"
    
    shipping_address = request.json.get("shipping_address")

    def user_order_main(userdata):

        if shipping_method not in ("same day", "next day", "regular"):

            return jsonify({ "message": "error, illegal shipping_method, use 'same day', 'next day', 'regular'" }), 400

        if type(shipping_address) is not dict:

            return jsonify({ "message": "error, type shipping_address not dictionary" }), 400

        name = shipping_address["name"] if "name" in shipping_address else None
        phone = shipping_address["phone_number"] if "phone_number" in shipping_address else None
        address = shipping_address["address"] if "address" in shipping_address else None
        city = shipping_address["city"] if "city" in shipping_address else None

        if name is None or phone is None or address is None or city is None:

            return jsonify({ "message": "error, shipping_address couldn`t to be null" }), 400

        if name == "" or phone == "" or address == "" or city == "":

            return jsonify({ "message": "error, shipping_address couldn`t empty" }), 400

        u = sqlx_easy_orm(engine, meta.tables.get("users"))
        c = sqlx_easy_orm(engine, meta.tables.get("carts"))
        o = sqlx_easy_orm(engine, meta.tables.get("orders"))

        seller = u.get(type=True)

        carts = c.getall(["id"], c.c.is_ordered != True, user_id=userdata.id)

        if not carts:

            return jsonify({ "message": "error, carts has been empty" }), 400

        shipping_prices, total = get_shipping_prices(userdata)

        if not shipping_prices:

            return jsonify({ "message": "error, maybe carts has been empty" }), 400

        shipping_price = 0

        for data in shipping_prices:

            if data["name"] == shipping_method:

                shipping_price = data["price"]
                break

        if shipping_price <= 0:

            return jsonify({ "message": "error, shipping method not found" }), 400

        total += shipping_price

        if userdata.balance < total:

            return jsonify({ "message": "error, user balance not enough" }), 400

        if o.post(sqlx_gen_uuid(), userdata.id, shipping_method, name, phone, address, city, "waiting", get_time_epoch()):
        
            if u.update(userdata.id, balance=userdata.balance - total):

                if u.update(seller.id, balance=seller.balance + total):

                    for cart in carts:

                        if not c.update(cart.id, is_ordered=True):

                            return jsonify({ "message": "error, cart cannot update data" }), 500

                    return jsonify({ "message": "success, order was successful" }), 200

                return jsonify({ "message": "error, seller cannot update data" }), 500
            
            return jsonify({ "message": "error, buyer cannot update data" }), 500
            
        return jsonify({ "message": "error, order cannot update data" }), 500

    return auth_with_token(auth, user_order_main)

## symlink
users_bp.route("/order", methods=["POST"])(user_order)
# users_bp.route("/user/order", methods=["POST"])(user_order)

def user_get_order():

    auth = request.headers.get("authentication")

    # sort_by Price a_z, Price z_a
    sort_by = request.args.get("sort_by")

    # page 1
    _page = request.args.get("page")

    # page_size 25
    _page_size = request.args.get("page_size")

    # is_admin True(boolean)
    is_admin = request.args.get("is_admin")

    def user_get_order_main(userdata):

        page = parse_num(_page) or 1
        page_size = parse_num(_page_size) or 100

        offset: int
        offset = (page - 1) * page_size

        obj_limit = {}

        if _page_size is not None:

            obj_limit["offset"] = offset
            obj_limit["size"] = page_size

        """
        [
            {
            "id": "uuid",
            "created_at": "Mon, 22 august 2022",
            "products": [
                {
                    "id": "uuid",
                    "details": {
                        "quantity": 100,
                        "size": "M"
                    },
                    "price": 10000,
                    "image": "/url/image.jpg",
                    "name": "Product a"
                }
            ],
            "shipping_method": "same day",
            "shipping_address": {
                "name": "address name",
                "phone_number": "082713626",
                "address": "22, ciracas, east jakarta",
                "city": "Jakarta"
            }
            }
        ]

        """

        data = []

        u = sqlx_easy_orm(engine, meta.tables.get("users"))
        c = sqlx_easy_orm(engine, meta.tables.get("carts"))
        p = sqlx_easy_orm(engine, meta.tables.get("products"))
        o = sqlx_easy_orm(engine, meta.tables.get("orders"))

        j = sqlx.join(u.table, c.table, u.c.id == c.c.user_id)\
        .join(o.table, u.c.id == o.c.user_id)\
        .join(p.table, c.c.product_id == p.c.id)

        rows = u.getall(
            [
                "carts.id",
                "carts.quantity",
                "carts.size",
                "orders.created_at",
                "orders.id",
                "orders.shipping_method",
                "orders.name",
                "orders.phone",
                "orders.address",
                "orders.city",
                "products.id",
                "products.price",
                "products.images",
                "products.name",
            ],

            get_sort_columns(
                p.table, 
                *get_sort_rules(sort_by)
            ),
            
            c.c.is_ordered == True,
            u.c.user_id == userdata.id,

            j,

            **obj_limit
        )

        rows = sqlx_rows_norm_expand(rows)

        for row in rows:

            cart = {}

            n = len(data)

            carts = row.carts
            orders = row.orders
            products = row.products

            x = -1

            ## get current cart & update cart
            for i in range(n):

                if data[i]["id"] == orders.id:

                    cart = data[i]
                    x = i
                    break

            created_at = convert_epoch_to_datetime(orders.created_at)
            
            cart["id"] = orders.id
            cart["created_at"] = created_at
            
            if "products" not in cart:
            
                cart["products"] = []

            image = None
            images = get_images_url_from_column_images(products.images)

            if len(images) > 0:

                image = images[0]

            # find = False

            # for product in cart["products"]:

            #     if product["name"] == products.name:

            #         find = True
            #         break

            # if not find:
            #     cart["products"] += [{
            #         "id": carts.id,
            #         "details": {
            #             "quantity": carts.quantity,
            #             "size": carts.size,
            #         },
            #         "price": products.price,
            #         "image": image,
            #         "name": products.name,
            #     }]

            cart["products"] += [{
                "id": carts.id,
                "details": {
                    "quantity": carts.quantity,
                    "size": carts.size,
                },
                "price": products.price,
                "image": image,
                "name": products.name,
            }]

            cart["shipping_method"] = orders.shipping_method
            cart["shipping_address"] = {
                "name": orders.name,
                "phone_number": orders.phone,
                "address": orders.address,
                "city": orders.city
            }

            if 0 <= x:

                data[x] = cart

            else:

                data += [cart]

        if not data:

            return jsonify({ "data": data, "message": "success, data empty" }), 200

        return jsonify({ "data": data, "message": "success, yeah boiii" }), 200

    return auth_with_token(auth, user_get_order_main)

## symlink
# users_bp.route("/order", methods=["GET"])(user_get_order)
users_bp.route("/user/order", methods=["GET"])(user_get_order)
