"""
数据库访问层 — 使用参数化查询防止 SQL 注入。
"""
import sqlite3
import os
from typing import Optional, Any

DB_PATH = os.environ.get("DB_PATH", "todo.db")


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query_db(sql: str, params: tuple = ()):
    """
    使用参数化查询安全地执行查询。
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    conn.close()
    return result


def execute_db(sql: str, params: tuple = ()):
    """
    使用参数化查询安全地执行写操作。
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
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
            user_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        INSERT OR IGNORE INTO users (id, username, password_hash, email)
        VALUES (1, 'admin',
                '5e884898da28047151d0e56f8dc6292773603d0d',
                'admin@example.com');
    """)
    conn.commit()
    conn.close()
