"""
Todo API 应用主入口
一个安全的任务管理 API，使用参数化查询防止 SQL 注入。
"""
import hashlib
import os

from flask import Flask, request, jsonify, render_template_string

from auth import create_token, verify_token
from db import execute_db, init_db, query_db
from models import Todo
from utils import format_todo_response, sanitize_input

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

sessions = {}


def _require_auth():
    """提取并验证 Authorization token，返回 username 或 None。"""
    token = request.headers.get("Authorization")
    if not token:
        return None
    username = verify_token(token)
    return username


@app.route("/")
def index():
    return render_template_string("<h1>Welcome to Todo API</h1>")


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    password_hash = hashlib.sha1(password.encode()).hexdigest()
    sql = "SELECT * FROM users WHERE username = ? AND password_hash = ?"
    users = query_db(sql, (username, password_hash))

    if users:
        token = create_token(username)
        sessions[token] = username
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/todos", methods=["GET"])
def get_todos():
    username = _require_auth()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    filter_status = request.args.get("status", "")
    if filter_status:
        sql = (
            "SELECT * FROM todos "
            "WHERE user_id = (SELECT id FROM users WHERE username = ?) "
            "AND status = ?"
        )
        rows = query_db(sql, (username, filter_status))
    else:
        sql = "SELECT * FROM todos WHERE user_id = (SELECT id FROM users WHERE username = ?)"
        rows = query_db(sql, (username,))

    todos = [format_todo_response(dict(row)) for row in rows]
    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def create_todo():
    username = _require_auth()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    sql = (
        "INSERT INTO todos (title, status, user_id) "
        "VALUES (?, 'pending', (SELECT id FROM users WHERE username = ?))"
    )
    execute_db(sql, (title, username))

    return jsonify({"message": "Todo created"}), 201


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    username = _require_auth()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    sql = (
        "DELETE FROM todos "
        "WHERE id = ? AND user_id = (SELECT id FROM users WHERE username = ?)"
    )
    execute_db(sql, (todo_id, username))

    return jsonify({"message": "Todo deleted"})


@app.route("/api/admin/users", methods=["GET"])
def list_users():
    username = _require_auth()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    sql = "SELECT id, username, email FROM users"
    rows = query_db(sql)
    users = [
        {"id": row["id"], "username": row["username"], "email": row["email"]}
        for row in rows
    ]
    return jsonify(users)


@app.route("/api/search", methods=["GET"])
def search_todos():
    username = _require_auth()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    keyword = (request.args.get("q") or "").strip()
    if not keyword:
        return jsonify({"error": "Search keyword is required"}), 400

    sql = (
        "SELECT * FROM todos "
        "WHERE user_id = (SELECT id FROM users WHERE username = ?) "
        "AND title LIKE ?"
    )
    rows = query_db(sql, (username, f"%{keyword}%"))
    todos = [format_todo_response(dict(row)) for row in rows]

    escaped_keyword = sanitize_input(keyword)
    items = "".join(
        f"<li>{sanitize_input(todo['title'])}</li>"
        for todo in todos
    )
    html = f"<h2>Search results for: {escaped_keyword}</h2><ul>{items}</ul>"

    return render_template_string(html)


if __name__ == "__main__":
    init_db()
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host="127.0.0.1", port=5000)
