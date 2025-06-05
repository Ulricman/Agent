import os
import json
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class QASystem:
    def __init__(self):
        self.data_file = "data/qa_database.json"
        self.backup_dir = "data/backups/qa"
        self.log_file = "data/qa_log.json"
        
        # Initialize directories
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Sample QA pairs
        self.sample_qa_pairs = [
            {
                "id": "qa_001",
                "question": "增值税一般纳税人的认定标准是什么？",
                "answer": "增值税一般纳税人的认定标准主要有：1）年应征增值税销售额超过500万元；2）年应税销售额未超过标准但会计核算健全，能够提供准确税务资料的纳税人也可申请认定。",
                "category": "增值税",
                "keywords": ["增值税", "一般纳税人", "认定标准"],
                "confidence": 0.95,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source": "增值税暂行条例",
                "related_questions": ["qa_002"],
                "priority": "high",
                "status": "active"
            },
            {
                "id": "qa_002",
                "question": "小规模纳税人和一般纳税人有什么区别？",
                "answer": "主要区别包括：1）认定标准不同：一般纳税人年销售额超过500万元，小规模纳税人不超过500万元；2）税率不同：一般纳税人适用13%、9%等税率，小规模纳税人征收率为3%；3）进项税抵扣：一般纳税人可以抵扣进项税，小规模纳税人不能抵扣。",
                "category": "增值税",
                "keywords": ["小规模纳税人", "一般纳税人", "区别", "税率"],
                "confidence": 0.92,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source": "增值税暂行条例",
                "related_questions": ["qa_001"],
                "priority": "high",
                "status": "active"
            },
            {
                "id": "qa_003",
                "question": "企业所得税的税率是多少？",
                "answer": "企业所得税税率为：1）一般企业：25%；2）符合条件的小型微利企业：20%；3）国家重点扶持的高新技术企业：15%。小型微利企业还可享受减半征收等优惠政策。",
                "category": "企业所得税",
                "keywords": ["企业所得税", "税率", "小微企业", "高新技术企业"],
                "confidence": 0.98,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source": "企业所得税法",
                "related_questions": [],
                "priority": "high",
                "status": "active"
            },
            {
                "id": "qa_004",
                "question": "个人所得税的起征点是多少？",
                "answer": "个人所得税起征点为每月5000元（年度6万元）。超过起征点的部分按照3%-45%的累进税率计算个人所得税。同时可以享受子女教育、继续教育、大病医疗、住房贷款利息、住房租金、赡养老人等专项附加扣除。",
                "category": "个人所得税",
                "keywords": ["个人所得税", "起征点", "累进税率", "专项附加扣除"],
                "confidence": 0.96,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source": "个人所得税法",
                "related_questions": [],
                "priority": "high",
                "status": "active"
            },
            {
                "id": "qa_005",
                "question": "如何办理税务登记？",
                "answer": "税务登记办理流程：1）准备材料：营业执照、组织机构代码证、法人身份证等；2）到主管税务机关申请；3）填写税务登记表；4）提交相关材料；5）税务机关审核；6）领取税务登记证。现在多数地区已实现多证合一，可通过网上办税服务厅办理。",
                "category": "税务登记",
                "keywords": ["税务登记", "办理流程", "材料", "网上办税"],
                "confidence": 0.89,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source": "税务登记管理办法",
                "related_questions": [],
                "priority": "medium",
                "status": "active"
            }
        ]
        
        # Simulated LLM response templates
        self.llm_templates = {
            "default": [
                "根据税务法规，{answer}",
                "按照相关政策规定，{answer}",
                "根据最新税务政策，{answer}",
                "依据税法条文，{answer}"
            ],
            "增值税": [
                "关于增值税问题，{answer}",
                "根据增值税暂行条例，{answer}",
                "增值税政策规定，{answer}"
            ],
            "企业所得税": [
                "企业所得税法规定，{answer}",
                "关于企业所得税，{answer}",
                "根据企业所得税相关政策，{answer}"
            ],
            "个人所得税": [
                "个人所得税法明确，{answer}",
                "关于个人所得税，{answer}",
                "根据个税政策，{answer}"
            ]
        }

    async def initialize(self):
        """Initialize QA system with sample data if empty"""
        if not os.path.exists(self.data_file):
            await self._save_data(self.sample_qa_pairs)
            await self._log_operation("initialize", {"items_count": len(self.sample_qa_pairs)})

    async def _load_data(self) -> List[Dict]:
        """Load QA data from file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both formats: direct list or wrapped in "qa_pairs" key
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "qa_pairs" in data:
                    return data["qa_pairs"]
                else:
                    return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    async def _save_data(self, data: List[Dict]):
        """Save QA data to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save QA database: {str(e)}")

    async def _log_operation(self, operation: str, details: Dict):
        """Log operations to log file"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "details": details
            }
            
            # Load existing logs
            logs = []
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
            
            # Add new log entry
            logs.append(log_entry)
            
            # Keep only last 1000 entries
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            # Save logs
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error logging operation: {e}")

    async def get_all_items(self) -> List[Dict]:
        """Get all QA items"""
        return await self._load_data()

    async def add_item(self, item: Dict) -> Dict:
        """Add new QA item"""
        try:
            items = await self._load_data()
            
            # Generate ID if not provided
            if 'id' not in item:
                item['id'] = f"qa_{str(uuid.uuid4())[:8]}"
            
            # Add timestamps
            item['created_at'] = datetime.now().isoformat()
            item['updated_at'] = datetime.now().isoformat()
            
            # Set default values
            item.setdefault('status', 'active')
            item.setdefault('priority', 'medium')
            item.setdefault('keywords', [])
            item.setdefault('related_questions', [])
            item.setdefault('confidence', 0.8)
            
            # Check for duplicate ID
            if any(existing['id'] == item['id'] for existing in items):
                return {"success": False, "error": "Item with this ID already exists"}
            
            items.append(item)
            await self._save_data(items)
            await self._log_operation("add_item", {"item_id": item['id'], "question": item.get('question', 'N/A')})
            
            return {"success": True, "item": item}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def update_item(self, item_id: str, updated_item: Dict) -> Dict:
        """Update existing QA item"""
        try:
            items = await self._load_data()
            
            # Find item to update
            item_index = None
            for i, item in enumerate(items):
                if item['id'] == item_id:
                    item_index = i
                    break
            
            if item_index is None:
                return {"success": False, "error": "Item not found"}
            
            # Preserve original creation time and ID
            updated_item['id'] = item_id
            updated_item['created_at'] = items[item_index].get('created_at', datetime.now().isoformat())
            updated_item['updated_at'] = datetime.now().isoformat()
            
            # Update item
            items[item_index] = updated_item
            await self._save_data(items)
            await self._log_operation("update_item", {"item_id": item_id, "question": updated_item.get('question', 'N/A')})
            
            return {"success": True, "item": updated_item}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def delete_item(self, item_id: str) -> Dict:
        """Delete QA item"""
        try:
            items = await self._load_data()
            
            # Find and remove item
            original_count = len(items)
            items = [item for item in items if item['id'] != item_id]
            
            if len(items) == original_count:
                return {"success": False, "error": "Item not found"}
            
            await self._save_data(items)
            await self._log_operation("delete_item", {"item_id": item_id})
            
            return {"success": True, "message": f"Item {item_id} deleted successfully"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def search(self, query: str) -> List[Dict]:
        """Search QA database"""
        try:
            items = await self._load_data()
            query = query.lower().strip()
            
            if not query:
                return items
            
            matching_items = []
            
            for item in items:
                # Search in question, answer, keywords, and category
                searchable_text = " ".join([
                    item.get('question', ''),
                    item.get('answer', ''),
                    item.get('category', ''),
                    " ".join(item.get('keywords', []))
                ]).lower()
                
                if query in searchable_text:
                    # Calculate relevance score
                    score = 0
                    if query in item.get('question', '').lower():
                        score += 10
                    if query in item.get('keywords', []):
                        score += 8
                    if query in item.get('category', '').lower():
                        score += 5
                    if query in item.get('answer', '').lower():
                        score += 3
                    
                    item_copy = item.copy()
                    item_copy['_relevance_score'] = score
                    matching_items.append(item_copy)
            
            # Sort by relevance score
            matching_items.sort(key=lambda x: x.get('_relevance_score', 0), reverse=True)
            
            await self._log_operation("search", {"query": query, "results_count": len(matching_items)})
            
            return matching_items
            
        except Exception as e:
            print(f"Search error: {e}")
            return []

    async def ask_question(self, question: str) -> Dict:
        """Ask a question and get simulated LLM response"""
        try:
            # First, search for existing answers
            existing_answers = await self.search(question)
            
            if existing_answers:
                # Use the best matching answer
                best_match = existing_answers[0]
                response = await self._generate_llm_response(best_match, question)
                await self._log_operation("ask_question", {
                    "question": question,
                    "matched_qa_id": best_match.get('id'),
                    "confidence": best_match.get('confidence', 0.5)
                })
                return response
            
            # If no existing answer found, generate a fallback response
            fallback_response = await self._generate_fallback_response(question)
            await self._log_operation("ask_question", {
                "question": question,
                "fallback_used": True,
                "confidence": 0.3
            })
            return fallback_response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "question": question
            }

    async def _generate_llm_response(self, qa_item: Dict, original_question: str) -> Dict:
        """Generate simulated LLM response based on existing QA item"""
        try:
            category = qa_item.get('category', 'default')
            answer = qa_item.get('answer', '')
            
            # Select appropriate template
            templates = self.llm_templates.get(category, self.llm_templates['default'])
            template = random.choice(templates)
            
            # Format the response
            formatted_answer = template.format(answer=answer)
            
            # Add some variation to simulate LLM behavior
            variations = [
                f"根据我的理解，{formatted_answer}",
                f"让我为您解答：{formatted_answer}",
                f"针对您的问题，{formatted_answer}",
                formatted_answer
            ]
            
            final_answer = random.choice(variations)
            
            return {
                "success": True,
                "question": original_question,
                "answer": final_answer,
                "confidence": qa_item.get('confidence', 0.8),
                "source_qa_id": qa_item.get('id'),
                "category": category,
                "response_type": "matched",
                "timestamp": datetime.now().isoformat(),
                "related_questions": qa_item.get('related_questions', [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "question": original_question
            }

    async def _generate_fallback_response(self, question: str) -> Dict:
        """Generate fallback response when no matching QA found"""
        try:
            # Detect question category based on keywords
            category = self._detect_category(question)
            
            fallback_answers = {
                "增值税": "关于增值税的问题，建议您咨询当地税务部门或查阅最新的增值税暂行条例。如需具体政策解读，请联系专业税务顾问。",
                "企业所得税": "关于企业所得税的问题，建议您参考企业所得税法相关条文，或咨询税务专业人士获取准确信息。",
                "个人所得税": "关于个人所得税的问题，建议您查阅个人所得税法或通过税务部门官方渠道获取权威信息。",
                "default": "很抱歉，我无法找到与您问题完全匹配的答案。建议您：1）咨询当地税务部门；2）查阅相关税法条文；3）寻求专业税务顾问帮助。"
            }
            
            answer = fallback_answers.get(category, fallback_answers["default"])
            
            return {
                "success": True,
                "question": question,
                "answer": answer,
                "confidence": 0.3,
                "category": category,
                "response_type": "fallback",
                "timestamp": datetime.now().isoformat(),
                "suggestion": "建议添加相关问答到知识库以改善回答质量"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "question": question
            }

    def _detect_category(self, question: str) -> str:
        """Detect question category based on keywords"""
        question_lower = question.lower()
        
        if any(keyword in question_lower for keyword in ["增值税", "vat", "进项税", "销项税"]):
            return "增值税"
        elif any(keyword in question_lower for keyword in ["企业所得税", "cit", "企业税"]):
            return "企业所得税"
        elif any(keyword in question_lower for keyword in ["个人所得税", "个税", "工资税"]):
            return "个人所得税"
        elif any(keyword in question_lower for keyword in ["消费税", "资源税", "环保税"]):
            return "其他税种"
        else:
            return "default"

    async def init_from_file(self, file_path: str) -> Dict:
        """Initialize QA system from JSON file"""
        try:
            if not os.path.exists(file_path):
                return {"success": False, "error": "File not found"}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                new_items = json.load(f)
            
            # Validate and process items
            processed_items = []
            for item in new_items:
                if not isinstance(item, dict):
                    continue
                
                # Ensure required fields
                if 'question' not in item or 'answer' not in item:
                    continue
                
                # Add missing fields
                if 'id' not in item:
                    item['id'] = f"qa_{str(uuid.uuid4())[:8]}"
                
                item.setdefault('created_at', datetime.now().isoformat())
                item.setdefault('updated_at', datetime.now().isoformat())
                item.setdefault('status', 'active')
                item.setdefault('priority', 'medium')
                item.setdefault('keywords', [])
                item.setdefault('category', 'general')
                item.setdefault('confidence', 0.8)
                
                processed_items.append(item)
            
            # Save processed items
            await self._save_data(processed_items)
            await self._log_operation("init_from_file", {
                "file_path": file_path,
                "items_loaded": len(processed_items)
            })
            
            return {
                "success": True,
                "message": f"Successfully loaded {len(processed_items)} QA pairs from {file_path}",
                "items_count": len(processed_items)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def export_all(self) -> Dict:
        """Export entire QA database"""
        try:
            items = await self._load_data()
            export_data = {
                "export_time": datetime.now().isoformat(),
                "items_count": len(items),
                "items": items
            }
            
            # Create export file
            export_filename = f"qa_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            export_path = os.path.join(self.backup_dir, export_filename)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            await self._log_operation("export_all", {"export_path": export_path, "items_count": len(items)})
            
            return {
                "success": True,
                "export_path": export_path,
                "items_count": len(items),
                "data": export_data
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def process_updates(self, updates: List[Dict]) -> Dict:
        """Process updates from crawler and generate new QA pairs"""
        try:
            processed_count = 0
            added_count = 0
            
            for update in updates:
                # Generate QA pairs from updates
                new_qa_pairs = await self._generate_qa_from_update(update)
                
                for qa_pair in new_qa_pairs:
                    result = await self.add_item(qa_pair)
                    if result.get('success'):
                        added_count += 1
                
                processed_count += 1
            
            await self._log_operation("process_updates", {
                "processed_count": processed_count,
                "added_count": added_count
            })
            
            return {
                "success": True,
                "processed_count": processed_count,
                "added_count": added_count
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _generate_qa_from_update(self, update: Dict) -> List[Dict]:
        """Generate QA pairs from update information"""
        try:
            qa_pairs = []
            
            update_type = update.get('update_type', 'unknown')
            description = update.get('description', '')
            category = update.get('category', 'general')
            
            if update_type == 'policy_change':
                qa_pairs.append({
                    "question": f"{category}政策有什么新变化？",
                    "answer": f"根据最新政策更新，{description}",
                    "category": category,
                    "keywords": [category, "政策变更", "最新"],
                    "confidence": 0.7,
                    "priority": update.get('priority', 'medium'),
                    "source": "系统自动生成",
                    "auto_generated": True
                })
            
            elif update_type == 'rate_adjustment':
                qa_pairs.append({
                    "question": f"{category}税率调整了吗？",
                    "answer": f"是的，{description}",
                    "category": category,
                    "keywords": [category, "税率", "调整"],
                    "confidence": 0.8,
                    "priority": update.get('priority', 'medium'),
                    "source": "系统自动生成",
                    "auto_generated": True
                })
            
            return qa_pairs
            
        except Exception as e:
            print(f"Error generating QA from update: {e}")
            return []

    async def get_stats(self) -> Dict:
        """Get QA system statistics"""
        try:
            items = await self._load_data()
            
            # Basic stats
            total_items = len(items)
            active_items = len([item for item in items if item.get('status') == 'active'])
            
            # Category breakdown
            categories = {}
            for item in items:
                category = item.get('category', 'unknown')
                categories[category] = categories.get(category, 0) + 1
            
            # Confidence distribution
            high_confidence = len([item for item in items if item.get('confidence', 0) >= 0.8])
            medium_confidence = len([item for item in items if 0.5 <= item.get('confidence', 0) < 0.8])
            low_confidence = len([item for item in items if item.get('confidence', 0) < 0.5])
            
            # Recent additions (last 7 days)
            recent_additions = 0
            cutoff_date = (datetime.now() - timedelta(days=7)).isoformat()
            for item in items:
                if item.get('created_at', '') > cutoff_date:
                    recent_additions += 1
            
            return {
                "total_items": total_items,
                "active_items": active_items,
                "inactive_items": total_items - active_items,
                "categories": categories,
                "confidence_distribution": {
                    "high": high_confidence,
                    "medium": medium_confidence,
                    "low": low_confidence
                },
                "recent_additions": recent_additions,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)} 