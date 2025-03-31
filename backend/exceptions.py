from fastapi import HTTPException, status

class DocumentNotFoundError(HTTPException):
    def __init__(self, detail: str = "文档不存在"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class PermissionDeniedError(HTTPException):
    def __init__(self, detail: str = "权限不足"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class DocumentLockedError(HTTPException):
    def __init__(self, detail: str = "文档已被锁定"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "数据库操作失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class ValidationError(HTTPException):
    def __init__(self, detail: str = "数据验证失败"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        ) 