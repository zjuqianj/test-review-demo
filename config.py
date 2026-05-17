"""
应用配置文件 — 所有敏感配置通过环境变量读取。
"""
import os


class Config:
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///todo.db")
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-change-me")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")


config = Config()
