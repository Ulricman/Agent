from flask import Blueprint, render_template, request, redirect, session, send_file

auth_bp = Blueprint("auth", __name__)

# 模拟用户数据库
users = {
    "admin_user": {"password": "admin_pass", "role": "admin"},
    "manager_user": {"password": "manager_pass", "role": "manager"},
    "service_user": {"password": "service_pass", "role": "service"},
}


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]
            if user["role"] == "admin":
                return redirect("/admin")
            elif user["role"] == "manager":
                return redirect("/manager")
            elif user["role"] == "service":
                return redirect("/service")
        return "Invalid credentials", 401
    # return render_template('login.html')
    return send_file("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/auth/login")
