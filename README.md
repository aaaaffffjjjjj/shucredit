## 📁 项目结构完整说明文档

### 一、项目概述

这是一个 **通信工程专业学分管理系统**，采用 **Next.js 前端 + Flask 后端** 架构。学生可以通过上传教务处 PDF 课表，自动识别已修课程，并以 3D 太阳系可视化形式展示学分完成进度。

**技术栈**：
| 部分 | 技术 |
|------|------|
| 前端 | Next.js 16 + TypeScript + Tailwind CSS + Three.js |
| 后端 | Flask + SQLAlchemy + MySQL |
| 数据库 | MySQL |
| 3D 可视化 | React Three Fiber / Three.js |
| 认证 | Flask-Login + Session |

---

### 二、根目录文件说明

| 文件名 | 用途 |
|--------|------|
| `app.py` | Flask 后端主入口，定义所有 API 路由（`/api/progress_data`、`/upload_pdf`、`/api/auth/login` 等） |
| `config.py` | Flask 配置类（数据库连接、密钥等），从环境变量读取 |
| `import_curriculum.py` | 培养方案导入脚本：解析 PDF 中的模块树和课程，写入数据库（只需运行一次） |
| `init_db.py` | 数据库初始化脚本（创建表、测试数据） |
| `requirements.txt` | Python 依赖列表 |
| `next.config.mjs` | Next.js 配置文件，含 `/api/*` 代理到 Flask（解决跨域） |
| `package.json` | Node.js 依赖管理 |
| `tsconfig.json` | TypeScript 配置 |
| `postcss.config.mjs` | PostCSS 配置（Tailwind CSS） |
| `components.json` | shadcn/ui 组件配置 |
| `.env` | 环境变量（数据库密码、密钥等，不提交 Git） |
| `.env.example` | 环境变量模板 |
| `.env.local.example` | Next.js 本地环境变量模板 |
| `.gitignore` | Git 忽略文件 |
| `pnpm-lock.yaml` | pnpm 锁文件（可选） |
| `package-lock.json` | npm 锁文件 |

---

### 三、核心文件夹说明

#### 📁 `app/` - Next.js 页面路由（App Router）

| 路径 | 功能 |
|------|------|
| `app/layout.tsx` | 根布局（字体、元数据、主题） |
| `app/page.tsx` | 主界面（仪表盘 + 太阳系 + 左侧边栏） |
| `app/login/page.tsx` | 登录/注册页面 |
| `app/forum/` | 论坛模块（列表、发帖、详情） |

#### 📁 `components/` - React 组件

| 文件 | 用途 |
|------|------|
| `credit-solar-system.tsx` | Three.js 太阳系核心组件（行星、轨道、相机、交互） |
| `math-background.tsx` | 数学公式背景动画（漂浮的 ∫ ∑ π 等） |
| `top-navbar.tsx` | 顶部导航栏（模块切换、重置视角） |
| `sidebar-modules.tsx` | 左侧可折叠模块列表 |
| `planet-detail-panel.tsx` | 点击行星弹出的详情面板（子模块 + 课程列表） |
| `upload-pdf.tsx` | PDF 上传组件 |
| `theme-provider.tsx` | 主题切换提供者 |
| `ui/` | shadcn/ui 基础组件（button, card 等） |

#### 📁 `lib/` - 工具函数

| 文件 | 用途 |
|------|------|
| `utils.ts` | 通用工具（cn 合并类名） |
| `api.ts` | 统一 API 请求封装（含 `credentials: 'include'`） |

#### 📁 `hooks/` - 自定义 React Hooks

| 文件 | 用途 |
|------|------|
| `use-mobile.ts` | 移动端检测 |
| `use-toast.ts` | 消息提示 |

#### 📁 `public/` - 静态资源

存放 favicon、图片等公开资源。

#### 📁 `static/` - Flask 静态文件

存放旧的 HTML/JS/CSS（已废弃，可清理）。

#### 📁 `templates/` - Flask 模板

存放旧的 Jinja2 模板（已废弃，可清理）。

#### 📁 `uploads/` - 上传文件存储

存放用户上传的 PDF 课表文件（自动创建）。

#### 📁 `styles/` - 全局样式

`globals.css` 等 Tailwind 样式。

#### 📁 `__pycache__/` - Python 缓存

自动生成，可忽略。

#### 📁 `.idea/`、`.vs/` - IDE 配置

开发工具（PyCharm/VS Code）生成，可忽略。

---

### 四、关键数据流

```
用户浏览器 (http://localhost:3000)
        │
        ▼
Next.js 前端 (端口 3000)
  - app/page.tsx 调用 fetch('/api/progress_data')
  - next.config.mjs 将 /api/* 代理到 http://127.0.0.1:5000
        │
        ▼
Flask 后端 (端口 5000)
  - app.py 中 /api/progress_data 查询数据库
  - 计算每个模块的 earned_credits
  - 返回 JSON
        │
        ▼
MySQL 数据库 (student_system)
  - module (模块树)
  - course (课程)
  - enrollment (学生选课)
  - user / student (用户)
```

---

### 五、启动方式

```bash
# 终端1 - Flask 后端
cd D:\Dev\studentsystem
python app.py

# 终端2 - Next.js 前端
cd D:\Dev\studentsystem
npm run dev
```

访问 `http://localhost:3000`

---

### 六、首次部署步骤

1. **创建 MySQL 数据库**：`CREATE DATABASE student_system`
2. **配置环境变量**：复制 `.env.example` 为 `.env`，填写数据库密码
3. **安装后端依赖**：`pip install -r requirements.txt`
4. **安装前端依赖**：`npm install`
5. **导入培养方案**：`python import_curriculum.py`（解析 PDF 并写入模块/课程）
6. **启动服务**：上述启动命令

---

### 七、常见问题

| 问题 | 解决方法 |
|------|----------|
| 前端无法请求 API | 检查 Flask 是否在 5000 端口运行，且 `.env` 配置正确 |
| 行星不显示 | 检查 `/api/progress_data` 返回数据是否包含 `planets` |
| 登录后仍 401 | 清除浏览器 Cookie，重新登录 |
| PDF 上传未识别 | 检查课表 PDF 中的课程编号格式是否匹配正则 `[A-Z]{2,5}\d{6,}` |

---

**文档版本**：v4.0  
**最后更新**：2026-05-25  
**维护者**：项目开发者
