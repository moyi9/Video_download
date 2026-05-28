# VideoDL - 万能视频下载网站

## 项目简介

一个跨平台的万能视频下载工具网站，支持 1800+ 平台（YouTube、B站、抖音、TikTok等），包含 AI 视频总结功能。

## 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | Vue 3 (Composition API + `<script setup>`) + Vite |
| 样式 | Tailwind CSS + @tailwindcss/typography |
| 后端 | FastAPI + uvicorn |
| 视频解析 | yt-dlp (Python库，直接import) |
| AI | DeepSeek (openai SDK) |
| Markdown | marked |
| 思维导图 | markmap-lib + markmap-view |

## 项目结构

```
Video_download/
├── CLAUDE.md              # 项目规范
├── todo.md                # 任务进度
├── docs/
│   ├── 需求分析.md
│   └── 方案设计.md
├── backend/
│   ├── main.py            # FastAPI 入口 + CORS + 路由注册
│   ├── downloader.py      # yt-dlp 封装（解析/下载/直链）
│   ├── douyin.py          # 抖音短链重定向处理
│   ├── summarizer.py      # 字幕提取 + DeepSeek AI 调用
│   ├── api_video.py       # 视频 API 路由
│   ├── api_summarize.py   # AI 总结/问答 SSE 路由
│   ├── requirements.txt
│   ├── .env.example       # DEEPSEEK_API_KEY 模板
│   └── downloads/         # 临时下载目录
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── style.css      # Tailwind + 自定义样式
│   │   ├── components/
│   │   │   ├── AppHeader.vue
│   │   │   ├── HeroSection.vue
│   │   │   ├── VideoResult.vue    # 左右双栏容器
│   │   │   ├── VideoInfo.vue      # 左栏：视频信息+下载
│   │   │   ├── VideoSummary.vue   # 右栏：AI 面板
│   │   │   ├── SummaryTab.vue
│   │   │   ├── SubtitleTab.vue
│   │   │   ├── MindmapTab.vue
│   │   │   ├── ChatTab.vue
│   │   │   ├── FeatureSection.vue
│   │   │   ├── PricingSection.vue
│   │   │   ├── PlatformSection.vue
│   │   │   └── AppFooter.vue
│   │   ├── api/
│   │   │   ├── video.js
│   │   │   └── summarize.js
│   │   └── utils/
│   │       └── format.js
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
```

## 开发规范

### 前端规范

- 使用 Composition API + `<script setup>` 语法
- 组件命名：PascalCase（如 `VideoInfo.vue`）
- CSS 使用 Tailwind CSS，避免自定义 CSS
- 状态管理：组件内 `ref()` / `reactive()`，不使用 Vuex/Pinia
- API 调用：统一在 `src/api/` 目录下封装

### 后端规范

- 路由前缀：`/api/`
- 错误返回格式：`{"success": false, "error": "错误信息"}`
- 成功返回格式：`{"success": true, "data": {...}}`
- SSE 事件格式：`data: {"type": "事件类型", "data": "内容"}\n\n`
- 文件编码：UTF-8

### 代码风格

- 不写注释，代码自解释
- 不使用分号（JS）
- 使用单引号（JS）
- 函数命名：camelCase（JS）/ snake_case（Python）
- 组件命名：PascalCase

## 启动方式

### 后端

```bash
cd backend
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY

# 启动
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd frontend
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## API 接口

### 视频解析

```
POST /api/parse
Body: {"url": "视频链接"}
Response: {"success": true, "data": {id, title, thumbnail, duration, formats, ...}}
```

### 获取直链

```
POST /api/direct-url
Body: {"url": "视频链接", "format_id": "格式ID"}
Response: {"success": true, "data": {direct_url, ext, filesize}}
```

### 代理下载

```
POST /api/download
Body: {"url": "视频链接", "format_id": "格式ID"}
Response: 视频文件流
```

### AI 总结（SSE）

```
POST /api/summarize
Body: {"url": "视频链接", "language": "zh"}
Response: SSE 事件流（subtitle, summary, mindmap, done）
```

### AI 问答（SSE）

```
POST /api/chat
Body: {"url": "视频链接", "question": "问题", "history": [...]}
Response: SSE 事件流（answer, done）
```

## UI 设计规范

- 深色主题：黑色背景 + 霓虹光效
- 主色：`cyan-400` (#22d3ee) → `blue-500` (#3b82f6)
- 渐变：`from-cyan-400 to-blue-500`
- 卡片：玻璃拟态（`bg-white/5 backdrop-blur-xl`）
- 按钮：胶囊形（`rounded-full`）+ 渐变 + 阴影
- 动画：`animate-fade-in-up` + delay 类

## 注意事项

1. 抖音短链需要先通过 requests 跟踪重定向获取真实 URL
2. B站字幕优先使用专用 API，回退到 yt-dlp
3. SSE 传输时 token 需要 `json.dumps()` 编码，避免换行符破坏协议
4. 思维导图 PNG 导出需要将 `foreignObject` 替换为 SVG `<text>`
5. Content-Disposition 文件名需要 RFC 5987 编码支持中文
