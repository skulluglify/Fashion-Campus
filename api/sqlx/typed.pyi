from _typeshed import Incomplete
from sqlalchemy.engine import Compiled, Connection, Dialect, Engine, Row
from sqlalchemy.schema import DDLElement, DefaultGenerator
from sqlalchemy.sql.base import ImmutableColumnCollection
from sqlalchemy.sql.elements import BinaryExpression, UnaryExpression
from sqlalchemy.sql.expression import ClauseElement, FunctionElement
from typing import Any, List, Optional, Tuple, Union

column_t: Incomplete
column_n_t = Optional[column_t]
columns_t = Union[ImmutableColumnCollection, Tuple[column_t], List[column_t]]
columns_n_t = Optional[columns_t]
rows_t = Union[Tuple[Row], List[Row], Row]
rows_n_t = Optional[rows_t]
drows_t = Union[List[dict], dict]
drows_n_t = Optional[drows_t]
nrows_t = List[Tuple[Any, ...]]
data_t = Union[List, dict]
conn_t = Union[Engine, Connection]
stmt_t = Union[ClauseElement, FunctionElement, DDLElement, DefaultGenerator, Compiled, str]
schemas_t: Incomplete
schemas_n_t = Optional[schemas_t]
mv_copy_t: Incomplete
catch_dialect_t = Union[Dialect, conn_t]
group_by_t: Incomplete
group_by_n_t = Optional[group_by_t]
order_by_t = Union[Tuple[UnaryExpression], List[UnaryExpression]]
order_by_n_t = Optional[order_by_t]
where_clauses_t = Union[Tuple[BinaryExpression], List[BinaryExpression], BinaryExpression]
where_clauses_n_t = Optional[where_clauses_t]
