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

def post_respond(route, something):
    link = f"{base}{route}"
    x = requests.post(link, json = something)
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

test_connect()


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
    if respond != {"message": "error, phone number not valid"} and status != 400: return sp("Null Email", "failed")
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

test_signup()
# run_query("DELETE FROM users WHERE name = 'coba2'",True)

def test_signin():
    printe("Sign-in")
    data = {
        "email": "",
        "password": ""
    }
    respond, status = post_respond('/sign-in', data)
    if respond != {"message": "error, email not valid"} and status != 400: return sp("Null Email", "failed")
    data['email'] = 'coba2@gmail.com'
    respond, status = post_respond('/sign-in', data)
    if respond != {"message": "error, wrong password"} and status != 400: return sp("wrong Password", "failed")
    data['password'] = 'aa@@AA11'
    respond, status = post_respond('/sign-in', data)
    if respond != {"message": "success, login success"} and status != 200: return sp("Success", "failed")
    return sp("OK", "passed")

test_signin()
