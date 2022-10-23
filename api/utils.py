from sqlalchemy import create_engine, text

def call_engine():
    # DO NOT SHARE THIS INFORMATION, THANK YOU :D
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
from datetime import datetime, timedelta

def get_time_epoch():
    return int(time.time())

def convert_epoch_to_datetime(the_time):
    return datetime.utcfromtimestamp(the_time) + timedelta(hours=7)

def convert_datetime_to_epoch(the_time):
    return calendar.timegm(time.strptime(str(the_time), '%Y-%m-%d %H:%M:%S'))

def get_dayname_from_datetime(the_time):
    return the_time.strftime("%a")