# 配置数据库链接

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 数据库URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 创建数据引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建基础类，用于继承数据库模型
Base = declarative_base()

# 确保数据库表已创建
def init_db():
    # 导入所有模型以确保它们被注册
    from . import models
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)

# 初始化数据库
init_db()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()