# 文档管理系统

## 项目简介
这是一个基于Python FastAPI + Vue.js的文档管理系统，支持多人协作、多级列表管理、文档版本控制等功能。系统设计用于局域网环境下的团队协作。

## 技术栈
### 后端
- Python 3.8+
- FastAPI (Web框架)
- SQLAlchemy (ORM)
- SQLite (数据库)
- JWT (用户认证)
- Alembic (数据库迁移)

### 前端
- Vue.js 3
- Element Plus (UI组件库)
- Axios (HTTP客户端)

## 系统架构
```
├── backend/                # 后端代码
│   ├── __init__.py        # Python包标识
│   ├── main.py            # FastAPI主程序
│   ├── models.py          # 数据模型
│   ├── schemas.py         # Pydantic模型
│   ├── crud.py           # 数据库操作
│   ├── auth.py           # 认证相关
│   ├── database.py       # 数据库配置
│   └── alembic/          # 数据库迁移
├── frontend/              # 前端代码
│   ├── src/              # 源代码
│   ├── public/           # 静态资源
│   └── package.json      # 依赖配置
├── requirements.txt      # Python依赖
├── alembic.ini          # Alembic配置
└── README.md            # 项目文档
```

## 核心功能
1. 用户管理
   - 用户注册/登录
   - 基于角色的权限控制
   - 用户组管理

2. 项目管理
   - 创建/编辑/删除项目
   - 项目成员管理
   - 项目权限设置

3. 列表管理
   - 支持多级列表结构
   - 有序/无序列表
   - 列表拖拽排序

4. 文档管理
   - 支持Word文档导入
   - 富文本编辑
   - 文档版本控制
   - 文档导出

5. 协作功能
   - 实时同步
   - 多人同时编辑
   - 修改历史记录

## 部署说明
1. 后端部署
   ```bash
   # 安装依赖
   pip install -r requirements.txt

   # 数据库迁移
   cd backend
   alembic upgrade head

   # 启动服务（在项目根目录下运行）
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. 前端部署
   ```bash
   # 安装依赖
   cd frontend
   npm install

   # 开发环境
   npm run dev

   # 生产环境
   npm run build
   ```

## 数据库迁移
```bash
# 创建新的迁移（在backend目录下运行）
cd backend
alembic revision --autogenerate -m "描述变更内容"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 开发环境要求
1. Python 3.8+
2. Node.js 16+
3. npm 8+

## 开发计划
1. 第一阶段：基础架构搭建 ✅
   - [x] 数据库设计
   - [x] 后端API框架
   - [x] 数据库迁移配置
   - [ ] 前端项目初始化

2. 第二阶段：核心功能开发 🔄
   - [x] 用户认证系统
   - [x] 项目管理
   - [x] 列表管理
   - [x] 文档编辑
   - [x] 文档版本控制
   - [x] 文档导出
   - [ ] 前端界面开发

3. 第三阶段：协作功能
   - [x] 文档锁定机制
   - [ ] 实时同步
   - [ ] 在线协作

4. 第四阶段：优化和测试
   - [ ] 性能优化
   - [ ] 单元测试
   - [ ] 集成测试
   - [ ] 部署文档

## 下一步工作
1. 前端开发
   - 创建Vue.js项目
   - 实现用户认证界面
   - 开发项目管理界面
   - 实现文档编辑功能

2. 实时协作功能
   - 集成WebSocket
   - 实现实时同步
   - 添加在线状态显示

3. 测试与优化
   - 编写单元测试
   - 进行性能测试
   - 优化数据库查询
   - 完善错误处理

## API文档

### 用户管理API
#### 用户注册
- 路径: `/api/users/register`
- 方法: POST
- 参数:
  ```json
  {
    "username": "string",  // 用户名，必填
    "password": "string"   // 密码，必填
  }
  ```
- 返回: 用户信息（不含密码）

#### 用户登录
- 路径: `/api/users/login`
- 方法: POST
- 参数:
  ```json
  {
    "username": "string",  // 用户名，必填
    "password": "string"   // 密码，必填
  }
  ```
- 返回: JWT令牌和用户信息

### 项目管理API
#### 创建项目
- 路径: `/api/projects/`
- 方法: POST
- 参数:
  ```json
  {
    "name": "string",      // 项目名称，必填
    "description": "string" // 项目描述，可选
  }
  ```
- 返回: 项目信息

#### 获取项目列表
- 路径: `/api/projects/`
- 方法: GET
- 返回: 用户的所有项目列表

### 列表管理API
#### 创建列表
- 路径: `/api/lists/`
- 方法: POST
- 参数:
  ```json
  {
    "name": "string",      // 列表名称，必填
    "project_id": "int",   // 所属项目ID，必填
    "parent_id": "int",    // 父列表ID，可选
    "is_ordered": "bool"   // 是否有序列表，默认false
  }
  ```
- 返回: 列表信息

#### 获取列表树
- 路径: `/api/lists/tree/{project_id}`
- 方法: GET
- 参数: project_id (路径参数)
- 返回: 项目的完整列表树结构

### 文档管理API
#### 创建文档
- 路径: `/api/documents/`
- 方法: POST
- 参数:
  ```json
  {
    "title": "string",     // 文档标题，必填
    "content": "string",   // 文档内容，必填
    "list_id": "int"       // 所属列表ID，必填
  }
  ```
- 返回: 文档信息

#### 更新文档
- 路径: `/api/documents/{document_id}`
- 方法: PUT
- 参数:
  ```json
  {
    "title": "string",     // 文档标题，可选
    "content": "string",   // 文档内容，可选
    "comment": "string"    // 版本说明，可选
  }
  ```
- 返回: 更新后的文档信息

#### 获取文档
- 路径: `/api/documents/{document_id}`
- 方法: GET
- 参数: document_id (路径参数)
- 返回: 文档信息

#### 删除文档
- 路径: `/api/documents/{document_id}`
- 方法: DELETE
- 参数: document_id (路径参数)
- 返回: 操作结果

### 文档版本控制API
#### 获取文档版本历史
- 路径: `/api/documents/{document_id}/versions`
- 方法: GET
- 参数: document_id (路径参数)
- 返回: 文档版本列表

#### 恢复文档版本
- 路径: `/api/documents/{document_id}/versions/{version}`
- 方法: POST
- 参数: 
  - document_id (路径参数)
  - version (路径参数)
- 返回: 恢复后的文档信息

### 文档权限API
#### 设置文档权限
- 路径: `/api/documents/{document_id}/permissions`
- 方法: POST
- 参数:
  ```json
  {
    "user_id": "int",           // 用户ID，必填
    "permission_level": "enum"  // 权限级别：READ/WRITE/ADMIN，必填
  }
  ```
- 返回: 权限设置结果

#### 获取文档权限列表
- 路径: `/api/documents/{document_id}/permissions`
- 方法: GET
- 参数: document_id (路径参数)
- 返回: 文档权限列表

### 文档锁定API
#### 获取文档锁
- 路径: `/api/documents/{document_id}/lock`
- 方法: POST
- 参数: document_id (路径参数)
- 返回: 锁定信息

#### 释放文档锁
- 路径: `/api/documents/{document_id}/lock`
- 方法: DELETE
- 参数: document_id (路径参数)
- 返回: 操作结果

## 权限说明
系统定义了三种权限级别：
1. READ (读取权限)
   - 可以查看文档内容
   - 可以查看文档版本历史
   - 不能修改文档

2. WRITE (写入权限)
   - 包含READ权限
   - 可以编辑文档
   - 可以创建新版本
   - 可以恢复历史版本

3. ADMIN (管理权限)
   - 包含WRITE权限
   - 可以设置文档权限
   - 可以删除文档
   - 可以管理文档锁定

## 错误码说明
- 400: 请求参数错误
- 401: 未认证或认证失败
- 403: 权限不足
- 404: 资源不存在
- 409: 资源冲突（如文档被锁定）
- 422: 数据验证失败
- 500: 服务器内部错误

## 注意事项
1. 文档锁定机制
   - 锁定默认有效期为30分钟
   - 同一用户重复获取锁会刷新有效期
   - 锁定过期后自动释放

2. 版本控制
   - 每次更新文档都会创建新版本
   - 版本号从1开始递增
   - 可以随时恢复到任意历史版本

3. 权限继承
   - 项目创建者自动获得所有文档的管理权限
   - 文档创建者自动获得该文档的管理权限

4. 数据安全
   - 所有密码都经过加密存储
   - 敏感操作需要重新验证身份
   - 定期备份数据库 