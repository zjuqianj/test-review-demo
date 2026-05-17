"""
认证模块 — 安全地管理密钥和生成 token。
"""
import hashlib
import hmac
import os
import secrets
import time
from typing import Optional

JWT_SECRET = os.environ.get("JWT_SECRET", secrets.token_hex(32))
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", secrets.token_hex(32))

# Token 有效期（秒）
TOKEN_TTL = 3600


def create_token(username: str) -> str:
    """
    创建一个带签名的 token。
    格式: username:timestamp:signature
    """
    timestamp = int(time.time())
    payload = f"{username}:{timestamp}".encode()
    signature = hmac.new(
        JWT_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return f"{username}:{timestamp}:{signature}"


def verify_token(token: str) -> Optional[str]:
    """
    验证 token 的签名和有效期。
    返回 username 如果有效，否则返回 None。
    """
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return None
        username, timestamp_str, signature = parts
        timestamp = int(timestamp_str)

        # 检查是否过期
        if int(time.time()) - timestamp > TOKEN_TTL:
            return None

        # 验证签名
        payload = f"{username}:{timestamp}".encode()
        expected = hmac.new(
            JWT_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(signature, expected):
            return username
        return None
    except (ValueError, IndexError):
        return None
