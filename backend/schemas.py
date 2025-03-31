# 定义Pydantic模式，用于数据验证和序列化。
###############     定义各类数据的类型与结构      #################

from pydantic import BaseModel
from typing import List, Optional,TYPE_CHECKING
from datetime import datetime
from .models import PermissionLevel

###############     用户名、密码、状态、登录token      #################
class UserBase(BaseModel):
    """用户基础信息模型，包含用户名。"""
    username: str

class UserCreate(UserBase):
    """创建用户模型，继承自 UserBase 并包含密码。"""
    password: str

class User(UserBase):
    """用户模型，继承自 UserBase 并包含用户 ID、是否活跃和是否为管理员。"""
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    """令牌模型，包含访问令牌和令牌类型。"""
    access_token: str
    token_type: str

###############     文档类      #################

class DocumentPermissionBase(BaseModel):
    permission_level: PermissionLevel

class DocumentPermissionCreate(DocumentPermissionBase):
    user_id: int

class DocumentPermission(DocumentPermissionBase):
    id: int
    document_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    """文档基础信息模型，包含文档标题和内容。"""
    title: str
    content: str
    tags: Optional[str] = None  # 添加tags字段

class DocumentCreate(DocumentBase):
    """创建文档模型，继承自 DocumentBase。"""
    pass

class DocumentVersionBase(BaseModel):
    """文档版本基础模型"""
    content: str
    comment: Optional[str] = None

class DocumentVersionCreate(DocumentVersionBase):
    """创建文档版本模型"""
    pass

class DocumentVersion(DocumentVersionBase):
    """文档版本模型"""
    id: int
    document_id: int
    version: int
    created_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True

class DocumentLockBase(BaseModel):
    expires_at: datetime

class DocumentLockCreate(DocumentLockBase):
    pass

class DocumentLock(DocumentLockBase):
    id: int
    document_id: int
    user_id: int
    locked_at: datetime
    is_active: bool

    class Config:
        orm_mode = True

class DocumentCommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None

class DocumentCommentCreate(DocumentCommentBase):
    pass

class DocumentComment(DocumentCommentBase):
    id: int
    document_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_resolved: bool
    replies: List['DocumentComment'] = []

    class Config:
        orm_mode = True

class Document(DocumentBase):
    """文档模型，继承自 DocumentBase 并包含文档 ID 和列表 ID。"""
    id: int
    list_id: int
    created_at: datetime
    updated_at: datetime
    version: int
    is_deleted: bool
    creator_id: int
    tags: Optional[str] = None
    permissions: List[DocumentPermission] = []
    locks: List[DocumentLock] = []
    comments: List[DocumentComment] = []

    class Config:
        orm_mode = True

###############     列表类      #################

class ListBase(BaseModel):
    """列表基础信息模型，包含列表名称和是否有序。"""
    name: str
    is_ordered: bool

class ListCreate(ListBase):
    """创建列表模型，继承自 ListBase 并包含父级列表 ID。"""
    parent_id: Optional[int] = None  # 父级列表的 ID
    order_index: Optional[int] = None  # 同级列表的排序索引

class ListSchema(ListBase):
    """列表模型，继承自 ListBase 并包含列表 ID、项目 ID、父级列表 ID、子列表和文档。"""
    id: int
    project_id: int
    parent_id: Optional[int] = None
    level_id: int
    order_index: int
    children: List["ListSchema"] = []  # 嵌套子列表
    documents: List[Document] = []
    full_path: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ListTree(ListSchema):
    """用于返回完整列表树的模型"""
    pass

###############     项目类      #################

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    owner_id: int
    lists: List[ListSchema] = []

    class Config:
        from_attributes = True


###############     预留类      #################
class ItemBase(BaseModel):
    title: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

