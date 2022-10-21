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

from flask import Blueprint, request, jsonify
from schema.meta import engine, meta
from sqlx import *
from utils import PasswordChecker, check_password, get_time_epoch_exp, get_value

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

                    else:

                        return jsonify({ "message": "error, can`t update jwt token" }), 500

                return jsonify({ "message": "error, wrong password" }), 401

            return jsonify({ "message": "error, user not found" }), 404

    return jsonify({ "message": "error, bad request" }), 400