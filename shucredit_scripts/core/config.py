"""应用配置：优先从环境变量读取，避免在代码中硬编码敏感信息。"""
import os
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '24567@Zzy')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'student_system')

    @classmethod
    def sqlalchemy_uri(cls):
        password = quote_plus(cls.MYSQL_PASSWORD)
        return (
            f"mysql+pymysql://{cls.MYSQL_USER}:{password}"
            f"@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DB}"
        )
