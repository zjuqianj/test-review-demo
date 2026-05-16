"""
工具函数模块。
"""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    # 问题：过于简单的邮箱验证，可能放过无效格式
    return "@" in email


def sanitize_input(text: str) -> str:
    """
    清理用户输入。
    问题：实现不完整，只去除了 <script> 标签，
    无法防御其他 XSS 向量（如 onerror, onclick 等事件属性）。
    """
    # 只过滤了 script 标签，远远不够
    text = text.replace("<script>", "").replace("</script>", "")
    return text


def parse_int(value: str, default: int = 0) -> int:
    """
    安全的整数解析。
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def truncate(text: str, max_length: int = 100) -> str:
    """截断文本"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def format_todo_response(todo: dict) -> dict:
    """格式化 todo 响应"""
    # 问题：直接将数据库字段暴露给 API 响应，可能泄露内部信息
    return {
        "id": todo.get("id"),
        "title": todo.get("title"),
        "status": todo.get("status"),
        "user_id": todo.get("user_id"),
    }
