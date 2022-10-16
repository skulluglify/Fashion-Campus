from flask import Flask

# from route.users import users.bp
# from route.products import products.bp
# from route.carts import carts.bp
# from route.admin-page import admin-page.bp

# just for testing
from utils import run_query

def create_app():
    app = Flask(__name__)

    blueprints = []
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # for testing able to connect with db or not
    # go to Fashion-Campus/api then run "python3 main.py"
    print(run_query("SELECT * FROM categories"))
    # it should return empty list

    return app

app = create_app()