import enum
from .base import DType
from sqlalchemy.sql.visitors import TraversibleType
from typing import Any, List

def sqlx_wrap_ddt(typed: TraversibleType) -> DType: ...
def sqlx_get_ddt(module: Any) -> List[DType]: ...

class DDT(enum.Enum):
    GENERIC: List[DType]
    FIREBIRD: List[DType]
    MSSQL: List[DType]
    MYSQL: List[DType]
    ORACLE: List[DType]
    POSTGRESQL: List[DType]
    SQLITE: List[DType]
    SYBASE: List[DType]
