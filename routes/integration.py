from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import requests
from functools import wraps

integration_bp = Blueprint('integration', __name__, url_prefix='/integration')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Backend API base URL
BACKEND_URL = 'http://localhost:8000'

@integration_bp.route('/dashboard')
@login_required
def dashboard():
    """Backend integration dashboard"""
    return render_template('backend_integration.html')

@integration_bp.route('/enhanced-features')
@login_required
def enhanced_features():
    """Enhanced features page with backend integration"""
    return render_template('enhanced_features.html')

@integration_bp.route('/api/proxy/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def api_proxy(endpoint):
    """Proxy API calls to backend service"""
    try:
        # Construct the full backend URL
        backend_url = f"{BACKEND_URL}/{endpoint}"
        
        # Forward query parameters
        if request.args:
            backend_url += '?' + '&'.join([f"{k}={v}" for k, v in request.args.items()])
        
        # Prepare request data
        request_data = None
        headers = {'Content-Type': 'application/json'}
        
        if request.method in ['POST', 'PUT'] and request.is_json:
            request_data = request.get_json()
        
        # Make the request to backend
        if request.method == 'GET':
            response = requests.get(backend_url, timeout=30)
        elif request.method == 'POST':
            response = requests.post(backend_url, json=request_data, headers=headers, timeout=30)
        elif request.method == 'PUT':
            response = requests.put(backend_url, json=request_data, headers=headers, timeout=30)
        elif request.method == 'DELETE':
            response = requests.delete(backend_url, timeout=30)
        
        # Return the response
        return jsonify(response.json()), response.status_code
        
    except requests.RequestException as e:
        return jsonify({
            'code': 500,
            'message': f'Backend service unavailable: {str(e)}',
            'data': None
        }), 500
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Internal error: {str(e)}',
            'data': None
        }), 500

@integration_bp.route('/check-backend-status')
@login_required
def check_backend_status():
    """Check if backend service is available"""
    try:
        response = requests.get(f"{BACKEND_URL}/system/status", timeout=10)
        if response.status_code == 200:
            return jsonify({
                'status': 'online',
                'message': 'Backend service is available',
                'data': response.json()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Backend service returned error',
                'data': None
            })
    except requests.RequestException:
        return jsonify({
            'status': 'offline',
            'message': 'Backend service is not available',
            'data': None
        })

@integration_bp.route('/knowledge-management')
@login_required
def knowledge_management():
    """Knowledge management interface"""
    return render_template('knowledge_management.html')

@integration_bp.route('/qa-system')
@login_required
def qa_system():
    """QA system interface"""
    return render_template('qa_system.html')

@integration_bp.route('/announcement-generator')
@login_required
def announcement_generator():
    """Announcement generator interface"""
    return render_template('announcement_generator.html')

@integration_bp.route('/crawler-monitor')
@login_required
def crawler_monitor():
    """Crawler monitoring interface"""
    return render_template('crawler_monitor.html')

@integration_bp.route('/version-control')
@login_required
def version_control():
    """Version control interface"""
    return render_template('version_control.html') 