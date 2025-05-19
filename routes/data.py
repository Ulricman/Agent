from flask import Blueprint, render_template, request, redirect, url_for, flash

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

# 问答详情页面
@data_bp.route('/qa/detail/<int:qa_id>')
def qa_detail(qa_id):
    # 在实际应用中，应该从数据库查询该ID的问答
    # 这里使用模拟数据查找对应的问答
    qa_item = None
    for item in qa_data[1:]:  # 跳过标题行
        if item[0] == qa_id:
            qa_item = item
            break
    
    if qa_item:
        return render_template("qa_detail.html", qa=qa_item, headers=qa_data[0])
    else:
        return render_template("error.html", message="未找到该问答信息")
    

# 编辑问答
@data_bp.route('/qa/edit/<int:qa_id>')
def qa_edit(qa_id):
    # 查找对应的问答
    qa_item = None
    for item in qa_data[1:]:
        if item[0] == qa_id:
            qa_item = item
            break
    
    if qa_item:
        return render_template("qa_edit.html", qa=qa_item)
    else:
        return render_template("error.html", message="未找到该问答信息")

# 更新问答
@data_bp.route('/qa/update/<int:qa_id>', methods=['POST'])
def qa_update(qa_id):
    question = request.form.get('question')
    answer = request.form.get('answer')
    category = request.form.get('category')
    
    # 查找并更新对应的问答
    for item in qa_data[1:]:
        if item[0] == qa_id:
            item[1] = question
            item[2] = answer
            item[3] = category
            break
    
    # 实际应用中应该更新数据库
    # flash("问答更新成功", "success")
    return redirect(url_for('data.qa_detail', qa_id=qa_id))

# 添加新问答页面
@data_bp.route('/qa/add', methods=['GET', 'POST'])
def qa_add():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        category = request.form.get('category')
        
        # 生成新ID (实际应用中应由数据库生成)
        new_id = max([item[0] for item in qa_data[1:]]) + 1
        
        # 添加新问答
        qa_data.append([new_id, question, answer, category])
        
        # 实际应用中应该更新数据库
        # flash("问答添加成功", "success")
        return redirect(url_for('data.qa'))
    
    return render_template("qa_add.html")