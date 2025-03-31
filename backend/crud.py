###############     对数据库进行操作      #################
# 定义CRUD操作
from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash
from typing import List, Optional
from datetime import datetime, timedelta
from .models import PermissionLevel


###############     用户读取/创建      #################
# 通过用户id或者用户名 读取用户
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    # 密码加密
    hashed_password = get_password_hash(user.password)
    # 根据user表格传参
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


###############     项目创建/读取      #################
# 创建/读取一个项目

def create_project(db:Session,project: schemas.ProjectCreate,user_id:int):
    db_project = models.Project(**project.dict(),owner_id = user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
def get_projects(db: Session, user_id: int):
    projects = db.query(models.Project).filter(models.Project.owner_id == user_id).all()
    return projects


###############     列表读取/创建      #################
# 创建/读取列表

def create_list(db: Session, list: schemas.ListCreate, project_id: int):
    """创建新列表"""
    db_list = models.mylist(
        name=list.name,
        is_ordered=list.is_ordered,
        project_id=project_id
    )
    
    # 处理父列表关系
    if list.parent_id:
        parent_list = db.query(models.mylist).filter(
            models.mylist.id == list.parent_id,
            models.mylist.project_id == project_id
        ).first()
        if parent_list:
            db_list.parent = parent_list
            db_list.level_id = parent_list.level_id + 1
            # 设置排序索引
            siblings = parent_list.children
            db_list.order_index = len(siblings)
        else:
            raise ValueError(f"未找到ID为{list.parent_id}的父列表")
    else:
        db_list.level_id = 0
        # 设置顶级列表的排序索引
        top_level_lists = db.query(models.mylist).filter(
            models.mylist.project_id == project_id,
            models.mylist.parent_id.is_(None)
        ).all()
        db_list.order_index = len(top_level_lists)
    
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def get_list_tree(db: Session, project_id: int):
    """获取项目的完整列表树"""
    def build_tree(lists, parent_id=None):
        tree = []
        for list_item in sorted(lists, key=lambda x: x.order_index):
            if list_item.parent_id == parent_id:
                list_item.children = build_tree(lists, list_item.id)
                tree.append(list_item)
        return tree
    
    all_lists = db.query(models.mylist).filter(
        models.mylist.project_id == project_id
    ).all()
    
    return build_tree(all_lists)

def get_a_list(db: Session, list_id: int = None, list_name: str = None, list_project_id: int = None):
    """获取列表"""
    query = db.query(models.mylist)
    if list_id:
        query = query.filter(models.mylist.id == list_id)
    if list_name:
        query = query.filter(models.mylist.name == list_name)
    if list_project_id:
        query = query.filter(models.mylist.project_id == list_project_id)
    results = query.all()
    return results

def update_list(
    db: Session,
    list_id: int,
    list_data: schemas.ListCreate,
    user_id: int
) -> Optional[models.mylist]:
    """更新列表"""
    # 获取列表
    db_list = db.query(models.mylist).filter(models.mylist.id == list_id).first()
    if not db_list:
        return None
    
    # 检查项目所有权
    if not check_project_ownership(db, db_list.project_id, user_id):
        return None
    
    # 如果父级列表发生变化，需要更新level_id
    if list_data.parent_id != db_list.parent_id:
        # 检查新父级列表是否存在且属于同一项目
        if list_data.parent_id:
            parent_list = db.query(models.mylist).filter(
                models.mylist.id == list_data.parent_id,
                models.mylist.project_id == db_list.project_id
            ).first()
            if not parent_list:
                return None
        
        # 更新父级列表ID
        db_list.parent_id = list_data.parent_id
        
        # 更新level_id
        db_list._calculate_level_id()
        
        # 递归更新所有子列表的level_id
        db_list.update_level_id_recursive()
    
    # 更新其他字段
    for key, value in list_data.dict(exclude={'parent_id'}).items():
            setattr(db_list, key, value)
    
    # 如果order_index发生变化，需要重新排序
    if list_data.order_index is not None and list_data.order_index != db_list.order_index:
        db_list.reorder_siblings(list_data.order_index)
    
        db.commit()
        db.refresh(db_list)
    return db_list

def delete_list(db: Session, list_id: int):
    """删除列表及其所有子列表"""
    db_list = db.query(models.mylist).filter(models.mylist.id == list_id).first()
    if db_list:
        # 由于设置了cascade="all, delete-orphan"，删除父列表会自动删除所有子列表
        db.delete(db_list)
        db.commit()
    return db_list


# 对应 @app.get("/lists_by_project/", response_model=List[schemas.ListSchema])
# def get_all_list(db: Session,list_project_id: int = None):
#     results = db.query(models.mylist).filter(models.mylist.project_id == list_project_id).all()
#     if results:
#         return results




###############     文档创建/读取      #################
# 创建/读写文档

def check_document_permission(db: Session, document_id: int, user_id: int, required_permission: PermissionLevel) -> bool:
    """检查用户是否有指定文档的所需权限"""
    # 获取文档
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        return False
    
    # 文档创建者拥有所有权限
    if document.creator_id == user_id:
        return True
    
    # 检查用户权限
    permission = db.query(models.DocumentPermission).filter(
        models.DocumentPermission.document_id == document_id,
        models.DocumentPermission.user_id == user_id
    ).first()
    
    if not permission:
        return False
    
    # 权限等级检查
    permission_levels = {
        PermissionLevel.READ: 1,
        PermissionLevel.WRITE: 2,
        PermissionLevel.ADMIN: 3
    }
    return permission_levels[permission.permission_level] >= permission_levels[required_permission]

def create_document_permission(
    db: Session,
    document_id: int,
    user_id: int,
    permission_level: PermissionLevel
) -> models.DocumentPermission:
    """创建文档权限"""
    db_permission = models.DocumentPermission(
        document_id=document_id,
        user_id=user_id,
        permission_level=permission_level
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def update_document_permission(
    db: Session,
    document_id: int,
    user_id: int,
    permission_level: PermissionLevel
) -> Optional[models.DocumentPermission]:
    """更新文档权限"""
    db_permission = db.query(models.DocumentPermission).filter(
        models.DocumentPermission.document_id == document_id,
        models.DocumentPermission.user_id == user_id
    ).first()
    
    if db_permission:
        db_permission.permission_level = permission_level
        db.commit()
        db.refresh(db_permission)
    return db_permission

def delete_document_permission(
    db: Session,
    document_id: int,
    user_id: int
) -> bool:
    """删除文档权限"""
    db_permission = db.query(models.DocumentPermission).filter(
        models.DocumentPermission.document_id == document_id,
        models.DocumentPermission.user_id == user_id
    ).first()
    
    if db_permission:
        db.delete(db_permission)
        db.commit()
        return True
    return False

def get_document_permissions(
    db: Session,
    document_id: int
) -> List[models.DocumentPermission]:
    """获取文档的所有权限"""
    return db.query(models.DocumentPermission).filter(
        models.DocumentPermission.document_id == document_id
    ).all()

def create_document(
    db: Session,
    document: schemas.DocumentCreate,
    list_id: int,
    user_id: int
) -> models.Document:
    """创建文档"""
    db_document = models.Document(
        **document.dict(),
        list_id=list_id,
        creator_id=user_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # 创建者自动获得管理权限
    create_document_permission(db, db_document.id, user_id, PermissionLevel.ADMIN)
    
    return db_document

def get_document(
    db: Session,
    document_id: int,
    user_id: int
) -> Optional[models.Document]:
    """获取文档（带权限检查）"""
    if not check_document_permission(db, document_id, user_id, PermissionLevel.READ):
        return None
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def update_document(
    db: Session,
    document_id: int,
    document: schemas.DocumentCreate,
    user_id: int,
    comment: str = None
) -> Optional[models.Document]:
    """更新文档（带权限检查）"""
    if not check_document_permission(db, document_id, user_id, PermissionLevel.WRITE):
        return None
    
    db_document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not db_document:
        return None
    
    # 创建新版本
    db_version = models.DocumentVersion(
        document_id=document_id,
        title=db_document.title,
        content=db_document.content,
        version=db_document.version,
        created_by_id=user_id,
        comment=comment
    )
    db.add(db_version)
    
    # 更新文档
        for key, value in document.dict().items():
            setattr(db_document, key, value)
    db_document.version += 1
    
        db.commit()
        db.refresh(db_document)
    return db_document

def delete_document(
    db: Session,
    document_id: int,
    user_id: int
) -> bool:
    """删除文档（带权限检查）"""
    if not check_document_permission(db, document_id, user_id, PermissionLevel.ADMIN):
        return False
    
    db_document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if db_document:
        db_document.is_deleted = True
        db.commit()
        return True
    return False

def get_document_versions(db: Session, document_id: int):
    """获取文档的所有版本"""
    return db.query(models.DocumentVersion).filter(
        models.DocumentVersion.document_id == document_id
    ).order_by(models.DocumentVersion.version.desc()).all()

def create_document_version(
    db: Session,
    document_id: int,
    content: str,
    user_id: int,
    comment: str = None
) -> models.DocumentVersion:
    """创建文档新版本"""
    document = get_document(db, document_id, user_id)
    if not document:
        raise ValueError(f"文档 {document_id} 不存在")
    
    db_version = models.DocumentVersion(
        document_id=document_id,
        title=document.title,
        content=content,
        version=document.version,
        created_by_id=user_id,
        comment=comment
    )
    db.add(db_version)
    document.version += 1
    db.commit()
    db.refresh(db_version)
    return db_version

def restore_document_version(db: Session, document_id: int, version: int, user_id: int):
    """恢复到指定版本"""
    document = get_document(db, document_id)
    if not document:
        raise ValueError(f"文档 {document_id} 不存在")
    
    version_record = db.query(models.DocumentVersion).filter(
        models.DocumentVersion.document_id == document_id,
        models.DocumentVersion.version == version
    ).first()
    
    if not version_record:
        raise ValueError(f"版本 {version} 不存在")
    
    # 创建新版本，内容为指定版本的内容
    create_document_version(
        db,
        document_id,
        version_record.content,
        user_id,
        f"恢复到版本 {version}"
    )
    
    return document

def acquire_document_lock(
    db: Session,
    document_id: int,
    user_id: int,
    lock_duration: int = 30
) -> Optional[models.DocumentLock]:
    """获取文档编辑锁"""
    # 检查是否有其他用户正在编辑
    current_time = datetime.utcnow()
    existing_lock = db.query(models.DocumentLock).filter(
        models.DocumentLock.document_id == document_id,
        models.DocumentLock.is_active == True,
        models.DocumentLock.expires_at > current_time
    ).first()
    
    if existing_lock:
        return None
    
    # 创建新的锁定记录
    expires_at = current_time + timedelta(minutes=lock_duration)
    db_lock = models.DocumentLock(
        document_id=document_id,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(db_lock)
    db.commit()
    db.refresh(db_lock)
    return db_lock

def release_document_lock(
    db: Session,
    document_id: int,
    user_id: int
) -> bool:
    """释放文档编辑锁"""
    current_time = datetime.utcnow()
    lock = db.query(models.DocumentLock).filter(
        models.DocumentLock.document_id == document_id,
        models.DocumentLock.user_id == user_id,
        models.DocumentLock.is_active == True,
        models.DocumentLock.expires_at > current_time
    ).first()
    
    if lock:
        lock.is_active = False
        db.commit()
        return True
    return False

def create_document_comment(
    db: Session,
    document_id: int,
    user_id: int,
    content: str,
    parent_id: Optional[int] = None
) -> models.DocumentComment:
    """创建文档评论"""
    db_comment = models.DocumentComment(
        document_id=document_id,
        user_id=user_id,
        content=content,
        parent_id=parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_document_comments(
    db: Session,
    document_id: int
) -> List[models.DocumentComment]:
    """获取文档的所有评论"""
    return db.query(models.DocumentComment).filter(
        models.DocumentComment.document_id == document_id,
        models.DocumentComment.parent_id.is_(None)  # 只获取顶级评论
    ).all()

def update_document_comment(
    db: Session,
    comment_id: int,
    user_id: int,
    content: str
) -> Optional[models.DocumentComment]:
    """更新文档评论"""
    comment = db.query(models.DocumentComment).filter(
        models.DocumentComment.id == comment_id,
        models.DocumentComment.user_id == user_id
    ).first()
    
    if comment:
        comment.content = content
        db.commit()
        db.refresh(comment)
    return comment

def delete_document_comment(
    db: Session,
    comment_id: int,
    user_id: int
) -> bool:
    """删除文档评论"""
    comment = db.query(models.DocumentComment).filter(
        models.DocumentComment.id == comment_id,
        models.DocumentComment.user_id == user_id
    ).first()
    
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False

def resolve_document_comment(
    db: Session,
    comment_id: int,
    user_id: int
) -> Optional[models.DocumentComment]:
    """标记评论为已解决"""
    comment = db.query(models.DocumentComment).filter(
        models.DocumentComment.id == comment_id,
        models.DocumentComment.user_id == user_id
    ).first()
    
    if comment:
        comment.is_resolved = True
        db.commit()
        db.refresh(comment)
    return comment


###############     预留      #################

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def check_project_ownership(db: Session, project_id: int, user_id: int) -> bool:
    """检查用户是否是项目的所有者"""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == user_id
    ).first()
    return project is not None

