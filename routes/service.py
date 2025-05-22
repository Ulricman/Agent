from flask import Blueprint, render_template

service_bp = Blueprint('service', __name__)

@service_bp.route('/search')
def search():
    return render_template('search.html')

@service_bp.route('/user-status')
def user_status():
    return render_template('user_status.html')

@service_bp.route('/')
def admin():
    return render_template('index_service.html', title="知识服务岗")