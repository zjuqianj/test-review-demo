"""
Todo API 应用主入口
一个简单的任务管理 API，包含一些常见的代码问题供审查测试。
"""
from flask import Flask, request, jsonify, render_template_string
from db import query_db, execute_db
from auth import verify_token, create_token
from models import Todo

app = Flask(__name__)

# 问题1: 硬编码的 secret key
app.secret_key = "my-super-secret-key-12345"

# 问题2: 全局变量存储会话
sessions = {}


@app.route("/")
def index():
    return render_template_string("<h1>Welcome to Todo API</h1>")


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # 问题3: SQL 注入漏洞 — 直接拼接用户输入
    sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = query_db(sql)

    if user:
        token = create_token(username)
        sessions[token] = username
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/todos", methods=["GET"])
def get_todos():
    token = request.headers.get("Authorization")
    if not token or token not in sessions:
        return jsonify({"error": "Unauthorized"}), 401

    # 问题4: 另一个 SQL 注入 — 拼接用户输入到 WHERE 子句
    filter_status = request.args.get("status", "")
    sql = "SELECT * FROM todos"
    if filter_status:
        sql += f" WHERE status = '{filter_status}'"

    rows = query_db(sql)
    todos = [dict(row) for row in rows]
    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def create_todo():
    token = request.headers.get("Authorization")
    if not token or token not in sessions:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    title = data.get("title")

    # 问题5: 缺少输入校验 — title 可以为空，可能为 None
    sql = f"INSERT INTO todos (title, status, user_id) VALUES ('{title}', 'pending', 1)"
    execute_db(sql)

    return jsonify({"message": "Todo created"}), 201


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    token = request.headers.get("Authorization")
    if not token or token not in sessions:
        return jsonify({"error": "Unauthorized"}), 401

    # 问题6: 无权限检查 — 任何登录用户都可以删除任意 todo
    sql = f"DELETE FROM todos WHERE id = {todo_id}"
    execute_db(sql)

    return jsonify({"message": "Todo deleted"})


@app.route("/api/admin/users", methods=["GET"])
def list_users():
    token = request.headers.get("Authorization")
    if not token or token not in sessions:
        return jsonify({"error": "Unauthorized"}), 401

    # 问题7: 敏感数据暴露 — 返回所有用户信息包括密码哈希
    sql = "SELECT id, username, password_hash, email FROM users"
    rows = query_db(sql)
    users = [dict(row) for row in rows]
    return jsonify(users)


@app.route("/api/search", methods=["GET"])
def search_todos():
    token = request.headers.get("Authorization")
    if not token or token not in sessions:
        return jsonify({"error": "Unauthorized"}), 401

    keyword = request.args.get("q", "")

    # 问题8: 又一个 SQL 注入，且在前端输出未转义内容
    sql = f"SELECT * FROM todos WHERE title LIKE '%{keyword}%'"
    rows = query_db(sql)
    todos = [dict(row) for row in rows]

    # 问题9: XSS 漏洞 — 直接将用户输入反射到 HTML
    html = f"<h2>Search results for: {keyword}</h2><ul>"
    for todo in todos:
        html += f"<li>{todo['title']}</li>"
    html += "</ul>"

    return render_template_string(html)


if __name__ == "__main__":
    # 问题10: debug 模式在生产环境开启
    app.run(debug=True, host="0.0.0.0", port=5000)
