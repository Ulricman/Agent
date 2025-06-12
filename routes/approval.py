from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from models import db, ApprovalRequest, ApprovalHistory, QAItem, KnowledgeItem
from datetime import datetime
import json

approval_bp = Blueprint('approval', __name__)

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('需要管理员权限', 'error')
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def manager_or_admin_required(f):
    def decorated_function(*args, **kwargs):
        if session.get('role') not in ['admin', 'manager']:
            flash('需要管理员或经理权限', 'error')
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# API Routes for approval workflow

@approval_bp.route('/api/submit', methods=['POST'])
@login_required
def submit_for_approval():
    """Submit content for approval"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content_type', 'title', 'content', 'action_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
        
        # Create approval request
        approval_request = ApprovalRequest(
            content_type=data['content_type'],
            title=data['title'],
            content=data['content'],
            submitter_id=session['user_id'],
            submitter_name=session['username'],
            action_type=data['action_type'],
            content_id=data.get('content_id'),
            category=data.get('category'),
            tags=data.get('tags'),
            priority=data.get('priority', 'normal'),
            question=data.get('question'),
            answer=data.get('answer')
        )
        
        db.session.add(approval_request)
        db.session.flush()  # Get the ID
        
        # Create history entry
        history = ApprovalHistory(
            request_id=approval_request.id,
            action='submitted',
            actor_id=session['user_id'],
            actor_name=session['username'],
            actor_role=session['role'],
            comment=data.get('submission_comment')
        )
        
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '内容已提交审批',
            'request_id': approval_request.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'提交失败: {str(e)}'}), 500

@approval_bp.route('/api/requests', methods=['GET'])
@login_required
@manager_or_admin_required
def get_approval_requests():
    """Get approval requests based on user role"""
    try:
        status = request.args.get('status', 'pending')
        content_type = request.args.get('content_type')
        priority = request.args.get('priority')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Build query based on user role
        query = ApprovalRequest.query
        
        if session['role'] == 'manager':
            # Managers can only see QA requests
            query = query.filter(ApprovalRequest.content_type == 'qa')
        
        # Apply filters
        if status:
            query = query.filter(ApprovalRequest.status == status)
        if content_type:
            query = query.filter(ApprovalRequest.content_type == content_type)
        if priority:
            query = query.filter(ApprovalRequest.priority == priority)
        
        # Order by priority and creation date
        priority_order = {
            'urgent': 1,
            'high': 2,
            'normal': 3,
            'low': 4
        }
        
        requests = query.order_by(
            ApprovalRequest.created_at.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [req.to_dict() for req in requests.items],
            'total': requests.total,
            'pages': requests.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取审批请求失败: {str(e)}'}), 500

@approval_bp.route('/api/requests/<int:request_id>', methods=['GET'])
@login_required
@manager_or_admin_required
def get_approval_request(request_id):
    """Get specific approval request with history"""
    try:
        approval_request = ApprovalRequest.query.get_or_404(request_id)
        
        # Check permissions
        if session['role'] == 'manager' and approval_request.content_type != 'qa':
            return jsonify({'success': False, 'message': '权限不足'}), 403
        
        # Get history
        history = ApprovalHistory.query.filter_by(request_id=request_id).order_by(
            ApprovalHistory.timestamp.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'data': {
                'request': approval_request.to_dict(),
                'history': [h.to_dict() for h in history]
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取审批详情失败: {str(e)}'}), 500

@approval_bp.route('/api/requests/<int:request_id>/approve', methods=['PUT'])
@login_required
@manager_or_admin_required
def approve_request(request_id):
    """Approve an approval request"""
    try:
        data = request.get_json()
        approval_request = ApprovalRequest.query.get_or_404(request_id)
        
        # Check permissions
        if session['role'] == 'manager' and approval_request.content_type != 'qa':
            return jsonify({'success': False, 'message': '权限不足'}), 403
        
        if approval_request.status != 'pending':
            return jsonify({'success': False, 'message': '该请求已被处理'}), 400
        
        # Update approval request
        approval_request.status = 'approved'
        approval_request.reviewer_id = session['user_id']
        approval_request.reviewer_name = session['username']
        approval_request.review_comment = data.get('comment', '')
        approval_request.reviewed_at = datetime.utcnow()
        
        # Create history entry
        history = ApprovalHistory(
            request_id=request_id,
            action='approved',
            actor_id=session['user_id'],
            actor_name=session['username'],
            actor_role=session['role'],
            comment=data.get('comment')
        )
        db.session.add(history)
        
        # Create actual content based on approval
        if approval_request.action_type == 'create':
            if approval_request.content_type == 'qa':
                qa_item = QAItem(
                    question=approval_request.question or approval_request.title,
                    answer=approval_request.answer or approval_request.content,
                    category=approval_request.category,
                    tags=approval_request.tags,
                    created_by=approval_request.submitter_id
                )
                db.session.add(qa_item)
            elif approval_request.content_type == 'knowledge':
                knowledge_item = KnowledgeItem(
                    title=approval_request.title,
                    content=approval_request.content,
                    category=approval_request.category,
                    tags=approval_request.tags,
                    created_by=approval_request.submitter_id
                )
                db.session.add(knowledge_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '内容已批准并发布'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'批准失败: {str(e)}'}), 500

@approval_bp.route('/api/requests/<int:request_id>/reject', methods=['PUT'])
@login_required
@manager_or_admin_required
def reject_request(request_id):
    """Reject an approval request"""
    try:
        data = request.get_json()
        approval_request = ApprovalRequest.query.get_or_404(request_id)
        
        # Check permissions
        if session['role'] == 'manager' and approval_request.content_type != 'qa':
            return jsonify({'success': False, 'message': '权限不足'}), 403
        
        if approval_request.status != 'pending':
            return jsonify({'success': False, 'message': '该请求已被处理'}), 400
        
        # Update approval request
        approval_request.status = 'rejected'
        approval_request.reviewer_id = session['user_id']
        approval_request.reviewer_name = session['username']
        approval_request.review_comment = data.get('comment', '')
        approval_request.reviewed_at = datetime.utcnow()
        
        # Create history entry
        history = ApprovalHistory(
            request_id=request_id,
            action='rejected',
            actor_id=session['user_id'],
            actor_name=session['username'],
            actor_role=session['role'],
            comment=data.get('comment')
        )
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '内容已拒绝'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'拒绝失败: {str(e)}'}), 500

@approval_bp.route('/api/requests/<int:request_id>/modify', methods=['PUT'])
@login_required
@manager_or_admin_required
def modify_request(request_id):
    """Modify content during review"""
    try:
        data = request.get_json()
        approval_request = ApprovalRequest.query.get_or_404(request_id)
        
        # Check permissions
        if session['role'] == 'manager' and approval_request.content_type != 'qa':
            return jsonify({'success': False, 'message': '权限不足'}), 403
        
        if approval_request.status != 'pending':
            return jsonify({'success': False, 'message': '该请求已被处理'}), 400
        
        # Update content
        if 'title' in data:
            approval_request.title = data['title']
        if 'content' in data:
            approval_request.content = data['content']
        if 'question' in data:
            approval_request.question = data['question']
        if 'answer' in data:
            approval_request.answer = data['answer']
        if 'category' in data:
            approval_request.category = data['category']
        if 'tags' in data:
            approval_request.tags = data['tags']
        
        # Create history entry
        history = ApprovalHistory(
            request_id=request_id,
            action='modified',
            actor_id=session['user_id'],
            actor_name=session['username'],
            actor_role=session['role'],
            comment=data.get('comment', '内容已修改')
        )
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '内容已修改'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'修改失败: {str(e)}'}), 500

@approval_bp.route('/api/stats', methods=['GET'])
@login_required
@manager_or_admin_required
def get_approval_stats():
    """Get approval statistics"""
    try:
        # Base query based on role
        base_query = ApprovalRequest.query
        if session['role'] == 'manager':
            base_query = base_query.filter(ApprovalRequest.content_type == 'qa')
        
        stats = {
            'pending': base_query.filter(ApprovalRequest.status == 'pending').count(),
            'approved': base_query.filter(ApprovalRequest.status == 'approved').count(),
            'rejected': base_query.filter(ApprovalRequest.status == 'rejected').count(),
            'total': base_query.count()
        }
        
        # Priority breakdown
        priority_stats = {}
        for priority in ['urgent', 'high', 'normal', 'low']:
            priority_stats[priority] = base_query.filter(
                ApprovalRequest.priority == priority,
                ApprovalRequest.status == 'pending'
            ).count()
        
        stats['priority_breakdown'] = priority_stats
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取统计失败: {str(e)}'}), 500

# Demo data creation endpoint
@approval_bp.route('/api/create-demo-data', methods=['POST'])
@login_required
@admin_required
def create_demo_data():
    """Create demo approval requests for testing"""
    try:
        demo_requests = [
            {
                'content_type': 'qa',
                'title': '增值税发票开具规定',
                'question': '企业开具增值税发票有哪些基本要求？',
                'answer': '企业开具增值税发票需要遵循以下基本要求：1. 必须如实开具，不得虚开；2. 必须按照规定的时限开具；3. 必须使用税务机关监制的发票；4. 必须按照发票联次开具...',
                'category': '增值税',
                'tags': '发票,开具,规定',
                'priority': 'high',
                'action_type': 'create'
            },
            {
                'content_type': 'knowledge',
                'title': '2024年企业所得税优惠政策汇总',
                'content': '2024年企业所得税优惠政策主要包括：1. 小微企业所得税优惠政策延续；2. 高新技术企业减按15%税率征收；3. 研发费用加计扣除比例提高...',
                'category': '企业所得税',
                'tags': '优惠政策,2024,企业所得税',
                'priority': 'urgent',
                'action_type': 'create'
            },
            {
                'content_type': 'qa',
                'title': '个人所得税专项附加扣除',
                'question': '个人所得税专项附加扣除包括哪些项目？',
                'answer': '个人所得税专项附加扣除包括：1. 子女教育；2. 继续教育；3. 大病医疗；4. 住房贷款利息；5. 住房租金；6. 赡养老人；7. 3岁以下婴幼儿照护...',
                'category': '个人所得税',
                'tags': '专项附加扣除,个税',
                'priority': 'normal',
                'action_type': 'create'
            }
        ]
        
        for demo_data in demo_requests:
            approval_request = ApprovalRequest(
                content_type=demo_data['content_type'],
                title=demo_data['title'],
                content=demo_data.get('content', demo_data.get('answer', '')),
                submitter_id=1,  # Assuming user ID 1 exists
                submitter_name='演示用户',
                action_type=demo_data['action_type'],
                category=demo_data['category'],
                tags=demo_data['tags'],
                priority=demo_data['priority'],
                question=demo_data.get('question'),
                answer=demo_data.get('answer')
            )
            
            db.session.add(approval_request)
            db.session.flush()
            
            # Create submission history
            history = ApprovalHistory(
                request_id=approval_request.id,
                action='submitted',
                actor_id=1,
                actor_name='演示用户',
                actor_role='service',
                comment='演示数据提交'
            )
            db.session.add(history)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'已创建 {len(demo_requests)} 条演示审批请求'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'创建演示数据失败: {str(e)}'}), 500 