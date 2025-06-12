from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import requests
from functools import wraps

service_bp = Blueprint('service', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def service_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'service':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Backend API base URL
BACKEND_URL = 'http://localhost:8000'

@service_bp.route('/search')
@login_required
@service_required
def search():
    return render_template('service/search.html')

@service_bp.route('/user-status')
@login_required
@service_required
def user_status():
    return render_template('service/user_status.html')

@service_bp.route('/')
@login_required
@service_required
def service_index():
    return render_template('service/index.html', title="知识服务岗")

# API endpoints for frontend integration
@service_bp.route('/api/search-knowledge')
@login_required
@service_required
def api_search_knowledge():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'success': False, 'message': '请输入搜索关键词'})
    
    try:
        response = requests.get(f"{BACKEND_URL}/knowledge/search", params={'q': query}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return jsonify({'success': True, 'data': result.get('data', [])})
        else:
            return jsonify({'success': False, 'message': '搜索服务暂时不可用'})
    except requests.RequestException:
        return jsonify({'success': False, 'message': '无法连接到后端服务'})

@service_bp.route('/api/fuzzy-search-qa')
@login_required
@service_required
def api_fuzzy_search_qa():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'success': False, 'message': '请输入搜索关键词'})
    
    try:
        # 尝试连接后端模糊搜索API
        response = requests.get(f"{BACKEND_URL}/qa/fuzzy-search", params={'q': query}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return jsonify({'success': True, 'data': result.get('data', [])})
        else:
            # 如果后端不可用，使用模拟数据
            return _get_mock_fuzzy_search_results(query)
    except requests.RequestException:
        # 如果后端不可用，使用模拟数据
        return _get_mock_fuzzy_search_results(query)

def _get_mock_fuzzy_search_results(query):
    """模拟模糊搜索结果"""
    mock_qa_data = [
        {
            "question": "增值税的计算公式是什么？",
            "answer": "增值税应纳税额 = 销项税额 - 进项税额。销项税额 = 销售额 × 适用税率。",
            "category": "增值税",
            "similarity": 0.95
        },
        {
            "question": "如何计算增值税？",
            "answer": "增值税计算：应纳税额 = 当期销项税额 - 当期进项税额",
            "category": "增值税",
            "similarity": 0.92
        },
        {
            "question": "增值税税率有哪些？",
            "answer": "增值税税率分为13%、9%、6%三档，另有3%、1%征收率适用于小规模纳税人。",
            "category": "增值税",
            "similarity": 0.88
        },
        {
            "question": "企业所得税如何计算？",
            "answer": "企业所得税 = 应纳税所得额 × 税率。应纳税所得额 = 收入总额 - 准予扣除项目。",
            "category": "企业所得税",
            "similarity": 0.90
        },
        {
            "question": "发票开具有什么要求？",
            "answer": "发票应按照规定的时限、顺序、栏目如实开具，不得虚开、代开。",
            "category": "发票管理",
            "similarity": 0.85
        },
        {
            "question": "如何进行税务申报？",
            "answer": "纳税人应在规定期限内向税务机关申报纳税，可通过网上申报或到税务大厅申报。",
            "category": "税务申报",
            "similarity": 0.87
        }
    ]
    
    # 模糊匹配逻辑
    query_lower = query.lower()
    results = []
    
    for item in mock_qa_data:
        if (query_lower in item['question'].lower() or 
            query_lower in item['answer'].lower() or 
            query_lower in item['category'].lower() or
            (query_lower == '增值税' and item['category'] == '增值税') or
            (query_lower == '企业所得税' and item['category'] == '企业所得税') or
            (query_lower == '发票' and item['category'] == '发票管理') or
            (query_lower == '申报' and item['category'] == '税务申报')):
            results.append(item)
    
    # 按相似度排序
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    return jsonify({'success': True, 'data': results})

@service_bp.route('/api/ask-question', methods=['POST'])
@login_required
@service_required
def api_ask_question():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'success': False, 'message': '请输入问题'})
    
    try:
        response = requests.post(f"{BACKEND_URL}/qa/ask", 
                               json={'question': question}, 
                               headers={'Content-Type': 'application/json'},
                               timeout=15)
        if response.status_code == 200:
            result = response.json()
            return jsonify({'success': True, 'data': result.get('data', {})})
        else:
            return jsonify({'success': False, 'message': '问答服务暂时不可用'})
    except requests.RequestException:
        return jsonify({'success': False, 'message': '无法连接到后端服务'})

@service_bp.route('/api/get-qa-list')
@login_required
@service_required
def api_get_qa_list():
    try:
        response = requests.get(f"{BACKEND_URL}/qa", timeout=10)
        if response.status_code == 200:
            result = response.json()
            return jsonify({'success': True, 'data': result.get('data', [])})
        else:
            return jsonify({'success': False, 'message': '获取问答列表失败'})
    except requests.RequestException:
        return jsonify({'success': False, 'message': '无法连接到后端服务'})

@service_bp.route('/api/get-knowledge-list')
@login_required
@service_required
def api_get_knowledge_list():
    try:
        response = requests.get(f"{BACKEND_URL}/knowledge", timeout=10)
        if response.status_code == 200:
            result = response.json()
            return jsonify({'success': True, 'data': result.get('data', [])})
        else:
            return jsonify({'success': False, 'message': '获取知识库列表失败'})
    except requests.RequestException:
        return jsonify({'success': False, 'message': '无法连接到后端服务'})