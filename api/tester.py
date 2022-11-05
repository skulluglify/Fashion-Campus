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

def sp(text, condition):
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


## TEST CONNECT ##
def test_connect():
    try:
        respond, status = get_respond('/')
        if respond == {'message': 'Server Online'} and status == 200:
            return sp("CONNECTED", "passed")
    except:
        sp("NOT CONNECTED", "failed")
    sys.exit()


## TEST ENDPOINTS ##
def test_signup():
    printe("Sign-up")
    data = {
        "name": "coba",
        "email": "coba@gmail.com",
        "phone_number": "0811111111111",
        "password": "aa@@AA11"
    }
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, user already exists"} and status != 400: return sp("User Exists", "failed")
    
    data['name'], data['email'], data['phone_number'], data['password'] = '', '', '', ''
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, name not valid"} and status != 400: return sp("Null Name", "failed")
    data['name'] = 'coba2'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, email not valid"} and status != 400: return sp("Null Email", "failed")
    data['email'] = 'coba2@gmail.com'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, phone number not valid"} and status != 400: return sp("Null Phone", "failed")
    data['phone_number'] = '0811111111111'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, password must contain at least 8 characters"} and status != 400: return sp("Null Password", "failed")
    data['password'] = '11111111'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, password must contain a lowercase letter"} and status != 400: return sp("Lowercase Password", "failed")
    data['password'] = 'a1111111'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, password must contain an uppercase letter"} and status != 400: return sp("Uppercase Password", "failed")
    data['password'] = 'aaaaAAAA'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "error, password must contain a number"} and status != 400: return sp("Number Password", "failed")
    # data['password'] = 'aaaAAA111'
    # respond, status = post_respond('/sign-up', data)
    # if respond != {"message": "error, password must contain a special character"} and status != 400: return sp("Special Character Password", "failed")
    data['password'] = 'aa@@AA11'
    respond, status = post_respond('/sign-up', data)
    if respond != {"message": "success, user created"} and status != 200: return sp("Create User", "failed")
    return sp("OK", "passed")


def test_signin():
    printe("Sign-in")
    data = {
        "email": "",
        "password": ""
    }
    respond, status = post_respond('/sign-in', data)
    if respond != {"message": "error, email not valid"} and status != 400: return sp("Null Email", "failed")
    data['email'] = 'admin@gmail.com'
    respond, status = post_respond('/sign-in', data)
    if respond != {"message": "error, wrong password"} and status != 400: return sp("Wrong Password", "failed")
    data['password'] = 'admin'
    try:
        respond, status = post_respond('/sign-in', data)
        if respond['message'] != "success, login success" and status != 200:
            return sp("Failed", "failed")
        global token
        token = respond['token']
        return sp("OK", "passed")
    except:
        return sp("Error Request", "passed")


def test_create_category():
    printe("Create Category")
    global token
    temp_token = '1234'
    data = {
        "category_name": ""
    }
    respond, status = post_respond('/categories', data, header = {"token": temp_token})
    if respond != {"message": "error, category is null"} and status != 400: return sp("Null Category", "failed")
    data["category_name"] = "category_testing2"
    respond, status = post_respond('/categories', data, header = {"token": temp_token})
    if respond != {"message": "error, invalid token"} and status != 400: return sp("Wrong Token", "failed")
    temp_token = token
    data["category_name"] = "category_testing"
    respond, status = post_respond('/categories', data, header = {"token": temp_token})
    if respond != {"message": "error, category already exists"} and status != 200: return sp("Category Exists", "failed")
    data["category_name"] = "category_testing2"
    respond, status = post_respond('/categories', data, header = {"token": temp_token})
    if respond != {"message": "success, category created"} and status != 200: return sp("Create Category", "failed")
    return sp("OK", "passed")


def run_all_test():
    global token
    token = ''
    test_connect()
    test_signup()
    test_signin() # as Admin
    test_create_category()

    # run_query("DELETE FROM users WHERE name = 'coba2'") # NOTE delete buyer coba2
    # run_query("DELETE FROM categories WHERE name = 'category_testing2'") # NOTE delete category category_testing2


run_all_test()