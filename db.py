"""
数据库访问层 — 包含故意设计的 SQL 注入漏洞。
"""
import sqlite3
from typing import Optional

DB_PATH = "todo.db"


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query_db(sql: str):
    """
    执行查询并返回结果。
    问题：直接执行拼接的 SQL，存在注入风险。
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result


def execute_db(sql: str):
    """
    执行写操作。
    问题：直接执行拼接的 SQL，存在注入风险。
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def init_db():
    """初始化数据库表结构"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT
        );
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            user_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        INSERT OR IGNORE INTO users (id, username, password_hash, email)
        VALUES (1, 'admin', '5e884898da28047151d0e56f8dc6292773603d0d', 'admin@example.com');
    """)
    conn.commit()
    conn.close()
