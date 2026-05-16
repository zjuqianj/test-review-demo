"""
数据模型定义。
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Todo:
    id: Optional[int] = None
    title: str = ""
    status: str = "pending"
    user_id: Optional[int] = None


@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    email: Optional[str] = None
