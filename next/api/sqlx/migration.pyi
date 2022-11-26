from .typed import conn_t
from sqlalchemy import MetaData as MetaData
from sqlalchemy.engine import Connection
from typing import Optional

def sqlx_migration_with_connection(conn: Connection, rbind: conn_t, metadata: Optional[MetaData] = ..., size: int = ..., chunk: int = ..., timeout: int = ...): ...
def sqlx_migration(bind: conn_t, rbind: conn_t, metadata: Optional[MetaData] = ..., size: int = ..., chunk: int = ..., timeout: int = ...): ...
