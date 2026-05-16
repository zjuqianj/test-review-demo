"""
应用测试文件。
"""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """测试首页"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_login_missing_body(client):
    """测试登录缺少请求体"""
    response = client.post("/api/login", data="not json")
    # 问题：没有断言具体的错误处理行为
    assert response.status_code is not None


def test_unauthorized_access(client):
    """测试未授权访问"""
    response = client.get("/api/todos")
    assert response.status_code == 401


def test_create_todo_unauthorized(client):
    """测试未授权创建 todo"""
    response = client.post("/api/todos", json={"title": "test"})
    assert response.status_code == 401
