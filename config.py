"""
应用配置文件。
问题：硬编码了敏感配置，应该通过环境变量读取。
"""
import os


class Config:
    # 问题：硬编码数据库连接字符串
    DATABASE_URL = "postgresql://admin:password123@localhost:5432/todo_db"

    # 问题：硬编码第三方服务密钥
    SENDGRID_API_KEY = "SG.xxxxxxxxxxxxx-xxxxxxxxxxxxx-xxxxxxxxxxxxx"

    # 问题：硬编码的 AWS 凭证
    AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

    # 问题：debug 模式默认开启
    DEBUG = True

    # 这些是正确的用法示例
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-change-me")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")


config = Config()
