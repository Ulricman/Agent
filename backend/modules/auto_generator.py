import os
import json
import uuid
import random
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
from .crawler import AnnouncementCrawler
from .knowledge_base import KnowledgeBase
from .qa_system import QASystem

class AutoGenerator:
    def __init__(self):
        self.crawler = AnnouncementCrawler()
        self.knowledge_base = KnowledgeBase()
        self.qa_system = QASystem()
        self.log_file = "data/auto_generator_log.json"
        
        # 税务领域的知识模板（扩展版）
        self.knowledge_templates = {
            "policy_change": {
                "categories": ["增值税", "企业所得税", "个人所得税", "消费税", "印花税"],
                "keywords_templates": [
                    ["政策变更", "税率调整", "计算方法"],
                    ["征收范围", "优惠政策", "减免条件"],
                    ["申报时间", "缴税期限", "办理流程"]
                ]
            },
            "new_regulation": {
                "categories": ["税务登记", "发票管理", "税务稽查", "行政处罚"],
                "keywords_templates": [
                    ["新规定", "管理办法", "实施细则"],
                    ["违法行为", "处罚标准", "法律责任"],
                    ["办理条件", "申请材料", "审批流程"]
                ]
            },
            "rate_adjustment": {
                "categories": ["增值税", "企业所得税", "个人所得税"],
                "keywords_templates": [
                    ["税率", "计算公式", "适用范围"],
                    ["征收标准", "减免政策", "优惠条件"],
                    ["执行时间", "过渡期", "新旧对比"]
                ]
            },
            "policy_abolish": {
                "categories": ["增值税", "企业所得税", "个人所得税", "消费税", "税务登记"],
                "keywords_templates": [
                    ["政策废除", "失效时间", "替代措施"],
                    ["过渡期安排", "历史文件", "存档管理"],
                    ["影响评估", "后续处理", "注意事项"]
                ]
            },
            "new_category_policy": {
                "categories": ["数字税", "环境税", "碳税", "数据税", "平台税"],
                "keywords_templates": [
                    ["新兴税种", "征收对象", "计税依据"],
                    ["税率标准", "申报方式", "管理办法"],
                    ["适用范围", "实施时间", "操作指南"]
                ]
            },
            "penalty_update": {
                "categories": ["税务处罚", "行政处罚", "法律责任"],
                "keywords_templates": [
                    ["处罚标准", "违法行为", "处罚程序"],
                    ["罚款金额", "责任认定", "申诉途径"],
                    ["处罚依据", "执行细则", "监督管理"]
                ]
            },
            "preferential_policy": {
                "categories": ["小微企业", "高新技术", "研发费用", "出口退税"],
                "keywords_templates": [
                    ["优惠政策", "减免条件", "申请程序"],
                    ["享受范围", "有效期限", "备案要求"],
                    ["计算方法", "申报流程", "审核标准"]
                ]
            },
            "international_tax": {
                "categories": ["国际税收", "跨境交易", "转让定价", "避税协定"],
                "keywords_templates": [
                    ["国际准则", "双边协定", "税收协调"],
                    ["跨境征税", "避免双重征税", "信息交换"],
                    ["合规要求", "申报义务", "风险防控"]
                ]
            }
        }
        
        # 问答模板（扩展版）
        self.qa_templates = {
            "policy_change": [
                "这项政策变更的主要内容是什么？",
                "新政策什么时候开始执行？",
                "这项变更对企业有什么影响？"
            ],
            "new_regulation": [
                "新规定的适用范围是什么？",
                "违反新规定会面临什么处罚？",
                "如何确保符合新规定要求？"
            ],
            "rate_adjustment": [
                "新税率是多少？",
                "税率调整从什么时候开始？",
                "哪些企业会受到影响？"
            ],
            "policy_abolish": [
                "被废除的政策有哪些？",
                "政策废除后应如何处理相关业务？",
                "是否有替代政策可以参考？"
            ],
            "new_category_policy": [
                "这个新税种的征收对象是什么？",
                "如何计算这个新税种的应纳税额？",
                "新税种什么时候开始实施？"
            ],
            "penalty_update": [
                "新的处罚标准有哪些变化？",
                "如何避免触犯新的处罚规定？",
                "违法后如何进行申诉？"
            ],
            "preferential_policy": [
                "享受优惠政策需要满足什么条件？",
                "如何申请税收优惠？",
                "优惠政策的有效期是多长？"
            ],
            "international_tax": [
                "跨境业务需要注意哪些税收问题？",
                "如何避免国际双重征税？",
                "国际税收协定的主要内容是什么？"
            ]
        }
        
        # 固定流程更新类型（这些会实际更新数据库）
        self.fixed_update_types = [
            "policy_change", "new_regulation", "rate_adjustment", 
            "policy_abolish", "new_category_policy", "penalty_update",
            "preferential_policy"
        ]
        
        # 非固定流程更新类型（仅显示提示）
        self.general_update_types = [
            "international_tax", "emergency_notice", "temporary_measure",
            "consultation_draft", "interpretation_clarification"
        ]

    async def auto_generate_from_crawler(self) -> Dict:
        """基于爬虫结果自动生成知识库和问答库内容"""
        try:
            # 获取爬虫最新结果（不重新检查，使用缓存的结果）
            crawler_result = await self._get_cached_crawler_results()
            
            if not crawler_result.get("has_updates", False):
                return {
                    "success": True,
                    "message": "没有发现更新，无需生成新内容",
                    "generated": {
                        "knowledge_items": 0,
                        "qa_items": 0
                    }
                }
            
            updates = crawler_result.get("updates", [])
            generated_knowledge = []
            generated_qa = []
            general_updates = []
            
            # 获取现有的知识库和问答库内容用于去重检查
            existing_knowledge = await self.knowledge_base.get_all_items()
            existing_qa = await self.qa_system.get_all_items()
            
            # 处理每个更新
            for update in updates:
                update_type = update.get("update_type")
                
                # 如果没有update_type，从文件名推断类型
                if not update_type and "filename" in update:
                    filename = update["filename"]
                    if "policy_change" in filename:
                        update_type = "policy_change"
                    elif "policy_abolish" in filename:
                        update_type = "policy_abolish"
                    elif "new_category_policy" in filename:
                        update_type = "new_category_policy"
                    elif "penalty_update" in filename:
                        update_type = "penalty_update"
                    elif "preferential_policy" in filename:
                        update_type = "preferential_policy"
                    elif "rate_adjustment" in filename:
                        update_type = "rate_adjustment"
                    elif "new_regulation" in filename:
                        update_type = "new_regulation"
                    else:
                        update_type = "policy_change"  # 默认类型
                    
                    # 添加推断的类型到更新对象
                    update["update_type"] = update_type
                    update["description"] = f"检测到{update_type}相关文件更新"
                    update["priority"] = "medium"
                    update["category"] = "税务政策"
                
                # 生成更新的唯一标识
                update_hash = self._generate_update_hash(update)
                
                # 检查是否已经基于此更新生成过内容
                if self._is_already_generated(update_hash, existing_knowledge, existing_qa):
                    continue  # 跳过已处理的更新
                
                # 区分固定流程和非固定流程
                if update_type in self.fixed_update_types:
                    # 固定流程：实际生成内容
                    knowledge_items = await self._generate_knowledge_from_update(update, update_hash)
                    # 去重检查
                    knowledge_items = self._deduplicate_knowledge(knowledge_items, existing_knowledge)
                    generated_knowledge.extend(knowledge_items)
                    
                    qa_items = await self._generate_qa_from_update(update, update_hash)
                    # 去重检查
                    qa_items = self._deduplicate_qa(qa_items, existing_qa)
                    generated_qa.extend(qa_items)
                else:
                    # 非固定流程：仅记录提示信息
                    general_updates.append(update)
            
            # 添加到知识库
            knowledge_added = 0
            for item in generated_knowledge:
                result = await self.knowledge_base.add_item(item)
                if result.get("success", False):
                    knowledge_added += 1
            
            # 添加到问答库
            qa_added = 0
            for item in generated_qa:
                result = await self.qa_system.add_item(item)
                if result.get("success", False):
                    qa_added += 1
            
            # 记录操作
            await self._log_operation("auto_generate", {
                "crawler_updates": len(updates),
                "knowledge_generated": len(generated_knowledge),
                "knowledge_added": knowledge_added,
                "qa_generated": len(generated_qa),
                "qa_added": qa_added
            })
            
            return {
                "success": True,
                "message": f"自动生成完成：知识库新增{knowledge_added}条，问答库新增{qa_added}条",
                "generated": {
                    "knowledge_items": knowledge_added,
                    "qa_items": qa_added
                },
                "crawler_updates": len(updates),
                "fixed_updates": len(updates) - len(general_updates),
                "general_updates": general_updates,
                "deduplication_info": {
                    "knowledge_generated": len(generated_knowledge),
                    "knowledge_added": knowledge_added,
                    "knowledge_duplicates_removed": len(generated_knowledge) - knowledge_added,
                    "qa_generated": len(generated_qa),
                    "qa_added": qa_added,
                    "qa_duplicates_removed": len(generated_qa) - qa_added
                }
            }
            
        except Exception as e:
            await self._log_operation("auto_generate_error", {"error": str(e)})
            return {
                "success": False,
                "error": f"自动生成失败: {str(e)}"
            }

    async def _generate_knowledge_from_update(self, update: Dict, update_hash: str) -> List[Dict]:
        """从更新信息生成知识库条目"""
        knowledge_items = []
        
        update_type = update.get("update_type", "policy_change")
        template = self.knowledge_templates.get(update_type, self.knowledge_templates["policy_change"])
        
        # 生成1-2个知识条目
        num_items = random.randint(1, 2)
        for i in range(num_items):
            category = random.choice(template["categories"])
            keywords = random.choice(template["keywords_templates"])
            
            # 根据更新类型生成内容
            content = self._generate_knowledge_content(update, category, update_type)
            title = self._generate_knowledge_title(update, category, update_type)
            
            knowledge_item = {
                "id": f"kb_auto_{str(uuid.uuid4())[:8]}",
                "title": title,
                "content": content,
                "category": category,
                "keywords": keywords + [category],
                "effective_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "active",
                "source": f"自动生成-{update.get('timestamp', '')}",
                "related_policies": [f"{category.upper()}-AUTO-{datetime.now().strftime('%Y%m%d')}"],
                "priority": update.get("priority", "medium"),
                "auto_generated": True,
                "source_update": update,
                "update_hash": update_hash  # 添加更新哈希
            }
            
            knowledge_items.append(knowledge_item)
        
        return knowledge_items

    async def _generate_qa_from_update(self, update: Dict, update_hash: str) -> List[Dict]:
        """从更新信息生成问答条目"""
        qa_items = []
        
        update_type = update.get("update_type", "policy_change")
        questions = self.qa_templates.get(update_type, self.qa_templates["policy_change"])
        
        # 生成1-3个问答条目
        num_items = random.randint(1, 3)
        for i in range(num_items):
            question = random.choice(questions)
            category = random.choice(["增值税", "企业所得税", "个人所得税", "税务管理"])
            
            # 根据更新信息生成具体问题和答案
            specific_question = self._generate_specific_question(update, category, question)
            answer = self._generate_answer(update, category)
            
            qa_item = {
                "id": f"qa_auto_{str(uuid.uuid4())[:8]}",
                "question": specific_question,
                "answer": answer,
                "category": category,
                "keywords": [category, update_type, "政策更新"],
                "confidence": round(random.uniform(0.8, 0.95), 2),
                "source": f"自动生成-{update.get('timestamp', '')}",
                "related_questions": [],
                "priority": update.get("priority", "medium"),
                "status": "active",
                "auto_generated": True,
                "source_update": update,
                "update_hash": update_hash  # 添加更新哈希
            }
            
            qa_items.append(qa_item)
        
        return qa_items

    def _generate_knowledge_content(self, update: Dict, category: str, update_type: str) -> str:
        """生成知识库内容"""
        base_content = {
            "policy_change": f"根据最新政策变更，{category}相关规定已作出调整。主要变化包括征收标准、计税方法等方面的更新。企业和个人纳税人应及时了解新政策内容，确保合规申报和缴税。",
            "new_regulation": f"新发布的{category}管理规定，对相关业务流程和要求进行了规范。纳税人应按照新规定的要求，完善相关管理制度，确保各项业务活动符合法规要求。",
            "rate_adjustment": f"{category}税率已进行调整，新税率标准即将生效。相关企业应及时调整会计核算方法，重新计算应纳税额，确保准确申报。",
            "policy_abolish": f"根据最新公告，{category}相关政策已正式废除。纳税人应停止执行已废除的政策条款，按照新的规定处理相关税务事项。已按旧政策处理的事项需要进行相应调整。",
            "new_category_policy": f"全新的{category}政策正式发布，这是一个全新的税收领域。纳税人应深入了解新税种的征收对象、计税方法和申报要求，确保及时合规。",
            "penalty_update": f"{category}处罚标准已更新，对违法违规行为的处罚力度和标准进行了调整。纳税人应严格遵守相关规定，避免因违规而面临处罚。",
            "preferential_policy": f"新的{category}优惠政策已发布，符合条件的纳税人可享受相应的税收减免。建议企业及时了解优惠条件和申请程序，充分利用政策红利。"
        }
        
        content = base_content.get(update_type, base_content["policy_change"])
        description = update.get("description", "")
        
        if description:
            content += f"\n\n具体变更说明：{description}"
            
        # 根据更新类型添加特定的注意事项
        if update_type == "policy_abolish":
            content += f"\n\n重要提醒：请务必在{datetime.now().strftime('%Y年%m月%d日')}之前完成相关业务调整，避免因执行已废除政策而产生不必要的风险。"
        elif update_type == "new_category_policy":
            content += f"\n\n实施时间：{datetime.now().strftime('%Y年%m月%d日')}起正式实施。建议提前做好相关准备工作。"
        elif update_type == "penalty_update":
            content += f"\n\n执行时间：自{datetime.now().strftime('%Y年%m月%d日')}起执行新的处罚标准。"
        
        return content

    async def _get_cached_crawler_results(self) -> Dict:
        """获取缓存的爬虫结果，如果没有则执行新的检查"""
        try:
            # 尝试读取最近的爬虫结果
            cache_file = "data/crawler_cache.json"
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                # 检查缓存是否在5分钟内
                try:
                    cache_time_str = cached_data.get("check_time", "")
                    if cache_time_str:
                        cache_time = datetime.fromisoformat(cache_time_str.replace('Z', '+00:00'))
                        if (datetime.now() - cache_time).total_seconds() < 300:  # 5分钟内
                            return cached_data
                except (ValueError, TypeError):
                    # 如果时间解析失败，忽略缓存
                    pass
            
            # 如果没有有效缓存，执行新的检查
            result = await self.crawler.check_for_updates()
            
            # 缓存结果
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            return result
            
        except Exception as e:
            # 如果出错，直接调用爬虫
            return await self.crawler.check_for_updates()

    def _generate_knowledge_title(self, update: Dict, category: str, update_type: str) -> str:
        """生成知识库标题"""
        title_templates = {
            "policy_change": f"{category}政策变更通知",
            "new_regulation": f"{category}新规定发布",
            "rate_adjustment": f"{category}税率调整公告",
            "policy_abolish": f"{category}政策废除公告",
            "new_category_policy": f"{category}新税种实施办法",
            "penalty_update": f"{category}处罚标准更新",
            "preferential_policy": f"{category}优惠政策发布"
        }
        
        base_title = title_templates.get(update_type, f"{category}政策更新")
        timestamp = datetime.now().strftime("%Y年%m月")
        
        return f"{base_title}（{timestamp}）"

    def _generate_specific_question(self, update: Dict, category: str, base_question: str) -> str:
        """生成具体的问题"""
        # 将通用问题转换为具体的分类问题
        specific_questions = {
            "这项政策变更的主要内容是什么？": f"{category}政策变更的主要内容是什么？",
            "新政策什么时候开始执行？": f"新的{category}政策什么时候开始执行？",
            "这项变更对企业有什么影响？": f"{category}政策变更对企业有什么影响？",
            "新规定的适用范围是什么？": f"{category}新规定的适用范围是什么？",
            "违反新规定会面临什么处罚？": f"违反{category}新规定会面临什么处罚？",
            "如何确保符合新规定要求？": f"如何确保符合{category}新规定要求？",
            "新税率是多少？": f"{category}的新税率是多少？",
            "税率调整从什么时候开始？": f"{category}税率调整从什么时候开始？",
            "哪些企业会受到影响？": f"{category}税率调整会对哪些企业产生影响？"
        }
        
        return specific_questions.get(base_question, f"{category}相关问题：{base_question}")

    def _generate_answer(self, update: Dict, category: str) -> str:
        """生成答案"""
        answer_templates = {
            "增值税": "根据增值税相关规定，纳税人应按照新的政策要求进行申报和缴税。具体包括税率调整、征收范围变化等内容。建议企业及时咨询税务专业人员，确保合规操作。",
            "企业所得税": "企业所得税政策更新后，企业应重新评估税务风险，调整税务筹划方案。新政策可能涉及税率变化、优惠政策调整等，企业财务人员需要深入学习相关规定。",
            "个人所得税": "个人所得税政策变化可能影响个人纳税负担，纳税人应了解新的计税方法、扣除标准等。建议关注税务部门的官方解读和操作指南。",
            "税务管理": "税务管理制度的更新要求纳税人完善内部管理流程，加强税务合规性管理。企业应建立健全税务管理制度，防范税务风险。"
        }
        
        base_answer = answer_templates.get(category, "根据最新税务政策，相关规定已发生变化，请及时关注官方通知。")
        description = update.get("description", "")
        
        if description:
            base_answer += f"\n\n更新详情：{description}"
        
        return base_answer

    async def update_default_data(self, knowledge_items: List[Dict] = None, qa_items: List[Dict] = None):
        """更新默认的知识库和问答库数据（用于系统重置）"""
        try:
            if knowledge_items:
                self.knowledge_base.sample_items = knowledge_items
            
            if qa_items:
                self.qa_system.sample_qa_pairs = qa_items
            
            await self._log_operation("update_default_data", {
                "knowledge_count": len(knowledge_items) if knowledge_items else 0,
                "qa_count": len(qa_items) if qa_items else 0
            })
            
            return {"success": True, "message": "默认数据已更新"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def reset_auto_generator(self):
        """重置自动生成器的日志和统计数据"""
        try:
            # 清空日志文件
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            
            # 重新初始化知识库和问答系统
            await self.knowledge_base.initialize()
            await self.qa_system.initialize()
            
            await self._log_operation("reset_auto_generator", {
                "message": "自动生成器已重置到默认状态"
            })
            
            return {"success": True, "message": "自动生成器已重置"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_stats(self) -> Dict:
        """获取自动生成统计信息"""
        try:
            # 读取日志
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            # 统计自动生成的数据
            total_generated = 0
            total_knowledge = 0
            total_qa = 0
            
            for log in logs:
                if log.get("operation") == "auto_generate":
                    details = log.get("details", {})
                    total_knowledge += details.get("knowledge_added", 0)
                    total_qa += details.get("qa_added", 0)
                    total_generated += 1
            
            return {
                "total_generations": total_generated,
                "total_knowledge_generated": total_knowledge,
                "total_qa_generated": total_qa,
                "last_generation": logs[-1].get("timestamp") if logs else None
            }
            
        except Exception as e:
            return {"error": str(e)}

    async def _log_operation(self, operation: str, details: Dict):
        """记录操作到日志文件"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "details": details
            }
            
            # 加载现有日志
            logs = []
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
            
            # 添加新日志
            logs.append(log_entry)
            
            # 保持最近1000条记录
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            # 保存日志
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error logging operation: {e}")
    
    def _generate_update_hash(self, update: Dict) -> str:
        """生成更新的唯一哈希标识"""
        # 创建用于哈希的关键信息字符串
        hash_content = {
            "type": update.get("update_type", ""),
            "filename": update.get("filename", ""),
            "timestamp": update.get("timestamp", ""),
            "description": update.get("description", ""),
            "category": update.get("category", "")
        }
        
        # 生成MD5哈希
        hash_string = json.dumps(hash_content, sort_keys=True)
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def _is_already_generated(self, update_hash: str, existing_knowledge: List[Dict], existing_qa: List[Dict]) -> bool:
        """检查是否已经基于相同的更新生成过内容"""
        # 检查知识库中是否存在相同哈希的条目
        for item in existing_knowledge:
            if item.get("update_hash") == update_hash:
                return True
        
        # 检查问答库中是否存在相同哈希的条目
        for item in existing_qa:
            if item.get("update_hash") == update_hash:
                return True
        
        return False
    
    def _deduplicate_knowledge(self, new_items: List[Dict], existing_items: List[Dict]) -> List[Dict]:
        """去除重复的知识库条目"""
        deduplicated = []
        
        for new_item in new_items:
            is_duplicate = False
            
            # 检查标题和内容相似度
            for existing_item in existing_items:
                if self._is_similar_content(new_item.get("title", ""), existing_item.get("title", ""), threshold=0.8):
                    is_duplicate = True
                    break
                if self._is_similar_content(new_item.get("content", ""), existing_item.get("content", ""), threshold=0.7):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                deduplicated.append(new_item)
        
        return deduplicated
    
    def _deduplicate_qa(self, new_items: List[Dict], existing_items: List[Dict]) -> List[Dict]:
        """去除重复的问答条目"""
        deduplicated = []
        
        for new_item in new_items:
            is_duplicate = False
            
            # 检查问题和答案相似度
            for existing_item in existing_items:
                if self._is_similar_content(new_item.get("question", ""), existing_item.get("question", ""), threshold=0.8):
                    is_duplicate = True
                    break
                if self._is_similar_content(new_item.get("answer", ""), existing_item.get("answer", ""), threshold=0.7):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                deduplicated.append(new_item)
        
        return deduplicated
    
    def _is_similar_content(self, text1: str, text2: str, threshold: float = 0.7) -> bool:
        """检查两个文本的相似度"""
        if not text1 or not text2:
            return False
        
        # 简单的基于字符的相似度检查
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()
        
        if text1 == text2:
            return True
        
        # 计算较长文本包含较短文本的比例
        shorter = text1 if len(text1) <= len(text2) else text2
        longer = text2 if len(text1) <= len(text2) else text1
        
        if len(shorter) == 0:
            return False
        
        # 如果较短文本在较长文本中的覆盖率超过阈值，认为相似
        common_chars = sum(1 for char in shorter if char in longer)
        similarity = common_chars / len(shorter)
        
        return similarity >= threshold 