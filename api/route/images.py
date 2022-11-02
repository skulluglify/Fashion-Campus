#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from flask import Blueprint, jsonify, send_from_directory

images_bp = Blueprint("images", __name__, url_prefix="/images")

@images_bp.route("/<path:image_id>", methods=["GET"])
def images_page(image_id):

    pwd = os.environ.get("IMAGE_FOLDER") or os.getcwd()

    src = os.path.join(pwd, image_id)

    if os.path.exists(src):

        return send_from_directory(pwd, image_id, as_attachment=True)

    return jsonify({

        "message": "error, image not found"
    }), 404
