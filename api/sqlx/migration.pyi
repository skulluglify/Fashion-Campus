import sqlalchemy as sqlx
from .typed import conn_t
from sqlalchemy.engine import Connection, Engine
from typing import Optional

def sqlx_migration_with_connection(conn: Connection, rbind: conn_t, metadata: Optional[sqlx.MetaData] = ..., size: int = ..., chunk: int = ..., timeout: int = ...): ...
def sqlx_migration(bind: conn_t, rbind: Engine, metadata: Optional[sqlx.MetaData] = ..., size: int = ..., chunk: int = ..., timeout: int = ...): ...
