# 定义数据库表的类型

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import enum

###############     用户类      #################

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    projects = relationship("Project", back_populates="owner")
    created_documents = relationship("Document", back_populates="creator")
    document_permissions = relationship("DocumentPermission", back_populates="user", cascade="all, delete-orphan")
    document_locks = relationship("DocumentLock", back_populates="user", cascade="all, delete-orphan")

    class Config:
        orm_mode = True

###############     项目类      #################

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")
    lists = relationship("mylist", back_populates="project")

###############     列表类      #################

class mylist(Base):
    __tablename__ = "mylists"
    # 字段定义
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_ordered = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    parent_id = Column(Integer, ForeignKey("mylists.id"), nullable=True)      # 父级列表的 ID
    level_id = Column(Integer, default=0)
    order_index = Column(Integer, default=0)  # 同级列表的排序索引

    # 关系定义
    parent = relationship("mylist", back_populates="children", remote_side=[id])     # 子列表
    children = relationship("mylist", back_populates="parent", cascade="all, delete-orphan")
    project = relationship("Project", back_populates="lists")
    documents = relationship("Document", back_populates="list", cascade="all, delete-orphan")

    def _calculate_level_id(self):
        if self.parent_id is None:
            self.level_id = 0
        else:
            parent = self.parent
            if parent:
                self.level_id = parent.level_id + 1
            else:
                self.level_id = 0

    def update_level_id_recursive(self):
        self._calculate_level_id()
        for child in self.children:
            child.update_level_id_recursive()

    @property
    def full_path(self) -> str:
        """获取列表的完整路径"""
        path = [self.name]
        current = self
        while current.parent:
            current = current.parent
            path.append(current.name)
        return " > ".join(reversed(path))

    def get_siblings(self):
        """获取同级列表"""
        if self.parent_id is None:
            return self.project.lists
        return self.parent.children

    def reorder_siblings(self, new_order_index: int):
        """重新排序同级列表"""
        # 获取同级列表
        if self.parent:
            siblings = self.parent.children
        else:
            # 如果是顶级列表，获取同一项目下的所有顶级列表
            siblings = [l for l in self.project.lists if l.parent_id is None]
        
        # 移除当前列表
        siblings.remove(self)
        
        # 插入到新位置
        siblings.insert(new_order_index, self)
        
        # 更新所有同级列表的order_index
        for i, sibling in enumerate(siblings):
            sibling.order_index = i

###############     文档类      #################

class PermissionLevel(enum.Enum):
    READ = "read"  # 只读权限
    WRITE = "write"  # 读写权限
    ADMIN = "admin"  # 管理权限

class DocumentPermission(Base):
    __tablename__ = "document_permissions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    permission_level = Column(Enum(PermissionLevel), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    document = relationship("Document", back_populates="permissions")
    user = relationship("User", back_populates="document_permissions")

    class Config:
        orm_mode = True

class DocumentLock(Base):
    """文档编辑锁定"""
    __tablename__ = "document_locks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    locked_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    document = relationship("Document", back_populates="locks")
    user = relationship("User", back_populates="document_locks")

    class Config:
        orm_mode = True

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)
    is_deleted = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey("mylists.id"))
    creator_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(String, nullable=True)

    list = relationship("mylist", back_populates="documents")
    creator = relationship("User", back_populates="created_documents")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")
    permissions = relationship("DocumentPermission", back_populates="document", cascade="all, delete-orphan")
    locks = relationship("DocumentLock", back_populates="document", cascade="all, delete-orphan")

    class Config:
        orm_mode = True

class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    content = Column(Text)  # 文档内容
    version = Column(Integer)  # 版本号
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(String, nullable=True)  # 版本说明

    # 关系定义
    document = relationship("Document", back_populates="versions")
    created_by = relationship("User")

###############     预留      #################
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)








