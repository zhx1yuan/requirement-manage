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