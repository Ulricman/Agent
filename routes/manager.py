from flask import Blueprint, render_template

manager_bp = Blueprint("manager", __name__)


@manager_bp.route("/user-status")
def user_status():
    return render_template("user_status.html", title="用户状态")


@manager_bp.route("/tasks")
def tasks():
    return render_template("tasks.html", title="待审批任务")


@manager_bp.route("/hotproblems")
def hotProblems():
    return render_template("hotProblems.html", title="高频问题")


@manager_bp.route("/update")
def update():
    return render_template("update.html", title="政策更新")


@manager_bp.route("/")
def admin():
    return render_template("index_manager.html", title="知识管理岗")
