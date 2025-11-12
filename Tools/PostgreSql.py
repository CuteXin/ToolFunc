"""
- 2025年11月12日
- pg数据库操作封装
- 依赖 psycopg2
- 使用方法见最后
"""
import json
import atexit
from psycopg2 import pool

# 全局连接池
_pg_pool    = None
dbname      = ""
host        = ""
port        = ""
user        = ""
password    = ""
dataurl     = ""

#-----数据库管理方法-----#
def init_db_pool(minconn=1, maxconn=5):
    """初始化数据库连接池"""
    global _pg_pool
    if _pg_pool is None:
        _pg_pool = pool.SimpleConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            dsn=f"dbname={dbname} user={user} password={password} host={host} port={port} client_encoding=utf8"
        )
        atexit.register(close_db_pool)

def close_db_pool():
    """关闭数据库连接池"""
    global _pg_pool
    if _pg_pool:
        _pg_pool.closeall()
        _pg_pool = None

def get_db_connection():
    """从连接池获取数据库连接"""
    global _pg_pool
    if _pg_pool is None:
        init_db_pool()
    return _pg_pool.getconn()

def put_db_connection(conn):
    """将连接放回连接池"""
    global _pg_pool
    if _pg_pool is not None:
        _pg_pool.putconn(conn)

def submit_cursor(sql:str,params:tuple|dict=None):
    """
    修改类语句
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql,params)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            put_db_connection(conn)


def query_cursor(sql:str,params:tuple|dict=None,one=False):
    """查询类语句"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql,params)
            if one:
                return cur.fetchone()
            return cur.fetchall()
    finally:
        if conn:
            put_db_connection(conn)

#-----具体方法-----#
def save_login_data(name: str, logindata: dict):
    """写入一条登录配置数据"""
    logindata = json.dumps(logindata)
    submit_cursor("""
        INSERT INTO logindata(name, logindata)
        VALUES (%s, %s)
        ON CONFLICT (name)
        DO UPDATE SET logindata = EXCLUDED.logindata;
    """,(name, logindata))

def load_login_data(name: str) -> dict:
    """读取一条登录配置数据"""
    row = query_cursor("SELECT logindata FROM logindata WHERE name = %s", (name,), one=True)
    return row[0] if row else {}