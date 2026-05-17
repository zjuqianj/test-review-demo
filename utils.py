"""
工具函数模块。
"""
import html
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """验证邮箱格式，使用标准正则表达式。"""
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_input(text: str) -> str:
    """
    使用标准库 html.escape 进行 HTML 实体转义，
    防止所有 XSS 注入向量。
    """
    return html.escape(text, quote=True)


def parse_int(value: str, default: int = 0) -> int:
    """安全的整数解析。"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def truncate(text: str, max_length: int = 100) -> str:
    """截断文本并添加省略号。"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def format_todo_response(todo: dict) -> dict:
    """格式化 todo 响应，仅返回必要的公开字段。"""
    return {
        "id": todo.get("id"),
        "title": todo.get("title"),
        "status": todo.get("status"),
    }
