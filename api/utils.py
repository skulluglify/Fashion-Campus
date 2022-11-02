import os
from typing import Optional, Tuple, Union, List
from sqlalchemy import create_engine, text

from sqlx.typed import drows_t
from sqlx.base import DRow

def call_engine():
    
    ## DO NOT SHARE THIS INFORMATION, THANK YOU :D
    pg_creds = {
        "host": "34.87.44.95",
        "port": "5432",
        "user": "postgres",
        "pass": "asdasdasd",
        "db": "FCampus",
    }
    engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        pg_creds["user"],
        pg_creds["pass"],
        pg_creds["host"],
        pg_creds["port"],
        pg_creds["db"],
    )
    engine = create_engine(engine_uri)
    
    return engine

def call_local_engine():

    engine = create_engine("sqlite:///" + os.path.join(os.path.dirname(__file__), "migration.db"))
    return engine

def run_query(query, commit: bool = False):
    engine = call_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
        else:
            return [dict(row) for row in conn.execute(query)]


import time
import calendar
from datetime import datetime, timezone, timedelta

def get_time_epoch():
    return int(time.time())

def convert_epoch_to_datetime(the_time):
    return datetime.utcfromtimestamp(the_time) + timedelta(hours=7)

def convert_datetime_to_epoch(the_time):
    return calendar.timegm(time.strptime(str(the_time), '%Y-%m-%d %H:%M:%S'))

def get_dayname_from_datetime(the_time):
    return the_time.strftime("%a")

def get_time_epoch_exp(hours: int) -> int:

    return convert_datetime_to_epoch(convert_epoch_to_datetime(get_time_epoch()) + timedelta(hours=hours))

################################################################
################################################################

import string

def get_value(data: dict, key: str, default = None):

    return data[key] if key in data else default

class PasswordChecker(Exception):

    message: str

    def __init__(self, message: str):

        self.message = message

def check_password(password: str):

    contains_8_chars = False
    contains_1_lowercase = False
    contains_uppercase = False
    contains_numbers = False

    if 8 <= len(password):

        contains_8_chars = True

    for c in password:

        if c in string.ascii_letters:

            if c.islower():

                contains_1_lowercase = True
                continue

            if c.isupper():

                contains_uppercase = True
                continue

        if c in string.digits:

            contains_numbers = True
            continue

    if not contains_8_chars:

        raise PasswordChecker("password must contain at least 8 characters")

    if not contains_1_lowercase:

        raise PasswordChecker("password must contain a lowercase letter")

    if not contains_uppercase:

        raise PasswordChecker("password must contain an uppercase letter")

    if not contains_numbers:

        raise PasswordChecker("password must contain a number")

################################################################

import json
import jwt.utils as jwtu

def get_payload_jwt(token: str) -> dict:

    tokens = token.split(".")

    if len(tokens) == 3:

        # head, body, tail = tokens
        _, body, _ = tokens

        try:
        
            # header = json.loads(jwtu.base64url_decode(head).decode("utf-8"))
            payload = json.loads(jwtu.base64url_decode(body).decode("utf-8"))
            # sig = jwtu.base64url_decode(tail)

            # header["alg"] if "alg" in header else "HS256"
            return payload

        except Exception as _:

            pass

    return {}

################################################################

def is_num(value: str) -> bool:

    dots: int
    dots = 0

    if len(value) > 0:

        for c in value:

            if c == ".":

                if dots > 1:

                    return False

                dots += 1
                continue

            if c not in string.digits:

                return False

        return True

    return False


## no raise
def parse_num(value: str, default: int = 0) -> Union[float, int]:

    if not is_num(value):

        return default

    if value.endswith("f"):

        return float(value)

    return int(value)


########################################################################
########################################################################

def is_seller(o: DRow) -> bool:

    if type(o.type) is bool:

        return bool(o.type)

    return 0

def sqlx_rows_norm_expand(data: drows_t) -> drows_t:

    ## normalize
    if type(data) not in (tuple, list):

        data = [ data ]

    return data

def get_images_url_from_column_images(images: str) -> List[str]:

    if images != "":

        return images.split(",")

    return []

########################################################################
########################################################################

def get_sort_rules(rules: Optional[str]) -> Tuple[str, str]:

    sort_column = "price"
    sort_rule = "a_z"

    if rules is not None:
            
        sort_rules = rules.lower().split(" ")

        if len(sort_rules) > 1:

            sort_column, sort_rule = sort_rules

        else:

            sort_column = sort_rule[0]

    return sort_column, sort_rule

########################################################################

from sqlalchemy import Table
from sqlalchemy.sql.elements import UnaryExpression

def get_sort_columns(table: Table, column: str, rule: str) -> List[UnaryExpression]:

    _sort_column = table.c.get(column)
    
    sort_by_column = []

    if _sort_column is not None:
    
        sort_by_column = [ _sort_column.asc() if rule == "a_z" else _sort_column.desc() ]
        return sort_by_column

    return []
