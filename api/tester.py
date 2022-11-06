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
    print(f"{COL.BOLD}{text}", end=' ')

def get_respond(route):
    link = f"{base}{route}"
    x = requests.get(link)
    return x.json(), x.status_code

def post_respond(route, body, header: dict = None):
    link = f"{base}{route}"
    x = requests.post(link, json = body) if header == None else requests.post(link, json = body, headers = header)
    return x.json(), x.status_code

def delete_respond(route, header: dict = None):
    link = f"{base}{route}"
    return x.json(), x.status_code


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
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, user already exists"} and status != 400: return sp("User Exists")
    
    data['name'], data['email'], data['phone_number'], data['password'] = '', '', '', ''
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, name not valid"} and status != 400: return sp("Null Name")

    data['name'] = 'tester'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, email not valid"} and status != 400: return sp("Null Email")

    data['email'] = 'tester@gmail.com'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, phone number not valid"} and status != 400: return sp("Null Phone")

    data['phone_number'] = '0811111111111'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, password must contain at least 8 characters"} and status != 400: return sp("Null Password")

    data['password'] = '11111111'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, password must contain a lowercase letter"} and status != 400: return sp("Lowercase Password")

    data['password'] = 'a1111111'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, password must contain an uppercase letter"} and status != 400: return sp("Uppercase Password")

    data['password'] = 'aaaaAAAA'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, password must contain a number"} and status != 400: return sp("Number Password")

    # data['password'] = 'aaaAAA111'
    # respond, status = post_respond('/sign-up', data)
    # if respond != {"message": "error, password must contain a special character"} and status != 400: return sp("Special Character Password")

    data['password'] = 'aa@@AA11'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "success, user created"} and status != 200: return sp("Create User")

    return sp("OK", "passed")


def test_signin():
    printe("Sign-in")
    data = {
        "email": "",
        "password": ""
    }
    respond, status = post_respond('/sign-in', data)
    if respond != {"message": "error, email not valid"} and status != 400: return sp("Null Email")

    data['email'] = 'admin@gmail.com'
    respond, status = post_respond('/sign-in', data)
    if respond != {"message": "error, wrong password"} and status != 400: return sp("Wrong Password")

    data['password'] = 'admin'
    try:
        respond, status = post_respond('/sign-in', data)
        if respond['message'] != "success, login success" and status != 200:
            return sp("Failed")
        global token
        token = respond['token']
        return sp("OK", "passed")
    except:
        return sp("Error Request")


def test_create_category():
    printe("Create Category")
    global token
    temp_token = '1234'
    data = {
        "category_name": ""
    }
    respond, status = post_respond('/categories', data, header = {"token": temp_token})
    if respond != {"message": "error, invalid name"} and status != 400: return sp("Null Category")

    data["category_name"] = "category_testing2"
    respond, status = post_respond('/categories', data, header = {"token": temp_token})
    if respond != {"message": "error, invalid token"} and status != 400: return sp("Wrong Token")

    temp_token = token
    data["category_name"] = "category_testing"
    respond, status = post_respond('/categories', data, header = {"token": temp_token})
    if respond != {"message": "error, category already exists"} and status != 400: return sp("Category Exists")

    data["category_name"] = "category_testing2"
    respond, status = post_respond('/categories', data, header = {"token": temp_token})
    if respond != {"message": "Category added"} and status != 200: return sp("Create Category")

    return sp("OK", "passed")


def test_update_category():
    printe("Update Category")
    global token
    temp_token = '1234'
    cat_id = run_query("SELECT category_id FROM categories WHERE name = 'category_testing2'")
    data = {
        "category_name": "",
        "category_id": ""
    }
    respond, status = post_respond(f'/categories/{cat_id}', data, header = {"token": temp_token})
    if respond != {"message": "error, invalid name"} and status != 400: return sp("Null Category")
    
    data["category_name"] = "category_testing3"
    respond, status = post_respond(f'/categories/{cat_id}', data, header = {"token": temp_token})
    if respond != {"message": "error, invalid id"} and status != 400: return sp("Null ID")

    data["category_id"] = f"{cat_id}"
    respond, status = post_respond(f'/categories/{cat_id}', data, header = {"token": temp_token})
    if respond != {"message": "Category updated"} and status != 200: return sp("Update Category")

    return sp("OK", "passed")


def test_delete_category():
    printe("Deleted Category")
    global token
    temp_token = '1234'
    cat_id = run_query("SELECT category_id FROM categories WHERE name = 'category_testing3'")

    respond, status = delete_respond(f'/categories/123123123')
    if respond != {"message": "error, invalid category"} and status != 400: return sp("Wrong ID")

    respond, status = delete_respond(f'/categories/{cat_id}')
    if respond != {"message": "Category deleted"} and status != 400: return sp("Delete Category")

    return sp("OK", "passed")


def reset_all_data_test():
    run_query("DELETE FROM users WHERE name = 'tester'", True)
    run_query("DELETE FROM categories WHERE name = 'category_testing%'", True)
    return sp("Data Has Been Reset", "passed")


def run_all_test():
    global token
    token = ''
    test_connect()
    test_signup()
    test_signin() # as Admin
    test_create_category()
    test_update_category()
    test_delete_category()
 

reset_all_data_test() # CLEARING DATA TEST FIRST
run_all_test()