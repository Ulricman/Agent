# Tax Knowledge Management Backend

## 📋 概述

这是 KnowTax 智知税典系统的后端服务，提供全面的税务知识管理、政策公告生成、问答系统和版本控制功能。

## 🚀 功能特性

### 核心功能

1. **税务公告生成器**
   - 生成标准化的税务政策公告HTML
   - 支持批量公告创建
   - 自定义公告模板

2. **版本管理系统**
   - 政策版本控制
   - 变更追踪（新增、替换、废止）
   - 版本回滚功能
   - 发布流程管理

3. **智能爬虫模块**
   - 模拟在线政策检查
   - 文件变更检测
   - 自动更新触发
   - 结构化日志记录

4. **知识库管理**
   - CRUD操作支持
   - 全文搜索功能
   - 分类管理
   - 数据导入/导出

5. **问答系统**
   - 模拟LLM响应
   - 智能问答匹配
   - 置信度评估
   - 自动QA生成

6. **后台管理界面**
   - 可视化数据管理
   - 实时统计面板
   - 操作日志查看

## 🛠️ 技术架构

### 后端技术栈
- **FastAPI**: 高性能API框架
- **Uvicorn**: ASGI服务器
- **Pydantic**: 数据验证和序列化
- **BeautifulSoup4**: HTML解析
- **JSON**: 本地数据存储

### 模块结构
```
backend/
├── app.py                 # 主应用入口
├── start_backend.py       # 启动脚本
├── requirements.txt       # 依赖包
├── modules/              # 核心模块
│   ├── html_generator.py # HTML生成器
│   ├── version_manager.py # 版本管理
│   ├── crawler.py        # 爬虫模块
│   ├── knowledge_base.py # 知识库
│   ├── qa_system.py      # 问答系统
│   └── logger.py         # 结构化日志
├── templates/            # 前端模板
│   └── index.html        # 管理界面
├── data/                 # 数据存储
│   ├── announcements/    # 公告文件
│   ├── backups/         # 备份文件
│   └── versions/        # 版本数据
└── static/              # 静态资源
```

## 🚀 快速开始

### 环境要求
- Python 3.7+
- 所需依赖包（见requirements.txt）

### 安装步骤

1. **进入后端目录**
   ```bash
   cd backend
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务器**
   ```bash
   python start_backend.py
   ```

4. **访问服务**
   - 管理界面: http://localhost:8000
   - API文档: http://localhost:8000/docs
   - 后端API: http://localhost:8000/api

## 📚 API接口文档

### 知识库管理 API

#### 获取所有知识条目
```http
GET /api/knowledge
```

#### 搜索知识库
```http
GET /api/knowledge/search?q={query}
```

#### 添加知识条目
```http
POST /api/knowledge
Content-Type: application/json

{
    "title": "条目标题",
    "content": "条目内容",
    "category": "分类",
    "keywords": ["关键词1", "关键词2"],
    "effective_date": "2024-01-01"
}
```

#### 更新知识条目
```http
PUT /api/knowledge/{item_id}
Content-Type: application/json

{
    "title": "更新的标题",
    "content": "更新的内容",
    "category": "更新的分类"
}
```

#### 删除知识条目
```http
DELETE /api/knowledge/{item_id}
```

### 问答系统 API

#### 获取所有问答对
```http
GET /api/qa
```

#### 搜索问答
```http
GET /api/qa/search?q={query}
```

#### 智能问答
```http
POST /api/qa/ask
Content-Type: application/json

{
    "question": "您的问题"
}
```

#### 添加问答对
```http
POST /api/qa
Content-Type: application/json

{
    "question": "问题内容",
    "answer": "回答内容",
    "category": "分类",
    "keywords": ["关键词"]
}
```

### 爬虫管理 API

#### 获取爬虫状态
```http
GET /api/crawler/status
```

#### 执行爬虫检查
```http
POST /api/crawler/check
```

#### 解析HTML文件
```http
POST /api/crawler/parse
Content-Type: application/json

{
    "html_path": "文件路径"
}
```

### 版本管理 API

#### 获取所有版本
```http
GET /api/versions
```

#### 创建新版本
```http
POST /api/versions/release
Content-Type: application/json

{
    "version": "1.1.0",
    "changes": [
        {
            "type": "append",
            "data": {"title": "新增政策"}
        }
    ],
    "release_notes": "版本发布说明"
}
```

#### 版本回滚
```http
POST /api/versions/{version}/rollback
```

### HTML生成 API

#### 生成示例公告
```http
GET /api/generate-announcement
```

#### 创建自定义公告
```http
POST /api/create-custom-announcement
Content-Type: application/json

[
    {
        "title": "公告标题",
        "content": "公告内容",
        "category": "公告分类",
        "effective_date": "2024-01-01"
    }
]
```

## 🔧 配置说明

### 服务器配置
- **主机地址**: 0.0.0.0
- **端口**: 8000
- **调试模式**: 开启（开发环境）
- **自动重载**: 开启（开发环境）

### 数据存储
- **格式**: JSON文件
- **位置**: `data/` 目录
- **备份**: 自动创建在 `data/backups/`

### 日志配置
- **标准日志**: `data/system.log`
- **结构化日志**: `data/system_log.json`
- **最大日志条目**: 10,000条

## 🔍 模块详解

### 1. HTML生成器 (html_generator.py)
负责生成标准化的税务政策公告HTML文件：
- 单个公告生成
- 批量公告生成
- 模板化设计
- 样式内嵌

### 2. 版本管理器 (version_manager.py)
提供完整的版本控制功能：
- 版本创建和发布
- 变更类型处理（append/replace/abolish）
- 版本比较
- 回滚操作
- 备份管理

### 3. 爬虫系统 (crawler.py)
模拟在线政策检查和更新：
- 文件哈希比较
- 变更检测
- HTML内容解析
- 随机更新模拟
- 状态追踪

### 4. 知识库 (knowledge_base.py)
管理税务知识条目：
- CRUD操作
- 全文搜索
- 分类管理
- 导入/导出
- 自动更新处理

### 5. 问答系统 (qa_system.py)
智能问答功能：
- 问答匹配
- 模拟LLM响应
- 置信度计算
- 回退响应
- 类别检测

### 6. 结构化日志 (logger.py)
系统日志管理：
- 多级别日志
- JSON格式存储
- 日志轮转
- 查询功能

## 🎯 使用示例

### 添加知识条目
```python
import requests

data = {
    "title": "增值税税率调整",
    "content": "根据最新政策，增值税税率调整为...",
    "category": "增值税",
    "keywords": ["增值税", "税率", "调整"],
    "effective_date": "2024-01-01"
}

response = requests.post(
    "http://localhost:8000/api/knowledge",
    json=data
)
print(response.json())
```

### 智能问答
```python
import requests

response = requests.post(
    "http://localhost:8000/api/qa/ask",
    json={"question": "增值税税率是多少？"}
)
print(response.json())
```

### 运行爬虫检查
```python
import requests

response = requests.post("http://localhost:8000/api/crawler/check")
result = response.json()
print(f"发现更新: {result['has_updates']}")
print(f"检查文件数: {result['files_checked']}")
```

## 🛡️ 安全考虑

1. **数据验证**: 使用Pydantic进行输入验证
2. **错误处理**: 完善的异常捕获和错误响应
3. **日志记录**: 详细的操作日志用于审计
4. **访问控制**: 可配置的CORS设置

## 🔄 部署指南

### 开发环境
```bash
# 启动开发服务器
python start_backend.py
```

### 生产环境
```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000
```

### Docker部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "start_backend.py"]
```

## 📊 监控和维护

### 健康检查
```http
GET /api/health
```

### 系统统计
```http
GET /api/dashboard/stats
```

### 日志查看
- 查看结构化日志文件: `data/system_log.json`
- 使用内置日志API获取最近日志

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交代码
4. 发起Pull Request

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 完整的知识库管理功能
- 问答系统实现
- 爬虫和版本控制模块
- Web管理界面

## 📞 支持与反馈

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 在线文档

---

**祝您使用愉快！** 🎉 