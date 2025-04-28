from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/permissions')
def permissions():
    return render_template('permissions.html', title="权限管理")

@admin_bp.route('/user-status')
def user_status():
    return render_template('user_status.html', title="用户状态")

@admin_bp.route('/')
def admin():
    return render_template('index_admin.html', title="系统管理员")