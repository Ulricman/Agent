from flask import Blueprint, jsonify, request, session
from models.user import db, Memo, Notification
from datetime import datetime

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/api/notifications')
def get_notifications():
    # 获取所有通知
    notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    return jsonify({
        'notifications': [{
            'date': n.created_at.strftime('%Y-%m-%d'),
            'time': n.created_at.strftime('%H:%M'),
            'content': n.content
        } for n in notifications]
    })

@notification_bp.route('/get_memos')
def get_memos():
    if 'role' not in session:
        return jsonify({'success': False, 'message': '未登录'})
    
    role = session['role']
    # 只获取当前用户角色的备忘录
    memos = Memo.query.filter_by(role=role).order_by(Memo.created_at.desc()).all()
    
    memo_list = [{
        'id': memo.id,
        'title': memo.title,
        'content': memo.content,
        'created_at': memo.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for memo in memos]
    
    return jsonify({'success': True, 'memos': memo_list})

@notification_bp.route('/save_memo', methods=['POST'])
def save_memo():
    if 'role' not in session:
        return jsonify({'success': False, 'message': '未登录'})
    
    title = request.form.get('title')
    content = request.form.get('content')
    role = session['role']  # 使用session中的角色，而不是从前端获取
    
    if not title or not content:
        return jsonify({'success': False, 'message': '标题和内容不能为空'})
    
    try:
        new_memo = Memo(
            title=title,
            content=content,
            role=role,
            created_at=datetime.now()
        )
        db.session.add(new_memo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'memo': {
                'id': new_memo.id,
                'title': new_memo.title,
                'content': new_memo.content,
                'created_at': new_memo.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@notification_bp.route('/delete_memo/<int:memo_id>', methods=['POST'])
def delete_memo(memo_id):
    if 'role' not in session:
        return jsonify({'success': False, 'message': '未登录'})
    
    memo = Memo.query.get_or_404(memo_id)
    
    # 确保只能删除自己角色的备忘录
    if memo.role != session['role']:
        return jsonify({'success': False, 'message': '无权删除此备忘录'})
    
    try:
        db.session.delete(memo)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}) 