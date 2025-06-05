from flask import Blueprint, render_template, request, jsonify
import requests
import json
from datetime import datetime

backend_bp = Blueprint('backend', __name__)

# Backend API configuration
BACKEND_URL = "http://localhost:8000/api"

def make_backend_request(endpoint, method='GET', data=None):
    """Helper function to make requests to backend API"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, json=data, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=10)
        else:
            return {"error": "Unsupported HTTP method"}
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Backend error: {response.status_code}"}
            
    except requests.exceptions.ConnectionError:
        return {"error": "无法连接到后端服务器。请确保后端服务正在运行 (端口 8000)"}
    except requests.exceptions.Timeout:
        return {"error": "请求超时"}
    except Exception as e:
        return {"error": str(e)}

@backend_bp.route('/dashboard')
def dashboard():
    """Backend management dashboard"""
    return render_template('backend_dashboard.html')

@backend_bp.route('/api/status')
def backend_status():
    """Check backend status"""
    result = make_backend_request("/health")
    return jsonify(result)

@backend_bp.route('/api/dashboard/stats')
def dashboard_stats():
    """Get dashboard statistics from backend"""
    result = make_backend_request("/dashboard/stats")
    return jsonify(result)

# Knowledge Base endpoints
@backend_bp.route('/api/knowledge')
def get_knowledge():
    """Get all knowledge items"""
    result = make_backend_request("/knowledge")
    return jsonify(result)

@backend_bp.route('/api/knowledge/search')
def search_knowledge():
    """Search knowledge base"""
    query = request.args.get('q', '')
    result = make_backend_request(f"/knowledge/search?q={query}")
    return jsonify(result)

@backend_bp.route('/api/knowledge', methods=['POST'])
def add_knowledge():
    """Add new knowledge item"""
    data = request.get_json()
    result = make_backend_request("/knowledge", method='POST', data=data)
    return jsonify(result)

@backend_bp.route('/api/knowledge/<item_id>', methods=['PUT'])
def update_knowledge(item_id):
    """Update knowledge item"""
    data = request.get_json()
    result = make_backend_request(f"/knowledge/{item_id}", method='PUT', data=data)
    return jsonify(result)

@backend_bp.route('/api/knowledge/<item_id>', methods=['DELETE'])
def delete_knowledge(item_id):
    """Delete knowledge item"""
    result = make_backend_request(f"/knowledge/{item_id}", method='DELETE')
    return jsonify(result)

# QA System endpoints
@backend_bp.route('/api/qa')
def get_qa():
    """Get all QA items"""
    result = make_backend_request("/qa")
    return jsonify(result)

@backend_bp.route('/api/qa/search')
def search_qa():
    """Search QA database"""
    query = request.args.get('q', '')
    result = make_backend_request(f"/qa/search?q={query}")
    return jsonify(result)

@backend_bp.route('/api/qa', methods=['POST'])
def add_qa():
    """Add new QA item"""
    data = request.get_json()
    result = make_backend_request("/qa", method='POST', data=data)
    return jsonify(result)

@backend_bp.route('/api/qa/ask', methods=['POST'])
def ask_question():
    """Ask a question to the QA system"""
    data = request.get_json()
    question = data.get('question', '')
    result = make_backend_request("/qa/ask", method='POST', data={"question": question})
    return jsonify(result)

# Crawler endpoints
@backend_bp.route('/api/crawler/status')
def crawler_status():
    """Get crawler status"""
    result = make_backend_request("/crawler/status")
    return jsonify(result)

@backend_bp.route('/api/crawler/check', methods=['POST'])
def run_crawler():
    """Run crawler check"""
    result = make_backend_request("/crawler/check", method='POST')
    return jsonify(result)

# Version management endpoints
@backend_bp.route('/api/versions')
def get_versions():
    """Get all versions"""
    result = make_backend_request("/versions")
    return jsonify(result)

@backend_bp.route('/api/versions/release', methods=['POST'])
def create_release():
    """Create new release"""
    data = request.get_json()
    result = make_backend_request("/versions/release", method='POST', data=data)
    return jsonify(result)

# HTML generation endpoints
@backend_bp.route('/api/generate-announcement')
def generate_announcement():
    """Generate sample announcement"""
    result = make_backend_request("/generate-announcement")
    return jsonify(result)

@backend_bp.route('/api/announcements', methods=['POST'])
def create_announcement():
    """Create custom announcement"""
    data = request.get_json()
    result = make_backend_request("/create-custom-announcement", method='POST', data=data)
    return jsonify(result)

# Enhanced frontend routes for tax management
@backend_bp.route('/knowledge-management')
def knowledge_management():
    """Knowledge management interface"""
    return render_template('knowledge_management.html')

@backend_bp.route('/qa-management')
def qa_management():
    """QA system management interface"""
    return render_template('qa_management.html')

@backend_bp.route('/announcement-generator')
def announcement_generator():
    """Tax announcement generator interface"""
    return render_template('announcement_generator.html')

@backend_bp.route('/crawler-monitor')
def crawler_monitor():
    """Crawler monitoring interface"""
    return render_template('crawler_monitor.html')

@backend_bp.route('/version-control')
def version_control():
    """Version control interface"""
    return render_template('version_control.html')

# Integration with existing data endpoints
@backend_bp.route('/enhanced-policies')
def enhanced_policies():
    """Enhanced policies view with backend integration"""
    # Get data from backend
    backend_data = make_backend_request("/knowledge")
    
    # If backend is not available, fall back to mock data
    if "error" in backend_data:
        # Fallback to existing mock data structure
        backend_data = [
            {
                "id": "kb_fallback_1",
                "title": "增值税政策（后端离线）",
                "content": "后端服务当前不可用，显示本地数据",
                "category": "增值税",
                "effective_date": datetime.now().strftime('%Y-%m-%d'),
                "status": "active"
            }
        ]
    
    return render_template("enhanced_table.html", 
                         title="增强税务政策库", 
                         data=backend_data,
                         headers=["ID", "标题", "分类", "生效日期", "状态"],
                         backend_integration=True)

@backend_bp.route('/enhanced-qa')
def enhanced_qa():
    """Enhanced QA view with backend integration"""
    # Get data from backend
    backend_data = make_backend_request("/qa")
    
    # If backend is not available, fall back to mock data
    if "error" in backend_data:
        backend_data = [
            {
                "id": "qa_fallback_1",
                "question": "后端服务不可用时的问题示例",
                "answer": "这是在后端服务离线时显示的示例回答",
                "category": "系统",
                "confidence": 0.5
            }
        ]
    
    return render_template("enhanced_qa_table.html",
                         title="增强问答库",
                         data=backend_data,
                         headers=["ID", "问题", "回答", "分类", "置信度"],
                         backend_integration=True)

# Real-time data updates
@backend_bp.route('/api/live-updates')
def live_updates():
    """Get live updates from backend systems"""
    try:
        # Get latest updates from various backend components
        crawler_status = make_backend_request("/crawler/status")
        knowledge_stats = make_backend_request("/dashboard/stats")
        
        updates = {
            "timestamp": datetime.now().isoformat(),
            "crawler_status": crawler_status.get("status", "unknown"),
            "last_check": crawler_status.get("last_check"),
            "total_knowledge_items": knowledge_stats.get("knowledge_base", {}).get("total_items", 0),
            "total_qa_items": knowledge_stats.get("qa_system", {}).get("total_items", 0),
            "backend_available": "error" not in crawler_status
        }
        
        return jsonify(updates)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "backend_available": False,
            "timestamp": datetime.now().isoformat()
        })

# Smart search across all backend data
@backend_bp.route('/api/smart-search')
def smart_search():
    """Smart search across knowledge base and QA system"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({"results": [], "message": "请输入搜索关键词"})
    
    try:
        # Search both knowledge base and QA system
        kb_results = make_backend_request(f"/knowledge/search?q={query}")
        qa_results = make_backend_request(f"/qa/search?q={query}")
        
        # Combine and format results
        combined_results = []
        
        if isinstance(kb_results, list):
            for item in kb_results[:5]:  # Limit to top 5
                combined_results.append({
                    "type": "knowledge",
                    "title": item.get("title", ""),
                    "content": item.get("content", "")[:200] + "...",
                    "category": item.get("category", ""),
                    "relevance": item.get("_relevance_score", 0)
                })
        
        if isinstance(qa_results, list):
            for item in qa_results[:5]:  # Limit to top 5
                combined_results.append({
                    "type": "qa",
                    "title": item.get("question", ""),
                    "content": item.get("answer", "")[:200] + "...",
                    "category": item.get("category", ""),
                    "relevance": item.get("_relevance_score", 0)
                })
        
        # Sort by relevance
        combined_results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        
        return jsonify({
            "results": combined_results,
            "total": len(combined_results),
            "query": query
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "results": [],
            "query": query
        }) 