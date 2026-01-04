# -*- coding: utf-8 -*-
"""
python -m pip install "psycopg[binary,pool]>=3.3.2"
"""
import atexit
import re
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from psycopg.conninfo import make_conninfo

# ---------------- 全局配置 ----------------
_pool: ConnectionPool | None = None

DSN = make_conninfo(
    dbname          = "",
    user            = "",
    password        = "",
    host            = "",
    port            = "",
    client_encoding = 'utf8',
    options         = '-c idle_session_timeout=0 -c statement_timeout=0'
)

# ---------------- 连接池管理 ----------------
def init_db_pool(minconn: int = 1, maxconn: int = 5) -> None:
    """初始化异步连接池"""
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            conninfo=DSN,
            min_size=minconn,
            max_size=maxconn,
            kwargs={"row_factory": dict_row},
            open=False,          # 手动 open 方便捕获异常
        )
        _pool.open()
        atexit.register(close_db_pool)

def close_db_pool() -> None:
    """关闭连接池"""
    global _pool
    if _pool:
        _pool.close()
        _pool = None
init_db_pool()

# ---------------- SQL 执行 ----------------
def submit_cursor(sql: str, params: tuple | dict | None = None) -> None:
    """写操作（INSERT / UPDATE / DELETE）"""
    try:
        sql = re.sub(r'\s+', ' ', sql.strip())
        with _pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
            conn.commit()
    except Exception as e:
        raise

def query_cursor(sql: str, params: tuple | dict | None = None, one: bool = False):
    """
    读操作（SELECT）
    默认返回 list[dict]；one=True 返回单条 dict
    """
    with _pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, params)
            return (cur.fetchone() or {}) if one else cur.fetchall()# 由于dict_row 查询单行空返回空字典 查询多行空返回空列表