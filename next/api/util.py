#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime as dt

from dotenv import dotenv_values
from sqlx.base import DRow

class Global:

    cwd = os.getcwd()
    pwd = os.path.dirname(__file__)
    env = dotenv_values(os.path.join(cwd, ".env"))

    def __init__(self, *args, **kwargs):

        self.env.update(os.environ)


def get_value(data: dict, key: str, default = None):

    return data[key] if key in data else default


def get_time_epoch() -> int:

    return int(dt.datetime.now(tz=dt.timezone.utc).timestamp())


def get_enhance_time_epoch(years: int = 0, month: int = 0, weeks: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0) -> int:

    days += years * 365
    days += month * 30 # /( 0_0)/ WTF.

    date = dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(
        days=days, 
        seconds=seconds, 
        microseconds=microseconds, 
        milliseconds=milliseconds, 
        minutes=minutes, 
        hours=hours, 
        weeks=weeks
    )

    return int(date.timestamp())

def get_string_time_epoch(timestamp: int) -> str:

    return dt.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

import string


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


#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

import json
from base64 import urlsafe_b64decode

def get_payload_jwt(token: str) -> dict:

    tokens = token.split(".")

    if len(tokens) == 3:

        body: str = tokens[1]
        
        pad = 4 - (len(body) % 4)
        body += "=" * pad

        try:
        
            return json.loads(urlsafe_b64decode(body).decode("utf-8"))

        except Exception as _:

            pass

    return None


#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

from typing import Union


def is_nan(a: Union[int, float]) -> bool:

    return a != a


def is_num(value: str) -> bool:

    dots: int
    dots = 0

    if len(value) > 0:

        if value.startswith("."):

            return False

        for c in value:

            if c == ".":

                if dots > 1:

                    return False

                dots += 1
                continue

            if c not in string.digits:

                return False

        if dots > 1:

            return False

        return True

    return False


def parse_num(value: Union[str, int, float], default: Union[float, int] = 0) -> Union[float, int]:

    if type(value) is str:

        value = value.strip()

        if not is_num(value):

            return default

        value = value.replace(",", "")
        value = value.replace("_", "")

        floating = False

        if value.endswith("f") or "." in value:

            value = value[:-1]
            floating = True

        value = float(value) if floating else int(value)

    return value if not is_nan(value) else default


#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

def is_seller(o: DRow) -> bool:

    if type(o.type) is bool:

        return bool(o.type)

    return False


#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

from typing import List, Optional, Tuple

def get_images_url_from_column_images(images: str) -> List[str]:

    if images != "":

        return images.split(",")

    return []


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


#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

from sqlalchemy import Table
from sqlalchemy.sql.elements import UnaryExpression

def get_sort_columns(table: Table, column: str, rule: str) -> List[UnaryExpression]:

    _sort_column = table.c.get(column)
    
    sort_by_column = []

    if _sort_column is not None:
    
        sort_by_column = [ _sort_column.asc() if rule == "a_z" else _sort_column.desc() ]
        return sort_by_column

    return []


def purify_row(row: DRow) -> dict:

    return dict([ (k.split(".").pop(), v) for (k, v) in row.items() ])


def purify_rows(rows: List[DRow]) -> List[dict]:

    return [ purify_row(row) for row in rows ]


#<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#

from base64 import b64decode

def base64_to_image_file(filename: str, context: str) -> str:

    if context.startswith("data:image/"):

        data = context.split(",", 1)

        if len(data) > 1:

            meta, b64 = data

            if len(b64) > 0:

                try:

                    a = meta.index(":")
                    b = meta.index(";")

                    mime = meta[a+1:b]

                    _, ext = mime.split("/", 1)

                    imagedir = os.environ.get("IMAGE_FOLDER") or "images"

                    os.makedirs(imagedir, mode=0o775, exist_ok=True)

                    path = os.path.join(imagedir, filename + "." + ext)

                    if not os.path.exists(path):

                        buff = b64decode(b64)

                        with open(path, "wb") as f:

                            f.seek(0)
                            f.write(buff)

                        return path

                except:

                    pass

    return None