from flask import Blueprint, render_template

data_bp = Blueprint('data', __name__)

# 模拟数据
policies_data = [
    ["政策编号", "政策名称", "发布日期", "备注"],
    [1, "增值税政策", "2025-01-01", "相关说明"],
    [2, "企业所得税政策", "2025-02-01", "相关说明"]
]

qa_data = [
    ["问题编号", "问题内容", "回答内容", "分类"],
    [1, "如何缴纳增值税？", "请参考政策库", "税务"],
    [2, "企业所得税计算公式？", "请参考企业所得税政策", "税务"]
]

terms_data = [
    ["词条编号", "词条名称", "释义"],
    [1, "增值税", "一种税收形式"],
    [2, "企业所得税", "企业经营所得需缴纳的税"]
]

# 税务政策库
@data_bp.route('/policies')
def policies():
    return render_template("table.html", title="税务政策库", headers=policies_data[0], data=policies_data[1:], add_new_url="/data/policies/add")

# 问答库
@data_bp.route('/qa')
def qa():
    return render_template("table.html", title="问答库", headers=qa_data[0], data=qa_data[1:], add_new_url="/data/qa/add")

# 词库
@data_bp.route('/terms')
def terms():
    return render_template("table.html", title="词库", headers=terms_data[0], data=terms_data[1:], add_new_url="/data/terms/add")

# 权限管理
#@data_bp.route('/permission')
#def terms():
    #return render_template("table.html", title="权限管理", headers=terms_data[0], data=terms_data[1:], add_new_url="/data/permission/add")