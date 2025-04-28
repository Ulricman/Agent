from flask import Flask, redirect, url_for
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.manager import manager_bp
from routes.service import service_bp
from routes.data import data_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(manager_bp, url_prefix="/manager")
app.register_blueprint(service_bp, url_prefix="/service")
app.register_blueprint(data_bp, url_prefix="/data")


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    app.run(debug=True, port=12345)
