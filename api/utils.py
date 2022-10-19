from sqlalchemy import create_engine, text

def call_engine():
    # DO NOT SHARE THIS INFORMATION, THANK YOU :D
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


def run_query(query, commit: bool = False):
    engine = call_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
        else:
            return [dict(row) for row in conn.execute(query)]
