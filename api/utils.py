import os
from sqlalchemy import create_engine, text

def call_engine():
    
    ## DO NOT SHARE THIS INFORMATION, THANK YOU :D
    pg_creds = {
        "host": "34.87.139.54",
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