from flask import Flask, redirect, url_for, render_template, session
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.manager import manager_bp
from routes.service import service_bp
from routes.data import data_bp
from routes.backend import backend_bp
from routes.approval import approval_bp
from models.user import db, User

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 配置数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tax.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化数据库
db.init_app(app)

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(manager_bp, url_prefix="/manager")
app.register_blueprint(service_bp, url_prefix="/service")
app.register_blueprint(data_bp, url_prefix="/data")
app.register_blueprint(backend_bp, url_prefix="/backend")
app.register_blueprint(approval_bp, url_prefix="/approval")

# 注册新的集成蓝图
from routes.integration import integration_bp

app.register_blueprint(integration_bp)


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("home.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 创建数据库表
    app.run(debug=True, port=12345)
