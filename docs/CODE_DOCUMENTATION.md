# KnowTax 智知税典 - 代码技术文档

## 📋 目录

- [系统架构概述](#系统架构概述)
- [前端系统 (Flask)](#前端系统-flask)
- [后端系统 (FastAPI)](#后端系统-fastapi)
- [数据模型](#数据模型)
- [API接口](#api接口)
- [核心算法](#核心算法)
- [部署配置](#部署配置)
- [开发规范](#开发规范)

## 系统架构概述

### 🏗️ 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    KnowTax 智知税典                          │
├─────────────────────────────────────────────────────────────┤
│  前端系统 (Flask)          │  后端系统 (FastAPI)             │
│  端口: 12345              │  端口: 8000                     │
│  ┌─────────────────────┐  │  ┌─────────────────────────┐    │
│  │ 用户界面            │  │  │ REST API 服务           │    │
│  │ 权限管理            │  │  │ 业务逻辑处理            │    │
│  │ 数据可视化          │  │  │ 数据管理                │    │
│  └─────────────────────┘  │  └─────────────────────────┘    │
│           │               │            │                    │
│  ┌─────────────────────┐  │  ┌─────────────────────────┐    │
│  │ SQLite 用户数据库   │  │  │ JSON 数据文件           │    │
│  │ Session 管理        │  │  │ 知识库/问答库           │    │
│  └─────────────────────┘  │  └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 数据流架构

```
用户请求 → Flask路由 → 业务逻辑 → SQLite/API调用 → FastAPI → JSON数据 → 响应返回
```

### 🛠️ 技术栈

#### 前端技术栈
- **Flask 2.0+**: Web应用框架
- **SQLAlchemy**: ORM数据库操作
- **Werkzeug**: 安全与认证
- **Jinja2**: 模板引擎
- **ECharts**: 数据可视化

#### 后端技术栈
- **FastAPI**: 高性能API框架
- **Pydantic**: 数据验证
- **Uvicorn**: ASGI服务器
- **BeautifulSoup4**: HTML解析
- **Python 3.7+**: 运行环境

---

## 前端系统 (Flask)

### 📁 目录结构
```
├── app.py                 # 主应用入口
├── create_user.py         # 用户初始化脚本
├── models/
│   └── user.py           # 用户数据模型
├── routes/
│   ├── auth.py           # 认证路由
│   ├── admin.py          # 管理员路由
│   ├── manager.py        # 经理路由
│   ├── service.py        # 客服路由
│   ├── data.py           # 数据路由
│   └── backend.py        # 后端集成路由
├── templates/            # HTML模板
├── static/              # 静态资源
└── instance/           # 实例配置
```

### 🔧 核心文件详解

#### `app.py` - 主应用入口
```python
# 主要功能:
# 1. Flask应用初始化
# 2. 数据库配置
# 3. 路由注册
# 4. 会话管理

from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tax_system.db'

# 关键组件初始化
db = SQLAlchemy(app)

# 路由蓝图注册
from routes.auth import auth_bp
from routes.admin import admin_bp
# ... 其他蓝图注册
```

**核心功能**:
- ✅ Flask应用配置和初始化
- ✅ SQLAlchemy数据库配置
- ✅ 会话管理配置
- ✅ 蓝图路由注册
- ✅ 错误处理

#### `models/user.py` - 用户数据模型
```python
# 功能: 定义用户数据结构和数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
```

**核心功能**:
- ✅ 用户基本信息存储
- ✅ 密码哈希处理
- ✅ 用户角色管理
- ✅ 用户状态控制

### 🛣️ 路由系统

#### `routes/auth.py` - 认证路由
```python
# 核心功能:
# 1. 用户登录验证
# 2. 会话管理
# 3. 权限检查
# 4. 安全控制

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 用户登录逻辑
    # 密码验证
    # 会话创建
    pass

@auth_bp.route('/logout')
def logout():
    # 会话清理
    # 安全登出
    pass
```

**关键功能**:
- ✅ 用户身份验证
- ✅ 密码安全验证  
- ✅ 会话状态管理
- ✅ 权限检查装饰器

#### `routes/admin.py` - 管理员路由
```python
# 管理员专用功能路由
@admin_bp.route('/user_monitor')
@login_required
@admin_required
def user_monitor():
    # 用户状态监控
    # 系统管理功能
    pass
```

**核心功能**:
- ✅ 用户权限管理
- ✅ 系统配置管理
- ✅ 数据库维护
- ✅ 系统监控

#### `routes/manager.py` - 经理路由
```python
# 经理专用功能路由
@manager_bp.route('/pending_tasks')
@login_required
@manager_required 
def pending_tasks():
    # 待审批任务管理
    # 内容审核
    pass
```

**核心功能**:
- ✅ 内容审核管理
- ✅ 数据质量控制
- ✅ 业务流程监控
- ✅ 统计分析

#### `routes/service.py` - 客服路由
```python
# 客服专用功能路由
@service_bp.route('/search')
@login_required
@service_required
def search():
    # 搜索服务功能
    # 用户查询支持
    pass
```

**核心功能**:
- ✅ 搜索服务提供
- ✅ 用户查询支持
- ✅ 问题答疑
- ✅ 服务记录

#### `routes/backend.py` - 后端集成路由
```python
# 前后端集成路由
@backend_bp.route('/dashboard')
@login_required
def dashboard():
    # 后端管理界面集成
    # API调用转发
    pass
```

**核心功能**:
- ✅ 前后端通信
- ✅ API调用转发
- ✅ 数据同步
- ✅ 错误处理

### 🎨 模板系统

#### `templates/base.html` - 基础模板
```html
<!-- 基础页面结构 -->
<!DOCTYPE html>
<html>
<head>
    <title>KnowTax 智知税典</title>
    <!-- 样式和脚本引用 -->
</head>
<body>
    <!-- 导航栏 -->
    <!-- 内容区域 -->
    <!-- 脚本区域 -->
</body>
</html>
```

**关键特性**:
- ✅ 响应式设计
- ✅ 统一样式风格
- ✅ 脚本管理
- ✅ SEO优化

#### 页面模板功能
- `home.html`: 主页面和仪表板
- `login.html`: 用户登录界面
- 角色专用页面: 各角色功能界面

---

## 后端系统 (FastAPI)

### 📁 目录结构
```
backend/
├── app.py                    # FastAPI主应用
├── start_backend.py          # 启动脚本
├── requirements.txt          # 依赖包
├── modules/                  # 核心模块
│   ├── html_generator.py     # HTML生成器
│   ├── version_manager.py    # 版本管理
│   ├── crawler.py           # 爬虫模块
│   ├── knowledge_base.py    # 知识库管理
│   ├── qa_system.py         # 问答系统
│   └── logger.py            # 日志系统
├── templates/               # 模板文件
│   └── index.html          # 管理界面
├── data/                   # 数据目录
└── README.md              # 说明文档
```

### 🔧 核心模块详解

#### `app.py` - FastAPI主应用
```python
# 主要功能:
# 1. FastAPI应用初始化
# 2. API路由定义
# 3. 中间件配置
# 4. 异常处理

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="KnowTax Backend API",
    description="智知税典后端API服务",
    version="1.0.0"
)

# 核心API端点
@app.get("/")
async def dashboard():
    # 管理仪表板
    pass

@app.post("/knowledge/add")
async def add_knowledge():
    # 知识库添加
    pass
```

**核心功能**:
- ✅ RESTful API设计
- ✅ 自动API文档生成
- ✅ 请求验证
- ✅ 异常处理
- ✅ 跨域支持

#### `modules/html_generator.py` - HTML生成器
```python
class HTMLGenerator:
    """税务公告HTML生成器"""
    
    def __init__(self):
        self.templates = {
            "announcement": "标准公告模板",
            "policy": "政策文件模板",
            "notice": "通知模板"
        }
    
    def generate_announcement(self, data):
        """生成税务公告HTML"""
        # 1. 验证输入数据
        # 2. 选择模板
        # 3. 填充数据
        # 4. 生成HTML
        # 5. 返回结果
        pass
```

**核心功能**:
- ✅ 模板化HTML生成
- ✅ 数据验证处理
- ✅ 样式美化
- ✅ 批量处理能力

#### `modules/version_manager.py` - 版本管理系统
```python
class VersionManager:
    """版本控制管理器"""
    
    def __init__(self):
        self.versions = {}
        self.current_version = "1.0.0"
    
    def create_version(self, version_info):
        """创建新版本"""
        # 1. 验证版本信息
        # 2. 创建版本记录
        # 3. 更新版本历史
        # 4. 备份当前数据
        pass
    
    def rollback_version(self, target_version):
        """版本回滚"""
        # 1. 验证目标版本
        # 2. 备份当前状态
        # 3. 恢复目标版本
        # 4. 更新版本状态
        pass
```

**核心功能**:
- ✅ 版本创建和管理
- ✅ 变更追踪
- ✅ 版本回滚
- ✅ 发布控制

#### `modules/crawler.py` - 智能爬虫模块
```python
class PolicyCrawler:
    """政策文件爬虫"""
    
    def __init__(self):
        self.check_interval = 3600  # 检查间隔(秒)
        self.last_check = None
        self.hash_store = {}
    
    def check_for_updates(self):
        """检查更新"""
        # 1. 扫描HTML文件
        # 2. 计算文件哈希
        # 3. 比较变更
        # 4. 记录更新
        pass
    
    def process_updates(self, updates):
        """处理发现的更新"""
        # 1. 分析更新内容
        # 2. 更新知识库
        # 3. 记录变更日志
        # 4. 通知相关系统
        pass
```

**核心功能**:
- ✅ 文件变更监控
- ✅ 哈希比较机制
- ✅ 自动更新处理
- ✅ 变更通知

#### `modules/knowledge_base.py` - 知识库管理
```python
class KnowledgeBase:
    """知识库管理系统"""
    
    def __init__(self):
        self.data_file = "data/knowledge.json"
        self.knowledge_data = []
    
    def add_knowledge(self, item):
        """添加知识条目"""
        # 1. 数据验证
        # 2. 去重检查
        # 3. 添加到库中
        # 4. 保存文件
        pass
    
    def search_knowledge(self, query):
        """搜索知识"""
        # 1. 分词处理
        # 2. 关键词匹配
        # 3. 相关性排序
        # 4. 返回结果
        pass
```

**核心功能**:
- ✅ CRUD操作完整支持
- ✅ 智能搜索算法
- ✅ 数据导入导出
- ✅ 分类管理

#### `modules/qa_system.py` - 问答系统
```python
class QASystem:
    """智能问答系统"""
    
    def __init__(self):
        self.qa_data = []
        self.confidence_threshold = 0.7
    
    def answer_question(self, question):
        """回答问题"""
        # 1. 问题理解
        # 2. 意图识别
        # 3. 答案匹配
        # 4. 置信度计算
        # 5. 返回最佳答案
        pass
    
    def simulate_llm_response(self, question, category):
        """模拟LLM响应"""
        # 1. 分析问题类型
        # 2. 选择回答模板
        # 3. 生成回答
        # 4. 评估置信度
        pass
```

**核心功能**:
- ✅ 问题理解和匹配
- ✅ 置信度评估
- ✅ 模拟LLM响应
- ✅ 自动回答生成

#### `modules/logger.py` - 日志系统
```python
class SystemLogger:
    """系统日志管理"""
    
    def __init__(self):
        self.log_file = "data/system.log"
        self.log_level = "INFO"
    
    def log_operation(self, operation, details):
        """记录操作日志"""
        # 1. 格式化日志信息
        # 2. 添加时间戳
        # 3. 写入日志文件
        # 4. 控制台输出
        pass
```

**核心功能**:
- ✅ 结构化日志记录
- ✅ 多级别日志支持
- ✅ JSON格式输出
- ✅ 文件和控制台双输出

---

## 数据模型

### 📊 前端数据模型

#### 用户模型 (SQLite)
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 📊 后端数据模型

#### 知识库模型 (JSON)
```json
{
    "id": "kb_001",
    "title": "增值税税率调整通知",
    "content": "具体内容...",
    "category": "增值税",
    "keywords": ["税率", "调整", "通知"],
    "effective_date": "2024-01-01",
    "status": "active",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 问答模型 (JSON)
```json
{
    "id": "qa_001", 
    "question": "如何申报增值税？",
    "answer": "详细回答内容...",
    "category": "申报流程",
    "keywords": ["申报", "增值税", "流程"],
    "confidence": 0.95,
    "created_at": "2024-01-01T00:00:00Z"
}
```

#### 版本模型 (JSON)
```json
{
    "version": "1.1.0",
    "release_date": "2024-01-01T00:00:00Z",
    "description": "版本更新说明",
    "changes": [
        {
            "type": "add|modify|delete",
            "target": "knowledge|qa|system",
            "description": "具体变更内容"
        }
    ],
    "is_current": true
}
```

---

## API接口

### 🌐 RESTful API设计

#### 知识库API
```python
# GET /knowledge - 获取知识列表
# POST /knowledge - 添加知识条目
# PUT /knowledge/{id} - 更新知识条目
# DELETE /knowledge/{id} - 删除知识条目
# GET /knowledge/search?q={query} - 搜索知识
```

#### 问答系统API
```python
# GET /qa - 获取问答列表
# POST /qa - 添加问答对
# POST /qa/ask - 提问获取回答
# PUT /qa/{id} - 更新问答对
# DELETE /qa/{id} - 删除问答对
```

#### 版本管理API
```python
# GET /version - 获取当前版本信息
# GET /version/history - 获取版本历史
# POST /version/create - 创建新版本
# POST /version/rollback/{version} - 版本回滚
```

#### 系统管理API
```python
# GET /system/status - 获取系统状态
# GET /system/logs - 获取系统日志
# POST /crawler/check - 手动触发爬虫检查
# GET /crawler/status - 获取爬虫状态
```

### 📝 API响应格式
```json
{
    "code": 200,
    "message": "success",
    "data": {},
    "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## 核心算法

### 🔍 搜索算法

#### 知识库搜索算法
```python
def search_knowledge(query, knowledge_data):
    """
    知识库搜索算法
    使用TF-IDF和关键词匹配
    """
    # 1. 查询预处理
    processed_query = preprocess_query(query)
    
    # 2. 关键词提取
    keywords = extract_keywords(processed_query)
    
    # 3. 相关性计算
    scores = []
    for item in knowledge_data:
        score = calculate_relevance(keywords, item)
        scores.append((item, score))
    
    # 4. 结果排序
    sorted_results = sorted(scores, key=lambda x: x[1], reverse=True)
    
    return sorted_results
```

#### 相关性计算
```python
def calculate_relevance(keywords, knowledge_item):
    """计算查询与知识条目的相关性"""
    score = 0.0
    
    # 标题权重: 0.4
    title_score = keyword_match_score(keywords, knowledge_item['title'])
    score += title_score * 0.4
    
    # 内容权重: 0.3
    content_score = keyword_match_score(keywords, knowledge_item['content'])
    score += content_score * 0.3
    
    # 关键词权重: 0.2
    keyword_score = keyword_match_score(keywords, knowledge_item['keywords'])
    score += keyword_score * 0.2
    
    # 分类权重: 0.1
    category_score = keyword_match_score(keywords, [knowledge_item['category']])
    score += category_score * 0.1
    
    return score
```

### 🤖 问答匹配算法

#### 问题相似度计算
```python
def calculate_question_similarity(input_question, stored_question):
    """计算问题相似度"""
    # 1. 文本预处理
    q1_processed = preprocess_text(input_question)
    q2_processed = preprocess_text(stored_question)
    
    # 2. 词汇重叠度
    word_overlap = calculate_word_overlap(q1_processed, q2_processed)
    
    # 3. 语义相似度(简化版)
    semantic_similarity = calculate_semantic_similarity(q1_processed, q2_processed)
    
    # 4. 综合评分
    final_score = word_overlap * 0.6 + semantic_similarity * 0.4
    
    return final_score
```

### 📈 版本差异算法

#### 变更检测算法
```python
def detect_changes(old_version, new_version):
    """检测版本间的变更"""
    changes = []
    
    # 1. 结构比较
    old_keys = set(old_version.keys())
    new_keys = set(new_version.keys())
    
    # 2. 添加的项目
    added = new_keys - old_keys
    for key in added:
        changes.append({
            'type': 'add',
            'key': key,
            'value': new_version[key]
        })
    
    # 3. 删除的项目
    deleted = old_keys - new_keys
    for key in deleted:
        changes.append({
            'type': 'delete',
            'key': key,
            'old_value': old_version[key]
        })
    
    # 4. 修改的项目
    common = old_keys & new_keys
    for key in common:
        if old_version[key] != new_version[key]:
            changes.append({
                'type': 'modify',
                'key': key,
                'old_value': old_version[key],
                'new_value': new_version[key]
            })
    
    return changes
```

---

## 部署配置

### 🚀 开发环境部署

#### 前端系统启动
```bash
# 1. 安装依赖
pip install flask flask-sqlalchemy

# 2. 初始化用户
python create_user.py

# 3. 启动服务
python app.py
```

#### 后端系统启动
```bash
# 1. 进入后端目录
cd backend

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python start_backend.py
```

### 🏭 生产环境部署

#### 使用Gunicorn部署前端
```bash
# 安装Gunicorn
pip install gunicorn

# 启动命令
gunicorn -w 4 -b 0.0.0.0:12345 app:app
```

#### 使用Uvicorn部署后端
```bash
# 启动命令
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Docker容器化部署
```dockerfile
# Dockerfile示例
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 12345 8000

CMD ["python", "start_all.py"]
```

### 🔧 配置文件

#### 环境配置
```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tax_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
```

---

## 开发规范

### 📝 代码规范

#### Python代码规范
```python
# 1. 遵循PEP 8规范
# 2. 使用类型提示
def add_knowledge(item: dict) -> bool:
    """添加知识条目
    
    Args:
        item: 知识条目字典
        
    Returns:
        bool: 操作是否成功
    """
    pass

# 3. 异常处理
try:
    result = process_data(data)
except ValidationError as e:
    logger.error(f"数据验证失败: {e}")
    raise HTTPException(status_code=400, detail=str(e))
```

#### 前端代码规范
```javascript
// 1. 使用ES6+语法
// 2. 错误处理
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('获取数据失败:', error);
        throw error;
    }
}
```

### 🧪 测试规范

#### 单元测试
```python
import unittest
from modules.knowledge_base import KnowledgeBase

class TestKnowledgeBase(unittest.TestCase):
    def setUp(self):
        self.kb = KnowledgeBase()
    
    def test_add_knowledge(self):
        item = {"title": "测试", "content": "内容"}
        result = self.kb.add_knowledge(item)
        self.assertTrue(result)
    
    def test_search_knowledge(self):
        results = self.kb.search_knowledge("测试")
        self.assertIsInstance(results, list)
```

### 📊 性能优化

#### 数据库优化
```python
# 1. 查询优化
def get_knowledge_by_category(category):
    return Knowledge.query.filter_by(category=category).all()

# 2. 缓存机制
from functools import lru_cache

@lru_cache(maxsize=100)
def get_frequent_questions():
    return qa_system.get_top_questions(limit=10)
```

#### API优化
```python
# 1. 分页处理
@app.get("/knowledge")
async def get_knowledge(page: int = 1, limit: int = 20):
    offset = (page - 1) * limit
    return knowledge_base.get_paginated(offset, limit)

# 2. 响应压缩
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 🔒 安全规范

#### 输入验证
```python
from pydantic import BaseModel, validator

class KnowledgeItem(BaseModel):
    title: str
    content: str
    category: str
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('标题不能为空')
        return v
```

#### 权限控制
```python
def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session:
                return redirect(url_for('auth.login'))
            if session['user_role'] != required_role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

---

## 📞 技术支持

### 🛠️ 开发工具
- **IDE**: VS Code, PyCharm
- **调试**: Flask Debug Mode, FastAPI Debug
- **测试**: Pytest, Unittest
- **文档**: Swagger UI (自动生成)

### 📚 参考资源
- **Flask文档**: https://flask.palletsprojects.com/
- **FastAPI文档**: https://fastapi.tiangolo.com/
- **SQLAlchemy文档**: https://www.sqlalchemy.org/
- **Pydantic文档**: https://pydantic-docs.helpmanual.io/

### 🐛 问题排查

#### 常见问题
1. **端口冲突**: 检查12345和8000端口占用
2. **数据库错误**: 检查SQLite文件权限
3. **API调用失败**: 检查跨域配置
4. **静态文件404**: 检查文件路径配置

#### 日志查看
```bash
# 前端日志
tail -f instance/flask.log

# 后端日志  
tail -f backend/data/system.log

# 系统日志
journalctl -u knowtax-service
```

---

**文档版本**: v1.0.0  
**最后更新**: 2024年1月  
**维护团队**: KnowTax开发组 