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
from flask import Blueprint, request, jsonify
import jwt
from utils import run_query, get_payload_jwt, get_user_id, get_user_role

admin_page = Blueprint("admin_page", __name__, url_prefix="")

@admin_page.route("/orders", methods=["GET"])
def get_orders():
        token = request.headers.get("Authorization")
        if token:
            try:
                payload = get_payload_jwt(token)    
                user_id = get_user_id(payload)
                user_role = get_user_role(user_id)
                if user_role == "admin":
                    query = run_query('SELECT * FROM orders')
                    return jsonify(query)
                else:
                    return jsonify({"message": "You are not authorized to access this page"}),400
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Signature expired. Please log in again."}),400
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token. Please log in again."}),400
        else:
            return jsonify({"message": "Please log in to access this page"}),400
