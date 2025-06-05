from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel

from modules.html_generator import HTMLGenerator
from modules.version_manager import VersionManager
from modules.crawler import AnnouncementCrawler
from modules.knowledge_base import KnowledgeBase
from modules.qa_system import QASystem
from modules.logger import StructuredLogger
from modules.backup_manager import BackupManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = StructuredLogger()

app = FastAPI(title="Tax Knowledge Backend", version="1.0.0")

# CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving HTML announcements
app.mount("/static/announcements", StaticFiles(directory="data/announcements"), name="announcements")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize modules
html_gen = HTMLGenerator()
version_mgr = VersionManager()
crawler = AnnouncementCrawler()
knowledge_base = KnowledgeBase()
qa_system = QASystem()
backup_mgr = BackupManager()

@app.on_event("startup")
async def startup_event():
    """Initialize databases and create necessary directories"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    # Initialize knowledge base and QA system
    await knowledge_base.initialize()
    await qa_system.initialize()
    
    logger.log_info("Backend server started successfully")

# Pydantic models
class TaxItem(BaseModel):
    id: str
    title: str
    content: str
    category: str
    effective_date: str
    status: str = "active"

class QAItem(BaseModel):
    id: str
    question: str
    answer: str
    category: str
    keywords: List[str]

class VersionRelease(BaseModel):
    version: str
    changes: List[Dict]
    release_notes: str

# HTML Generation Endpoints
@app.get("/api/generate-announcement")
async def generate_announcement():
    """Generate a sample tax announcement HTML"""
    html_content = await html_gen.generate_sample_announcement()
    return HTMLResponse(content=html_content)

@app.post("/api/create-custom-announcement")
async def create_custom_announcement(items: List[TaxItem]):
    """Create custom tax announcement from provided items"""
    html_content = await html_gen.create_announcement(items)
    return {"html": html_content, "timestamp": datetime.now().isoformat()}

# Version Management Endpoints
@app.get("/api/versions")
async def get_versions():
    """Get all available versions"""
    return await version_mgr.get_all_versions()

@app.post("/api/versions/release")
async def release_version(release: VersionRelease):
    """Release a new version of announcements"""
    result = await version_mgr.create_release(release.version, release.changes, release.release_notes)
    logger.log_info(f"New version released: {release.version}")
    return result

@app.get("/api/versions/{version}")
async def get_version_details(version: str):
    """Get details of a specific version"""
    return await version_mgr.get_version_details(version)

@app.post("/api/versions/{version}/rollback")
async def rollback_version(version: str):
    """Rollback to a specific version"""
    result = await version_mgr.rollback_to_version(version)
    logger.log_info(f"Rolled back to version: {version}")
    return result

# Crawler Endpoints
@app.post("/api/crawler/check")
async def check_for_updates():
    """Manually trigger crawler to check for new announcements"""
    result = await crawler.check_for_updates()
    logger.log_info("Manual crawler check initiated")
    return result

@app.get("/api/crawler/status")
async def get_crawler_status():
    """Get current crawler status"""
    return await crawler.get_status()

@app.post("/api/crawler/parse")
async def parse_html(html_path: str):
    """Parse specific HTML file"""
    result = await crawler.parse_html_file(html_path)
    return result

# Knowledge Base Endpoints
@app.get("/api/knowledge")
async def get_knowledge_items():
    """Get all knowledge base items"""
    return await knowledge_base.get_all_items()

@app.post("/api/knowledge")
async def add_knowledge_item(item: TaxItem):
    """Add new knowledge item"""
    result = await knowledge_base.add_item(item.dict())
    logger.log_info(f"Knowledge item added: {item.id}")
    return result

@app.put("/api/knowledge/{item_id}")
async def update_knowledge_item(item_id: str, item: TaxItem):
    """Update knowledge item"""
    result = await knowledge_base.update_item(item_id, item.dict())
    logger.log_info(f"Knowledge item updated: {item_id}")
    return result

@app.delete("/api/knowledge/{item_id}")
async def delete_knowledge_item(item_id: str):
    """Delete knowledge item"""
    result = await knowledge_base.delete_item(item_id)
    logger.log_info(f"Knowledge item deleted: {item_id}")
    return result

@app.get("/api/knowledge/search")
async def search_knowledge(q: str):
    """Search knowledge base"""
    return await knowledge_base.search(q)

@app.post("/api/knowledge/init")
async def init_knowledge_from_file(file_path: str):
    """Initialize knowledge base from JSON file"""
    result = await knowledge_base.init_from_file(file_path)
    logger.log_info(f"Knowledge base initialized from: {file_path}")
    return result

@app.get("/api/knowledge/export")
async def export_knowledge():
    """Export entire knowledge base"""
    return await knowledge_base.export_all()

# QA System Endpoints
@app.get("/api/qa")
async def get_qa_items():
    """Get all QA items"""
    return await qa_system.get_all_items()

@app.post("/api/qa")
async def add_qa_item(item: QAItem):
    """Add new QA item"""
    result = await qa_system.add_item(item.dict())
    logger.log_info(f"QA item added: {item.id}")
    return result

@app.put("/api/qa/{item_id}")
async def update_qa_item(item_id: str, item: QAItem):
    """Update QA item"""
    result = await qa_system.update_item(item_id, item.dict())
    logger.log_info(f"QA item updated: {item_id}")
    return result

@app.delete("/api/qa/{item_id}")
async def delete_qa_item(item_id: str):
    """Delete QA item"""
    result = await qa_system.delete_item(item_id)
    logger.log_info(f"QA item deleted: {item_id}")
    return result

@app.get("/api/qa/search")
async def search_qa(q: str):
    """Search QA database"""
    return await qa_system.search(q)

@app.post("/api/qa/ask")
async def ask_question(question: str):
    """Ask a question and get simulated LLM response"""
    return await qa_system.ask_question(question)

@app.post("/api/qa/init")
async def init_qa_from_file(file_path: str):
    """Initialize QA system from JSON file"""
    result = await qa_system.init_from_file(file_path)
    logger.log_info(f"QA system initialized from: {file_path}")
    return result

@app.get("/api/qa/export")
async def export_qa():
    """Export entire QA database"""
    return await qa_system.export_all()

# Update Process Endpoints
@app.post("/api/update/process")
async def process_updates(background_tasks: BackgroundTasks):
    """Process updates from new HTML content"""
    background_tasks.add_task(run_update_process)
    return {"message": "Update process started in background"}

async def run_update_process():
    """Background task to process updates"""
    try:
        # Check for new content
        crawler_result = await crawler.check_for_updates()
        
        if crawler_result.get("has_updates"):
            # Update knowledge base
            kb_result = await knowledge_base.process_updates(crawler_result["updates"])
            
            # Update QA system
            qa_result = await qa_system.process_updates(crawler_result["updates"])
            
            logger.log_info("Update process completed successfully", {
                "crawler_result": crawler_result,
                "knowledge_base_result": kb_result,
                "qa_result": qa_result
            })
        else:
            logger.log_info("No updates found")
            
    except Exception as e:
        logger.log_error(f"Update process failed: {str(e)}")

# Dashboard Endpoints
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    kb_stats = await knowledge_base.get_stats()
    qa_stats = await qa_system.get_stats()
    crawler_stats = await crawler.get_stats()
    
    return {
        "knowledge_base": kb_stats,
        "qa_system": qa_stats,
        "crawler": crawler_stats,
        "last_updated": datetime.now().isoformat()
    }

# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Serve static files for web interface
app.mount("/static", StaticFiles(directory="static"), name="static")

# Web interface
@app.get("/", response_class=HTMLResponse)
async def web_interface():
    """Serve the web interface for database management"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/html-manager", response_class=HTMLResponse)
async def html_manager_interface():
    """HTML file management interface"""
    try:
        with open("templates/html_manager.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>HTML文件管理器</title>
            <link href="https://cdn.bootcdn.net/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-info">
                    <h4><i class="fas fa-wrench"></i> HTML文件管理器</h4>
                    <p>此功能正在开发中。您可以通过以下API端点管理HTML文件：</p>
                    <ul>
                        <li><code>GET /html/files</code> - 获取所有HTML文件列表</li>
                        <li><code>POST /html/create</code> - 创建新的HTML文件</li>
                        <li><code>DELETE /html/files/{filename}</code> - 删除指定文件</li>
                        <li><code>POST /html/create-from-url</code> - 从URL抓取内容创建文件</li>
                    </ul>
                    <a href="/" class="btn btn-primary">返回主页</a>
                </div>
            </div>
        </body>
        </html>
        """, status_code=200)

@app.get("/backup-manager", response_class=HTMLResponse)
async def backup_manager_interface():
    """Backup management interface"""
    try:
        with open("templates/backup_manager.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>系统备份管理</title>
            <link href="https://cdn.bootcdn.net/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-info">
                    <h4><i class="fas fa-database"></i> 系统备份管理</h4>
                    <p>此功能正在开发中。您可以通过以下API端点管理系统备份：</p>
                    <ul>
                        <li><code>POST /api/backup/create</code> - 创建系统备份</li>
                        <li><code>GET /api/backup/list</code> - 获取备份列表</li>
                        <li><code>POST /api/backup/restore</code> - 恢复备份</li>
                        <li><code>POST /api/backup/reset</code> - 重置系统到默认状态</li>
                    </ul>
                    <a href="/" class="btn btn-primary">返回主页</a>
                </div>
            </div>
        </body>
        </html>
        """, status_code=200)

# Additional endpoints for frontend integration
@app.post("/knowledge/add")
async def add_knowledge_frontend(request: Request):
    """Frontend compatible knowledge add endpoint"""
    try:
        data = await request.json()
        # Convert frontend format to backend format
        item = {
            "id": f"kb_{len(knowledge_base.knowledge_data) + 1:03d}",
            "title": data.get("title", ""),
            "content": data.get("content", ""),
            "category": data.get("category", "其他"),
            "keywords": data.get("keywords", []),
            "effective_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "active"
        }
        result = await knowledge_base.add_item(item)
        return {"code": 200, "message": "Knowledge item added successfully", "data": item}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.get("/knowledge")
async def get_knowledge_frontend():
    """Frontend compatible knowledge get endpoint"""
    try:
        # Return sample knowledge data for now
        sample_data = [
            {
                "id": "kb_001",
                "title": "增值税税率说明",
                "content": "增值税是以商品（含应税劳务）在流转过程中产生的增值额作为计税依据而征收的一种流转税。",
                "category": "增值税",
                "keywords": ["增值税", "税率", "计算"],
                "effective_date": "2024-01-01",
                "status": "active"
            },
            {
                "id": "kb_002", 
                "title": "企业所得税申报",
                "content": "企业所得税是对企业所得征收的一种税。企业应当按规定申报企业所得税。",
                "category": "企业所得税",
                "keywords": ["企业所得税", "申报", "流程"],
                "effective_date": "2024-01-01",
                "status": "active"
            }
        ]
        return {"code": 200, "message": "Success", "data": sample_data}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": []}

@app.get("/knowledge/search")
async def search_knowledge_frontend(q: str):
    """Frontend compatible knowledge search endpoint"""
    try:
        result = await knowledge_base.search(q)
        return {"code": 200, "message": "Success", "data": result.get("items", [])}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": []}

@app.post("/qa/add")
async def add_qa_frontend(request: Request):
    """Frontend compatible QA add endpoint"""
    try:
        data = await request.json()
        item = {
            "id": f"qa_{len(qa_system.qa_data) + 1:03d}",
            "question": data.get("question", ""),
            "answer": data.get("answer", ""),
            "category": data.get("category", "其他"),
            "keywords": [data.get("question", "").split()[0]] if data.get("question") else []
        }
        result = await qa_system.add_item(item)
        return {"code": 200, "message": "QA pair added successfully", "data": item}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.get("/qa")
async def get_qa_frontend():
    """Frontend compatible QA get endpoint"""
    try:
        # Return sample QA data for now
        sample_data = [
            {
                "id": "qa_001",
                "question": "如何计算增值税？",
                "answer": "增值税的计算公式为：应纳税额 = 销项税额 - 进项税额。销项税额 = 销售额 × 税率。",
                "category": "增值税",
                "keywords": ["增值税", "计算", "公式"]
            },
            {
                "id": "qa_002",
                "question": "企业所得税税率是多少？",
                "answer": "企业所得税的基本税率为25%。符合条件的小型微利企业，减按20%的税率征收企业所得税。",
                "category": "企业所得税", 
                "keywords": ["企业所得税", "税率", "小微企业"]
            },
            {
                "id": "qa_003",
                "question": "什么是个人所得税起征点？",
                "answer": "个人所得税起征点是指个人所得税的免征额度。目前综合所得的基本减除费用标准为每年60000元（每月5000元）。",
                "category": "个人所得税",
                "keywords": ["个人所得税", "起征点", "免征额"]
            }
        ]
        return {"code": 200, "message": "Success", "data": sample_data}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": []}

@app.post("/qa/ask")
async def ask_question_frontend(request: Request):
    """Frontend compatible QA ask endpoint"""
    try:
        data = await request.json()
        question = data.get("question", "")
        
        # Simple matching logic for demo
        qa_database = [
            {
                "question": "如何计算增值税",
                "answer": "增值税的计算公式为：应纳税额 = 销项税额 - 进项税额。销项税额 = 销售额 × 税率。",
                "confidence": 0.95
            },
            {
                "question": "企业所得税税率",
                "answer": "企业所得税的基本税率为25%。符合条件的小型微利企业，减按20%的税率征收企业所得税。",
                "confidence": 0.90
            },
            {
                "question": "个人所得税起征点",
                "answer": "个人所得税起征点是指个人所得税的免征额度。目前综合所得的基本减除费用标准为每年60000元（每月5000元）。",
                "confidence": 0.88
            }
        ]
        
        # Find best match
        best_match = None
        highest_score = 0
        
        for qa in qa_database:
            # Simple keyword matching
            score = 0
            question_lower = question.lower()
            qa_question_lower = qa["question"].lower()
            
            if qa_question_lower in question_lower or question_lower in qa_question_lower:
                score = qa["confidence"]
            else:
                # Check for keyword overlap
                question_words = set(question_lower.split())
                qa_words = set(qa_question_lower.split())
                overlap = len(question_words & qa_words)
                if overlap > 0:
                    score = 0.6 + (overlap * 0.1)
            
            if score > highest_score:
                highest_score = score
                best_match = qa
        
        if best_match and highest_score > 0.5:
            result = {
                "answer": best_match["answer"],
                "confidence": highest_score,
                "question": question
            }
        else:
            result = {
                "answer": "抱歉，我暂时无法回答这个问题。建议您咨询专业的税务人员或查阅相关税务法规。",
                "confidence": 0.3,
                "question": question
            }
        
        return {"code": 200, "message": "Success", "data": result}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.get("/crawler/status")
async def get_crawler_status_frontend():
    """Frontend compatible crawler status endpoint"""
    try:
        result = await crawler.get_status()
        return {"code": 200, "message": "Success", "data": result}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": {"status": "error"}}

@app.post("/crawler/check")
async def trigger_crawler_check_frontend():
    """Frontend compatible crawler check endpoint"""
    try:
        result = await crawler.check_for_updates()
        return {"code": 200, "message": "Crawler check completed", "data": result}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.post("/html/generate-example")
async def generate_example_html_frontend():
    """Frontend compatible HTML generation endpoint"""
    try:
        # Generate HTML content directly - create a sample announcement
        current_date = datetime.now().strftime('%Y年%m月%d日')
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>税务政策更新公告</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 20px; }}
        .content {{ margin: 30px 0; line-height: 1.8; font-size: 16px; }}
        .highlight {{ background: #e8f4f8; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 40px; color: #666; border-top: 1px solid #eee; padding-top: 20px; }}
        .date {{ font-weight: bold; color: #e74c3c; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>增值税税率调整通知</h1>
        <div class="content">
            <p>根据《中华人民共和国增值税暂行条例》及相关法规，经国务院批准，现就调整增值税税率有关事项通知如下：</p>
            
            <div class="highlight">
                <h3>主要调整内容：</h3>
                <ul>
                    <li>一般纳税人销售货物、劳务、有形动产租赁服务或者进口货物，原适用17%税率的，税率调整为16%</li>
                    <li>原适用11%税率的，税率调整为10%</li>
                    <li>原适用6%税率的服务业继续执行6%税率</li>
                </ul>
            </div>
            
            <p><strong>生效时间：</strong>本通知自2024年1月1日起执行。</p>
            <p><strong>适用范围：</strong>全国范围内的增值税一般纳税人。</p>
            
            <div class="highlight">
                <p><strong>重要提醒：</strong>请各企业及时调整税务申报系统，确保新税率的正确应用。如有疑问，请咨询当地税务机关。</p>
            </div>
        </div>
        <div class="footer">
            <p class="date">发布日期: {current_date}</p>
            <p>国家税务总局</p>
        </div>
    </div>
</body>
</html>"""
        
        return {"code": 200, "message": "Example HTML generated", "data": {"html_content": html_content}}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.post("/html/generate")
async def generate_custom_html_frontend(request: Request):
    """Frontend compatible custom HTML generation endpoint"""
    try:
        data = await request.json()
        # Extract content and process line breaks outside f-string
        title = data.get('title', '税务公告')
        content = data.get('content', '').replace('\n', '<br>')
        date_str = datetime.now().strftime('%Y年%m月%d日')
        
        # Create a simple HTML structure
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; text-align: center; }}
        .content {{ margin: 20px 0; line-height: 1.6; }}
        .footer {{ text-align: center; margin-top: 40px; color: #666; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="content">
        {content}
    </div>
    <div class="footer">
        <p>发布日期: {date_str}</p>
    </div>
</body>
</html>"""
        return {"code": 200, "message": "Custom HTML generated", "data": {"html_content": html_content}}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

# HTML File Management APIs
@app.get("/html/files")
async def get_html_files():
    """Get list of all HTML announcement files"""
    try:
        files = html_gen.get_all_announcements()
        return {"code": 200, "message": "Success", "data": files}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": []}

@app.post("/html/create")
async def create_named_html(request: Request):
    """Create HTML file with custom name"""
    try:
        data = await request.json()
        filename = data.get('filename', '')
        overwrite = data.get('overwrite', False)
        
        if not filename:
            return {"code": 400, "message": "文件名不能为空", "data": None}
        
        # Prepare content data
        content_data = {
            'title': data.get('title', '税务公告'),
            'content': data.get('content', ''),
            'category': data.get('category', '其他'),
            'announcement_id': data.get('announcement_id', f'ANNO-{datetime.now().strftime("%Y%m%d%H%M%S")}'),
            'effective_date': data.get('effective_date', datetime.now().strftime('%Y-%m-%d'))
        }
        
        result = await html_gen.create_named_announcement(filename, content_data, overwrite)
        
        if result['success']:
            return {"code": 200, "message": result['message'], "data": result}
        else:
            return {"code": 400, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.delete("/html/files/{filename}")
async def delete_html_file(filename: str):
    """Delete HTML announcement file"""
    try:
        result = await html_gen.delete_announcement(filename)
        
        if result['success']:
            return {"code": 200, "message": result['message'], "data": result}
        else:
            return {"code": 404, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.get("/html/files/{filename}")
async def get_html_file_content(filename: str):
    """Get content of specific HTML file"""
    try:
        result = await html_gen.get_announcement_content(filename)
        
        if result['success']:
            return {"code": 200, "message": "Success", "data": result}
        else:
            return {"code": 404, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.post("/html/files/{filename}/copy")
async def copy_html_file(filename: str, request: Request):
    """Copy HTML file with new name"""
    try:
        data = await request.json()
        target_filename = data.get('target_filename', '')
        
        if not target_filename:
            return {"code": 400, "message": "目标文件名不能为空", "data": None}
        
        result = await html_gen.copy_announcement(filename, target_filename)
        
        if result['success']:
            return {"code": 200, "message": result['message'], "data": result}
        else:
            return {"code": 400, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.post("/html/batch-delete")
async def batch_delete_html_files(request: Request):
    """Delete multiple HTML files"""
    try:
        data = await request.json()
        filenames = data.get('filenames', [])
        
        if not filenames:
            return {"code": 400, "message": "文件名列表不能为空", "data": None}
        
        result = await html_gen.batch_delete_announcements(filenames)
        
        return {"code": 200, "message": result['message'], "data": result}
        
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.post("/html/create-from-url")
async def create_html_from_url_simulation(request: Request):
    """Simulate creating HTML from URL crawling"""
    try:
        data = await request.json()
        url = data.get('url', '')
        filename = data.get('filename', '')
        
        if not url or not filename:
            return {"code": 400, "message": "URL和文件名不能为空", "data": None}
        
        # Simulate content extraction from URL
        simulated_content = {
            'title': f'从 {url} 抓取的公告',
            'content': f'这是模拟从 {url} 抓取到的税务公告内容。\n\n实际系统中，这里会包含从指定URL抓取到的真实内容。\n\n抓取时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            'category': '爬虫抓取',
            'announcement_id': f'CRAWL-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'effective_date': datetime.now().strftime('%Y-%m-%d'),
            'source_url': url
        }
        
        result = await html_gen.create_named_announcement(filename, simulated_content, data.get('overwrite', False))
        
        if result['success']:
            # Add URL simulation info
            result['simulation_info'] = {
                'simulated_url': url,
                'crawl_timestamp': datetime.now().isoformat(),
                'note': '这是模拟的URL抓取功能，实际部署时会连接真实的爬虫系统'
            }
            return {"code": 200, "message": result['message'], "data": result}
        else:
            return {"code": 400, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.get("/system/status")
async def get_system_status_frontend():
    """Frontend compatible system status endpoint"""
    try:
        return {"code": 200, "message": "System is online", "data": {"status": "online", "timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": {"status": "error"}}

@app.get("/version/history")
async def get_version_history_frontend():
    """Frontend compatible version history endpoint"""
    try:
        result = await version_mgr.get_all_versions()
        return {"code": 200, "message": "Success", "data": result.get("versions", [])}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": []}

@app.post("/version/create")
async def create_version_frontend(request: Request):
    """Frontend compatible version creation endpoint"""
    try:
        data = await request.json()
        release = VersionRelease(
            version=data.get("version", "1.0.0"),
            changes=[{"type": "create", "description": data.get("description", "")}],
            release_notes=data.get("description", "")
        )
        result = await version_mgr.create_release(release.version, release.changes, release.release_notes)
        return {"code": 200, "message": "Version created successfully", "data": result}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

# Backup Management Endpoints
@app.post("/api/backup/create")
async def create_backup(request: Request):
    """Create a system backup"""
    try:
        data = await request.json()
        backup_name = data.get('backup_name', None)
        
        result = backup_mgr.create_backup(backup_name)
        
        if result['success']:
            logger.log_info(f"Backup created: {result['backup_info']['name']}")
            return {"code": 200, "message": result['message'], "data": result['backup_info']}
        else:
            return {"code": 500, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.get("/api/backup/list")
async def list_backups():
    """List all available backups"""
    try:
        backups = backup_mgr.list_backups()
        return {"code": 200, "message": "Success", "data": backups}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": []}

@app.post("/api/backup/restore")
async def restore_backup(request: Request):
    """Restore system from backup"""
    try:
        data = await request.json()
        backup_name = data.get('backup_name', '')
        
        if not backup_name:
            return {"code": 400, "message": "备份名称不能为空", "data": None}
        
        result = backup_mgr.restore_backup(backup_name)
        
        if result['success']:
            logger.log_info(f"System restored from backup: {backup_name}")
            return {"code": 200, "message": result['message'], "data": result}
        else:
            return {"code": 400, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.post("/api/backup/reset")
async def reset_to_default():
    """Reset system to default state"""
    try:
        result = backup_mgr.reset_to_default()
        
        if result['success']:
            logger.log_info("System reset to default state")
            return {"code": 200, "message": result['message'], "data": result}
        else:
            return {"code": 500, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.delete("/api/backup/delete/{backup_name}")
async def delete_backup(backup_name: str):
    """Delete a backup"""
    try:
        result = backup_mgr.delete_backup(backup_name)
        
        if result['success']:
            logger.log_info(f"Backup deleted: {backup_name}")
            return {"code": 200, "message": result['message'], "data": result}
        else:
            return {"code": 404, "message": result['message'], "data": None}
            
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.get("/api/backup/status")
async def get_backup_status():
    """Get system backup status"""
    try:
        status = backup_mgr.get_system_status()
        return {"code": 200, "message": "Success", "data": status}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

# Frontend Backup Endpoints
@app.post("/backup/create")
async def create_backup_frontend(request: Request):
    """Frontend compatible backup creation"""
    try:
        data = await request.json()
        backup_name = data.get('backup_name', None)
        
        result = backup_mgr.create_backup(backup_name)
        return {"code": 200 if result['success'] else 500, "message": result['message'], "data": result.get('backup_info')}
        
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.get("/backup/list")
async def list_backups_frontend():
    """Frontend compatible backup listing"""
    try:
        backups = backup_mgr.list_backups()
        return {"code": 200, "message": "Success", "data": backups}
    except Exception as e:
        return {"code": 500, "message": str(e), "data": []}

@app.post("/backup/restore")
async def restore_backup_frontend(request: Request):
    """Frontend compatible backup restoration"""
    try:
        data = await request.json()
        backup_name = data.get('backup_name', '')
        
        result = backup_mgr.restore_backup(backup_name)
        return {"code": 200 if result['success'] else 400, "message": result['message'], "data": result}
        
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

@app.post("/backup/reset")
async def reset_system_frontend():
    """Frontend compatible system reset"""
    try:
        result = backup_mgr.reset_to_default()
        return {"code": 200 if result['success'] else 500, "message": result['message'], "data": result}
        
    except Exception as e:
        return {"code": 500, "message": str(e), "data": None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 