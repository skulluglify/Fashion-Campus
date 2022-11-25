import requests
import sys
import rt.regis
rt.regis.module_registry(".modules.sqlx")

from utils import run_query

class COL:
    PASSED = "\033[92m\033[1m\u2713\033[0m"
    WARNING = "\033[93m\033[1m???"
    FAILED = "\033[91m\033[1m\u2717\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


base = 'http://127.0.0.1:5000'

def sp(text, condition: str = "failed"):
    cond = getattr(COL, condition.upper())
    print(f"{text} {cond}{COL.RESET}")

def printe(text):
    print(f"{COL.BOLD}{text}")
    # print(f"{COL.BOLD}{text}", end=' ')

def get_respond(route):
    link = f"{base}{route}"
    x = requests.get(link)
    return x.json(), x.status_code

def post_respond(route, body, header: dict = None):
    link = f"{base}{route}"
    x = requests.post(link, json = body) if header == None else requests.post(link, json = body, headers = header)
    return x.json(), x.status_code

def put_respond(route, body, header: dict = None):
    link = f"{base}{route}"
    x = requests.put(link, json = body) if header == None else requests.put(link, json = body, headers = header)
    return x.json(), x.status_code

def delete_respond(route, header: dict = None):
    link = f"{base}{route}"
    x = requests.delete(link) if header == None else requests.delete(link, headers = header)
    print(x.json(), x.status_code)
    return x.json(), x.status_code

def do_post(respond, status, url: str, data: dict, message: str, status_code: int, token: str = None):
    if token != None:
        respond, status = post_respond(url, data, header = {"Authentication": token})
    else:
        respond, status = post_respond(url, data)
    print(respond, status)
    if respond != {"message": message} and status != status_code: return True

def do_put(respond, status, url: str, data: dict, message: str, status_code: int, token: str = None):
    if token != None:
        respond, status = put_respond(url, data, header = {"Authentication": token})
    else:
        respond, status = put_respond(url, data)
    print(respond, status)
    if respond != {"message": message} and status != status_code: return True


## TEST CONNECT ##
def test_connect():
    try:
        respond, status = get_respond('/')
        if respond == {'message': 'Server Online'} and status == 200:
            return sp("CONNECTED", "passed")
    except:
        sp("NOT CONNECTED")
    sys.exit()


## TEST ENDPOINTS ##
def test_signup():
    printe("Sign-up")
    data = {
        "name": "tester_duplicate",
        "email": "tester_duplicate@gmail.com",
        "phone_number": "0811111111111",
        "password": "aa@@AA11"
    }
    respond, status = None, None
    if do_post(respond, status, '/sign-up', data, "error, user already exists", 400): return sp("User Exists") 
    data['name'], data['email'], data['phone_number'], data['password'] = '', '', '', ''
    if do_post(respond, status, '/sign-up', data, "error, name not valid", 400): return sp("Null Name")
    data['name'] = 'tester'
    if do_post(respond, status, '/sign-up', data, "error, email not valid", 400): return sp("Null Email") 
    data['email'] = 'tester@gmail.com'
    if do_post(respond, status, '/sign-up', data, "error, phone number not valid", 400): return sp("Null Phone")
    data['phone_number'] = '0811111111111'
    if do_post(respond, status, '/sign-up', data, "error, password must contain at least 8 characters", 400): return sp("Null Password")
    data['password'] = '11111111'
    if do_post(respond, status, '/sign-up', data, "error, password must contain a lowercase letter", 400): return sp("Lowercase Password")
    data['password'] = 'a1111111'
    if do_post(respond, status, '/sign-up', data, "error, password must contain an uppercase letter", 400): return sp("Uppercase Password")
    data['password'] = 'aaaaAAAA'
    if do_post(respond, status, '/sign-up', data, "error, password must contain a number", 400): return sp("Number Password")
    # data['password'] = 'aaaAAA111'
    # if do_post(respond, status, '/sign-up', data, "error, password must contain a special character", 400): return sp("Special Character Password")
    data['password'] = 'aa@@AA11'
    if do_post(respond, status, '/sign-up', data, "success, user created", 200): return sp("Create User")
    return sp("OK", "passed")


def test_signin():
    printe("Sign-in")
    data = {
        "email": "",
        "password": ""
    }
    respond, status = None, None
    if do_post(respond, status, '/sign-in', data, "error, email not valid", 400): return sp("Null Email")
    data['email'] = 'admin@gmail.com'
    if do_post(respond, status, '/sign-in', data, "error, wrong password", 400): return sp("Wrong Password")
    data['password'] = 'admin'

    try:
        respond, status = post_respond('/sign-in', data)
        if respond['message'] != "success, login success" and status != 200: return sp("Failed Login")
        global token
        token = respond['token']
        return sp("OK", "passed")
    except:
        return sp("Error Request")


def test_get_category():
    printe("Get Category")
    respond, status = get_respond('/home/category')
    for i in respond['data']:
        if i['id'] == 'category_testing' and i['title'] == 'category_testing':
            return sp("OK", "passed")
    return sp("Failed")


def test_create_category():
    printe("Create Category")
    global token
    temp_token = '1234'
    data = {
        "category_name": ""
    }
    respond, status = None, None
    if do_post(respond, status, '/categories', data, "error, invalid name", 400, token): return sp("Null Category")
    data["category_name"] = "category_testing_2"
    # if do_post(respond, status, '/categories', data, "error, invalid token", 400, temp_token): return sp("Wrong Token")
    data["category_name"] = "category_testing"
    if do_post(respond, status, '/categories', data, "error, category already exists", 400, token): return sp("Category Exists")
    data["category_name"] = "category_testing_2"
    if do_post(respond, status, '/categories', data, "Category added", 200, token): return sp("Create Category")
    return sp("OK", "passed")


def test_update_category():
    printe("Update Category")
    global token
    temp_token = '1234'
    cat_id = run_query("SELECT id FROM categories WHERE name = 'category_testing_2'")[0]['id']
    data = {
        "category_name": "category_testing_3"
        # "category_id": ""
    }
    respond, status = None, None
    # if do_put(respond, status, f'/categories/{cat_id}', data, "error, invalid name", 400, token): return sp("Null Category")
    # data["category_name"] = "category_testing_3"
    if do_put(respond, status, f'/categories/123123123', data, "error, invalid id", 400, token): return sp("Wrong ID")
    # data["category_id"] = f"{cat_id}"
    # if do_put(respond, status, f'/categories/{cat_id}', data, "error, invalid token", 400, temp_token): return sp("Wrong Token")
    if do_put(respond, status, f'/categories/{cat_id}', data, "Category updated", 200, token): return sp("Update Category")
    return sp("OK", "passed")


def test_delete_category():
    printe("Delete Category")
    global token
    # temp_token = '1234'
    cat_id = run_query("SELECT id FROM categories WHERE name = 'category_testing_3'")[0]['id']

    respond, status = delete_respond(f'/categories/123123123', header = {"Authentication": token})
    if respond != {"message": "error, invalid category"} and status != 400: return sp("Wrong ID")

    respond, status = delete_respond(f'/categories/{cat_id}', header = {"Authentication": token})
    if respond != {"message": "Category deleted"} and status != 200: return sp("Delete Category")
    return sp("OK", "passed")


def test_create_product():
    printe("Create Product")
    global token
    temp_token = '1234'
    data = {
        "product_name": "",
        "description": "description_testing",
        "images": "",
        "condition": "",
        "category": "",
        "price": None
    }
    respond, status = None, None
    # if do_post(respond, status, '/products', data, "error, invalid name", 400, token): return sp("Null Product")
    data["product_name"] = "product_testing"
    # if do_post(respond, status, '/products', data, "error, invalid condition", 400, token): return sp("Null Condition")
    data["condition"] = "New"
    # if do_post(respond, status, '/products', data, "error, invalid category", 400, token): return sp("Null Category")
    data["category"] = "asdasdasdasd"
    if do_post(respond, status, '/products', data, "error, category not found", 404, token): return sp("Wrong Category")
    data["category"] = "category_testing"
    if do_post(respond, status, '/products', data, "error, price hasn't been settled", 400, token): return sp("Null Price")
    data["price"] = 35000
    # if do_post(respond, status, '/products', data, "error, invalid token", 400, temp_token): return sp("Wrong Token")
    if do_post(respond, status, '/products', data, "error, product already exists", 400, token): return sp("Product Exist")
    data["product_name"] = "product_testing_2"
    if do_post(respond, status, '/products', data, "Product added", 201, token): return sp("Create Product")
    return sp("OK", "passed")


def test_update_product():
    printe("Update Products")
    global token
    temp_token = '1234'
    prd_id = run_query("SELECT id FROM products WHERE name = 'product_testing_2'")[0]['id']
    data = {
        "product_name": "",
        "description": "description_testing",
        "images": "",
        "condition": "",
        "category": "asdasdasdasd",
        "price": None,
        "product_id": f"{prd_id}"
    }
    respond, status = None, None
    if do_put(respond, status, '/products', data, "error, invalid name", 400, token): return sp("Null Product")
    data["product_name"] = "product_testing_3"
    if do_put(respond, status, '/products', data, "error, invalid condition", 400, token): return sp("Null Condition")
    data["condition"] = "new"
    # if do_put(respond, status, '/products', data, "error, invalid category", 400, token): return sp("Null Category")
    # data["category"] = ""
    if do_put(respond, status, '/products', data, "error, category not found", 400, token): return sp("Wrong Category")
    data["category"] = "category_testing"
    if do_put(respond, status, '/products', data, "error, price hasn't been settled", 400, token): return sp("Null Price")
    data["price"] = 45000
    # if do_put(respond, status, '/products', data, "error, invalid id", 400, token): return sp("Wrong ID")
    # data["product_id"] = prd_id
    # if do_put(respond, status, '/products', data, "error, invalid id", 400, temp_token): return sp("Wrong Token")
    if do_put(respond, status, '/products', data, "Product updated", 201, token): return sp("Update Product")
    return sp("OK", "passed")


def test_delete_product():
    printe("Delete Product")
    global token
    temp_token = '1234'
    cat_id = run_query("SELECT id FROM products WHERE name = 'product_testing_3'")[0]['id']

    respond, status = delete_respond(f'/products/123123123', header = {"Authentication": token})
    if respond != {"message": "error, invalid product"} and status != 400: return sp("Wrong ID")

    respond, status = delete_respond(f'/products/{cat_id}', header = {"Authentication": token})
    if respond != {"message": "Product deleted"} and status != 200: return sp("Delete Product")
    return sp("OK", "passed")



### MAIN FUNCTION, DO NOT EDIT JUST COMMENT ###

def reset_all_data_test():
    run_query("DELETE FROM users WHERE name = 'tester'", True)
    run_query("DELETE FROM categories WHERE name LIKE 'category_testing_%'", True)
    run_query("DELETE FROM products WHERE name LIKE 'product_testing_%'", True)
    return sp("Data Has Been Reset", "passed")


def run_all_test():
    global token
    token = ''
    # test_connect()
    # test_signup()
    test_signin() # as Admin
    # test_get_category()
    # test_create_category()
    # test_update_category()
    # test_delete_category()
    test_create_product()
    test_update_product()
    test_delete_product()

reset_all_data_test() # CLEARING DATA TEST FIRST
run_all_test()