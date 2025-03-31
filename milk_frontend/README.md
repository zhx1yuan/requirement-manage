# milk_frontend

这是一个基于 Vue 3 + TypeScript + Vite + Element Plus 的前端项目。

## 项目结构

```
milk_frontend/
├── src/                    # 源代码目录
│   ├── api/               # API 接口定义
│   │   ├── auth.ts        # 认证相关接口
│   │   ├── document.ts    # 文档相关接口
│   │   └── project.ts     # 项目相关接口
│   ├── assets/            # 静态资源
│   │   ├── base.css       # 基础样式
│   │   └── main.css       # 主样式
│   ├── components/        # 公共组件
│   ├── layouts/           # 布局组件
│   │   └── DefaultLayout.vue  # 默认布局（包含导航栏和侧边栏）
│   ├── router/            # 路由配置
│   │   └── index.ts       # 路由定义
│   ├── stores/            # 状态管理
│   │   └── user.ts        # 用户状态管理
│   ├── types/             # TypeScript 类型定义
│   │   └── index.ts       # 全局类型定义
│   ├── utils/             # 工具函数
│   │   └── request.ts     # Axios 请求封装
│   ├── views/             # 页面组件
│   │   ├── HomeView.vue   # 首页
│   │   ├── LoginView.vue  # 登录页
│   │   ├── ProjectsView.vue  # 项目列表页
│   │   ├── ProjectDetailView.vue  # 项目详情页
│   │   └── DocumentDetailView.vue  # 文档详情页
│   ├── App.vue            # 根组件
│   └── main.ts            # 应用入口
├── public/                # 公共资源目录
├── .env                   # 环境变量配置
├── package.json           # 项目依赖配置
├── tsconfig.json          # TypeScript 配置
└── vite.config.ts         # Vite 配置
```

## 技术栈

- Vue 3：使用 Composition API 和 `<script setup>` 语法
- TypeScript：提供类型检查和更好的开发体验
- Vite：快速的开发服务器和构建工具
- Element Plus：UI 组件库
- Pinia：状态管理
- Vue Router：路由管理
- Axios：HTTP 请求

## 主要功能模块

1. 认证模块
   - 登录/注册
   - Token 管理
   - 权限控制

2. 布局模块
   - 响应式导航栏
   - 可折叠侧边栏
   - 页面过渡动画

3. 项目模块
   - 项目列表
   - 项目详情
   - 项目权限管理

4. 文档模块
   - 文档列表
   - 文档编辑
   - 版本控制
   - 权限管理

## 开发指南

### 环境要求

- Node.js >= 16
- npm >= 7

### 安装依赖

```sh
npm install
```

### 开发服务器

```sh
npm run dev
```

### 生产构建

```sh
npm run build
```

### 代码检查

```sh
npm run lint
```

## 样式指南

项目使用 Element Plus 的设计系统，主要样式文件：

- `base.css`：基础样式，包含重置样式和全局变量
- `main.css`：主样式，包含全局布局和通用样式
- 组件样式：使用 `<style scoped>` 确保样式隔离

## 状态管理

使用 Pinia 进行状态管理，主要状态：

- 用户状态（`stores/user.ts`）
  - 用户信息
  - 认证状态
  - Token 管理

## API 请求

使用 Axios 封装请求，主要功能：

- 请求/响应拦截
- 错误处理
- Token 管理
- 请求重试

## 路由配置

使用 Vue Router 进行路由管理，主要路由：

- `/login`：登录页
- `/`：首页
- `/projects`：项目列表
- `/projects/:projectId`：项目详情
- `/documents/:documentId`：文档详情

## 开发规范

1. 组件命名
   - 使用 PascalCase
   - 以功能命名
   - 页面组件以 View 结尾

2. 文件组织
   - 按功能模块组织
   - 相关文件放在同一目录
   - 使用 index.ts 导出

3. 代码风格
   - 使用 TypeScript
   - 遵循 Vue 3 组合式 API 风格
   - 使用 ESLint 和 Prettier 保持代码风格一致

## 部署说明

1. 构建生产版本
```sh
npm run build
```

2. 预览生产版本
```sh
npm run preview
```

3. 部署到服务器
   - 将 `dist` 目录下的文件部署到 Web 服务器
   - 配置服务器支持 History 模式路由
   - 配置环境变量

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Run End-to-End Tests with [Cypress](https://www.cypress.io/)

```sh
npm run test:e2e:dev
```

This runs the end-to-end tests against the Vite development server.
It is much faster than the production build.

But it's still recommended to test the production build with `test:e2e` before deploying (e.g. in CI environments):

```sh
npm run build
npm run test:e2e
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
