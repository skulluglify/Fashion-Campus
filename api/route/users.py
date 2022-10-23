"""
TODO
1. Sign-up
2. Sign-in with JWT
3. User Details
4. Top-up Balance
5. Get user Shipping Address
(OPTIONAL) table user need edit
"""

from multiprocessing import connection
import jwt

from flask import Blueprint, request, jsonify
from api.valid import Validation
from schema.meta import engine, meta
from sqlx import sqlx_gen_uuid, sqlx_encypt_pass, sqlx_comp_pass, sqlx_easy_orm
from utils import PasswordChecker, check_password, get_time_epoch_exp, get_value, get_payload_jwt, get_time_epoch, parse_num

from typing import Callable, Optional

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

def auth_with_token(auth: Optional[str], fn: Callable):

    if auth is not None:

        timestamp = get_time_epoch()

        header = jwt.get_unverified_header(auth)
        algorithms = header["alg"] if "alg" in header else "HS256"

        payload = get_payload_jwt(auth)
        name = payload["name"] if "name" in payload else None
        expired = payload["exp"] if "exp" in payload else None

        if name is not None and expired is not None:

            u = sqlx_easy_orm(engine, meta.tables.get("users"))

            userdata = u.get(name=name)

            if userdata is not None:

                uuid = userdata.id
                token = userdata.token

                if auth != token:

                    return jsonify({ "message": "error, token not accepted" }), 401

                try:

                    jwt.decode(auth, key=uuid, algorithms=[algorithms])

                    if expired < timestamp:

                        return jsonify({ "message": "error, token was expired" }), 400

                    return fn(userdata)

                except jwt.ExpiredSignatureError as error:

                    return jsonify({ "message": "error, token was expired" }), 400

                except Exception as _:
                    
                    pass

                return jsonify({ "message": "error, something get wrong" }), 500

            return jsonify({ "message": "error, user not found" }), 400

        return jsonify({ "message": "error, token not valid" }), 400

    return jsonify({ "message": "error, bad request" }), 400

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

                    if (u.put(id=sqlx_gen_uuid(), name=name, email=email, phone=phone_number, password=sqlx_encypt_pass(password))):

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
            "country": userdata.country,
            "city": userdata.city,
            "balance": userdata.balance,
            "message": "success, authorized"
        }

        return jsonify(data), 200

    return auth_with_token(auth, user_info_main)

@users_bp.route("/user/shipping_address", methods=["GET", "POST"])
def user_ship_address():

    auth = request.headers.get("authentication")

    def user_ship_address_main(userdata):

        if request.method == "GET":

            data = {
                "name": userdata.name,
                "phone_number": userdata.phone,
                "address": userdata.address,
                "city": userdata.city,
                "message": "success, authorized"
            }

            return jsonify(data), 200

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
                if name is not None: data["name"] = name
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

@users_bp.route("/user/balance", methods=["POST"])
def user_topup():

    auth = request.headers.get("authentication")

    def user_topup_main(userdata):

        amount = request.args.get("amount")

        if amount is not None:

            balance = parse_num(amount)
            balance += userdata.balance or 0

            u = sqlx_easy_orm(engine, meta.tables.get("users"))

            if u.update(userdata.id, balance=balance):

                return jsonify({ "message": "success, user balance was updated" }), 200

            return jsonify({ "message": "error, something get wrong" }), 500

        return jsonify({ "message": "error, amount not set" }), 400

    return auth_with_token(auth, user_topup_main)