""" NOTE DO NOT EDIT & USE FUNCTION IN THIS FILE """
""" JUST FOR REFERENCES """

from sqlalchemy import MetaData, Table, Column, text, ForeignKey
# datatype only
from sqlalchemy import Integer, BigInteger, String, Boolean
from utils import call_engine


def drop_table(table):
    engine = call_engine()
    with engine.connect() as conn:
        for item in table:
            conn.execute(text(f"DROP TABLE IF EXISTS {item}"))
            print(f"DROPPED {item.upper()}")


def recreate_table_banners(engine):
    metadata = MetaData()
    
    banners = Table("banners", metadata,
        Column("id", String(36), primary_key=True),
        Column("title", String, unique=True, nullable=False),
        Column("image", String, nullable=False)
    )
    metadata.create_all(engine)


def recreate_table_users(engine):
    metadata = MetaData()
    # with engine.connect() as conn:
    #     conn.execute(text("DROP TABLE IF EXISTS users"))
    
    global users
    users = Table("users", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("email", String, unique=True, nullable=False),
        Column("phone", String),
        Column("password", String, nullable=False),
        Column("type", Boolean, default=False),         # False = 'buyer' AND True = 'seller'
        Column("token", String),
        Column("address", String),
        Column("country", String),
        Column("city", String),
        Column("balance", Integer, server_default=text("0"))
    )
    metadata.create_all(engine)


def recreate_table_categories(engine):
    metadata = MetaData()
    # with engine.connect() as conn:
    #     conn.execute(text("DROP TABLE IF EXISTS categories"))

    global categories
    categories = Table("categories", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, unique=True, nullable=False),
        Column("images", String, nullable=False),
        Column("is_deleted", Boolean, default=False)
    )
    metadata.create_all(engine)


def recreate_table_products(engine):
    metadata = MetaData()
    # with engine.connect() as conn:
    #     conn.execute(text("DROP TABLE IF EXISTS products"))

    global products
    products = Table("products", metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String, nullable=False),
        Column("brand", String),
        Column("detail", String),           # same as description
        Column("category_id", ForeignKey(categories.c.id)),
        Column("images", String),    # ["/image/image1", "/image/image2"]
        Column("price", Integer),
        Column("condition", String),        # new / used
        Column("is_deleted", Boolean, default=False)
    )
    metadata.create_all(engine)


def recreate_table_carts(engine):
    metadata = MetaData()
    # with engine.connect() as conn:
    #     conn.execute(text("DROP TABLE IF EXISTS carts"))

    carts = Table("carts", metadata,
        Column("id", String(36), primary_key=True),
        Column("user_id", ForeignKey(users.c.id), nullable=False),
        Column("product_id", ForeignKey(products.c.id), nullable=False),
        Column("quantity", Integer, nullable=False),
        Column("size", String, nullable=False),
        Column("is_deleted", Boolean, default=False)
    )
    metadata.create_all(engine)


def recreate_table_orders(engine):
    metadata = MetaData()
    # with engine.connect() as conn:
    #     conn.execute(text("DROP TABLE IF EXISTS orders"))

    orders = Table("orders", metadata,
        Column("id", String(36), primary_key=True),
        Column("user_id", ForeignKey(users.c.id), nullable=False),
        Column("shipping_method", String),
        Column("status", String, default="waiting"),
        Column("created_at", BigInteger, nullable=False)
    )
    metadata.create_all(engine)


""" NOTE DO NOT EDIT & USE FUNCTION IN THIS FILE """
""" JUST FOR REFERENCES """


# def recreate_table_prodcat(engine):
#     metadata = MetaData()
#     with engine.connect() as conn:
#         conn.execute(text("DROP TABLE IF EXISTS prodcat"))

#     prodcat = Table("prodcat", metadata,
#         # Table Column
#     )
#     metadata.create_all(engine)


# NOTE for normal datetime
#         Column("created_at", DateTime, server_default=func.now()),
#         Column("updated_at", DateTime, onupdate=func.now()),
#         Column("deleted_at", DateTime)

# NOTE for update if needed
# Column("updated_at", BigInteger, onupdate=text(f"{get_time_epoch()}")),