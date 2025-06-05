import os
import random
from datetime import datetime, timedelta
from typing import Dict, List

class PolicyHTMLGenerator:
    def __init__(self):
        self.announcements_dir = "data/announcements"
        os.makedirs(self.announcements_dir, exist_ok=True)
        
        # 政策更新模板
        self.policy_templates = {
            "policy_change": {
                "titles": [
                    "关于调整增值税征收政策的通知",
                    "企业所得税政策调整公告",
                    "个人所得税计算方法更新通知"
                ],
                "contents": [
                    "根据国家税务总局最新规定，现对相关税收政策进行调整。自本通知发布之日起，原有政策条款进行相应修订。",
                    "为进一步完善税收制度，规范税收征管，特对相关政策进行调整和完善。",
                    "结合当前经济发展情况，对税收政策进行适应性调整，确保税收政策的科学性和有效性。"
                ]
            },
            "policy_abolish": {
                "titles": [
                    "关于废除部分增值税优惠政策的公告",
                    "企业所得税减免政策废除通知",
                    "个人所得税专项扣除政策调整公告"
                ],
                "contents": [
                    "经研究决定，现将部分已不适应当前经济发展需要的税收优惠政策予以废除。",
                    "为统一税收政策执行标准，决定废除以下过时的税收优惠条款。",
                    "根据最新税法修订要求，原有部分税收优惠政策将予以废除，具体条款如下。"
                ]
            },
            "new_category_policy": {
                "titles": [
                    "数字税征收管理办法",
                    "环境保护税实施细则",
                    "碳排放税收政策指导意见"
                ],
                "contents": [
                    "为适应数字经济发展需要，建立健全数字税收制度，特制定本办法。",
                    "为加强环境保护，促进绿色发展，现制定环境保护税收政策。",
                    "结合碳达峰碳中和目标，建立碳排放税收调节机制，促进低碳发展。"
                ]
            },
            "penalty_update": {
                "titles": [
                    "税务违法行为处罚标准调整公告",
                    "税收征管法律责任更新通知",
                    "税务行政处罚裁量权细化规定"
                ],
                "contents": [
                    "为加强税收征管，规范执法行为，现对税务违法行为处罚标准进行调整。",
                    "根据最新法律法规，对税收征管中的法律责任进行明确和细化。",
                    "为保证执法公正，统一处罚标准，特制定本细化规定。"
                ]
            },
            "preferential_policy": {
                "titles": [
                    "小微企业税收优惠政策延续公告",
                    "高新技术企业所得税减免办法",
                    "研发费用加计扣除新规定"
                ],
                "contents": [
                    "为支持小微企业发展，减轻企业税收负担，现将相关优惠政策予以延续。",
                    "为鼓励科技创新，促进高新技术产业发展，特制定本减免办法。",
                    "为激励企业加大研发投入，完善研发费用税前扣除政策。"
                ]
            }
        }

    async def generate_policy_html_files(self) -> List[str]:
        """生成多个政策HTML文件"""
        generated_files = []
        
        # 为每种政策类型生成1-2个文件
        for policy_type, templates in self.policy_templates.items():
            num_files = random.randint(1, 2)
            for i in range(num_files):
                filename = await self._generate_single_policy_file(policy_type, templates, i)
                if filename:
                    generated_files.append(filename)
        
        return generated_files

    async def _generate_single_policy_file(self, policy_type: str, templates: Dict, index: int) -> str:
        """生成单个政策HTML文件"""
        try:
            title = random.choice(templates["titles"])
            content = random.choice(templates["contents"])
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{policy_type}_{timestamp}_{index}.html"
            filepath = os.path.join(self.announcements_dir, filename)
            
            # 生成HTML内容
            html_content = self._create_html_content(title, content, policy_type)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return filename
            
        except Exception as e:
            print(f"Error generating policy file: {e}")
            return None

    def _create_html_content(self, title: str, content: str, policy_type: str) -> str:
        """创建HTML内容"""
        # 根据政策类型选择样式
        policy_colors = {
            "policy_change": "#17a2b8",
            "policy_abolish": "#dc3545", 
            "new_category_policy": "#28a745",
            "penalty_update": "#ffc107",
            "preferential_policy": "#6f42c1"
        }
        
        color = policy_colors.get(policy_type, "#007bff")
        
        # 生成公告编号和日期
        announcement_id = f"{policy_type.upper()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        effective_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        publish_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background-color: #f8f9fa;
        }}
        
        .announcement {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid {color};
        }}
        
        .title {{
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .category {{
            display: inline-block;
            background: {color};
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        
        .content {{
            font-size: 1.1em;
            color: #444;
            margin: 20px 0;
            text-align: justify;
        }}
        
        .meta {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
        }}
        
        .meta span {{
            margin-right: 20px;
        }}
        
        .highlight {{
            background: {color}22;
            padding: 15px;
            border-left: 4px solid {color};
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #888;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="announcement">
        <div class="header">
            <div class="title">{title}</div>
            <div class="category">{self._get_policy_category(policy_type)}</div>
        </div>
        
        <div class="content">
            <p>{content}</p>
            
            <div class="highlight">
                <strong>重要提醒：</strong>{self._get_policy_reminder(policy_type)}
            </div>
            
            {self._get_policy_details(policy_type)}
        </div>
        
        <div class="meta">
            <span><strong>公告编号:</strong> {announcement_id}</span>
            <span><strong>生效日期:</strong> {effective_date}</span>
            <span><strong>发布时间:</strong> {publish_time}</span>
        </div>
        
        <div class="footer">
            <p>本公告由税务知识管理系统自动生成，仅供演示使用</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_template

    def _get_policy_category(self, policy_type: str) -> str:
        """获取政策分类显示名称"""
        categories = {
            "policy_change": "政策变更",
            "policy_abolish": "政策废除",
            "new_category_policy": "新税种政策",
            "penalty_update": "处罚标准更新",
            "preferential_policy": "优惠政策"
        }
        return categories.get(policy_type, "政策更新")

    def _get_policy_reminder(self, policy_type: str) -> str:
        """获取政策提醒内容"""
        reminders = {
            "policy_change": "请相关纳税人及时了解政策变更内容，确保合规申报。",
            "policy_abolish": "已废除的政策条款立即停止执行，请及时调整相关业务流程。",
            "new_category_policy": "新税种政策需要深入学习理解，建议咨询专业税务人员。",
            "penalty_update": "新的处罚标准已生效，请严格遵守相关规定避免违法风险。",
            "preferential_policy": "符合条件的纳税人可享受优惠政策，请及时申请办理。"
        }
        return reminders.get(policy_type, "请关注政策更新内容。")

    def _get_policy_details(self, policy_type: str) -> str:
        """获取政策详细内容"""
        details = {
            "policy_change": """
            <h3>主要变更内容：</h3>
            <ul>
                <li>税率结构调整：部分税率档次进行优化</li>
                <li>计税方法完善：明确特殊情况下的计税规则</li>
                <li>申报流程简化：减少不必要的申报环节</li>
                <li>执行时间明确：新政策的具体实施时间安排</li>
            </ul>
            """,
            "policy_abolish": """
            <h3>废除的政策条款：</h3>
            <ul>
                <li>原第三章第二节相关优惠条款</li>
                <li>临时性减免政策措施</li>
                <li>特定行业的过渡性规定</li>
                <li>已过期的试点政策条款</li>
            </ul>
            <p><strong>替代措施：</strong>请按照最新发布的统一政策执行。</p>
            """,
            "new_category_policy": """
            <h3>新税种要点：</h3>
            <ul>
                <li>征收对象：明确新税种的适用范围和对象</li>
                <li>计税依据：确定计税的基础和标准</li>
                <li>税率设置：采用差别化税率结构</li>
                <li>申报要求：建立专门的申报系统和流程</li>
            </ul>
            """,
            "penalty_update": """
            <h3>处罚标准调整：</h3>
            <ul>
                <li>轻微违法行为：降低处罚力度，注重教育引导</li>
                <li>严重违法行为：加大处罚力度，形成有效震慑</li>
                <li>首次违法：给予改正机会，减轻处罚</li>
                <li>重复违法：从重处罚，强化监管效果</li>
            </ul>
            """,
            "preferential_policy": """
            <h3>优惠政策内容：</h3>
            <ul>
                <li>减免税额：符合条件的最高可减免50%</li>
                <li>适用期限：优惠政策有效期为3年</li>
                <li>申请条件：需满足相关资质和经营要求</li>
                <li>办理流程：可通过网上办税服务厅申请</li>
            </ul>
            """
        }
        return details.get(policy_type, "<p>具体政策内容请关注后续详细通知。</p>")

    async def create_default_policy_files(self) -> Dict:
        """创建默认的政策文件集合"""
        try:
            generated_files = await self.generate_policy_html_files()
            
            return {
                "success": True,
                "files_created": len(generated_files),
                "filenames": generated_files,
                "message": f"成功创建 {len(generated_files)} 个政策HTML文件"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "创建政策文件失败"
            } 