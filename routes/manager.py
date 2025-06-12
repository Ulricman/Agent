from flask import Blueprint, render_template

manager_bp = Blueprint("manager", __name__)


@manager_bp.route("/user-status")
def user_status():
    return render_template("manager/user_status.html", title="用户状态")


@manager_bp.route("/tasks")
def tasks():
    return render_template("manager/tasks.html", title="待审批任务")


@manager_bp.route("/hotproblems")
def hot_problems():
    return render_template("manager/hotProblems.html", title="高频问题")


@manager_bp.route("/update")
def update():
    return render_template("manager/update.html", title="政策更新")


@manager_bp.route("/approvals")
def approvals():
    return render_template("manager/approvals.html", title="问答库审批")


@manager_bp.route("/")
def admin():
    return render_template("manager/index.html", title="知识管理岗")
