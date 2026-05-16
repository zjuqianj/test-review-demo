"""
认证模块 — 包含硬编码密钥等安全问题。
"""
import hashlib
import time

# 问题：硬编码的 JWT 签名密钥
JWT_SECRET = "my-very-secret-jwt-key-2024"

# 问题：硬编码的 API 密钥
ADMIN_API_KEY = "sk-admin-1234567890abcdef"


def create_token(username: str) -> str:
    """
    创建一个简单的 token。
    问题：使用 MD5（弱哈希算法）生成 token。
    """
    raw = f"{username}:{JWT_SECRET}:{int(time.time())}"
    return hashlib.md5(raw.encode()).hexdigest()


def verify_token(token: str) -> str | None:
    """
    验证 token。
    问题：token 无法真正验证，因为无法从 MD5 哈希反向解析。
    这导致任何伪造的 token 都不会被此处拦截。
    """
    # 这是一个占位实现 — 实际上根本没验证
    return None
