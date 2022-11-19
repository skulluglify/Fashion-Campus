#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from flask import Blueprint, jsonify, send_from_directory

images_bp = Blueprint("images", __name__, url_prefix="/image")

@images_bp.route("/<path:image_id>", methods=["GET"])
def images_page(image_id: str):

    pwd = os.environ.get("IMAGE_FOLDER") or os.getcwd()

    src = os.path.join(pwd, image_id)

    if os.path.exists(src):

        attach = send_from_directory(pwd, image_id, as_attachment=False), 200

        resp, status = attach

        if image_id.endswith(".png"):

            resp.headers["Content-Type"] = "image/png"

        if image_id.endswith(".jpg"):

            resp.headers["Content-Type"] = "image/jpeg"

        if image_id.endswith(".jpeg"):

            resp.headers["Content-Type"] = "image/jpeg"

        return resp, status

    return jsonify({

        "message": "error, image not found"
    }), 404
