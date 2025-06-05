import os
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

class KnowledgeBase:
    def __init__(self):
        self.data_file = "data/knowledge_base.json"
        self.backup_dir = "data/backups/knowledge"
        self.log_file = "data/knowledge_log.json"
        
        # Initialize directories
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Sample knowledge items
        self.sample_items = [
            {
                "id": "kb_001",
                "title": "增值税一般纳税人标准",
                "content": "年应征增值税销售额超过500万元的纳税人应当申请认定为增值税一般纳税人。年应税销售额未超过规定标准的纳税人，会计核算健全，能够提供准确税务资料的，可以申请成为一般纳税人。",
                "category": "增值税",
                "keywords": ["增值税", "一般纳税人", "认定标准", "销售额"],
                "effective_date": "2024-01-01",
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source": "增值税暂行条例实施细则",
                "related_policies": ["VAT-2024-001"],
                "priority": "high"
            },
            {
                "id": "kb_002", 
                "title": "企业所得税税率",
                "content": "企业所得税的税率为25%。符合条件的小型微利企业，减按20%的税率征收企业所得税。国家需要重点扶持的高新技术企业，减按15%的税率征收企业所得税。",
                "category": "企业所得税",
                "keywords": ["企业所得税", "税率", "小微企业", "高新技术企业"],
                "effective_date": "2024-01-01",
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source": "企业所得税法",
                "related_policies": ["CIT-2024-002"],
                "priority": "high"
            },
            {
                "id": "kb_003",
                "title": "个人所得税起征点",
                "content": "个人所得税起征点为每月5000元。个人所得税税率按照累进税率计算，税率为3%至45%。",
                "category": "个人所得税",
                "keywords": ["个人所得税", "起征点", "累进税率"],
                "effective_date": "2024-01-01",
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source": "个人所得税法",
                "related_policies": ["IIT-2024-003"],
                "priority": "high"
            }
        ]

    async def initialize(self):
        """Initialize knowledge base with sample data if empty"""
        if not os.path.exists(self.data_file):
            await self._save_data(self.sample_items)
            await self._log_operation("initialize", {"items_count": len(self.sample_items)})

    async def _load_data(self) -> List[Dict]:
        """Load knowledge base data from file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    async def _save_data(self, data: List[Dict]):
        """Save knowledge base data to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save knowledge base: {str(e)}")

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
        """Get all knowledge base items"""
        return await self._load_data()

    async def add_item(self, item: Dict) -> Dict:
        """Add new knowledge item"""
        try:
            items = await self._load_data()
            
            # Generate ID if not provided
            if 'id' not in item:
                item['id'] = f"kb_{str(uuid.uuid4())[:8]}"
            
            # Add timestamps
            item['created_at'] = datetime.now().isoformat()
            item['updated_at'] = datetime.now().isoformat()
            
            # Set default values
            item.setdefault('status', 'active')
            item.setdefault('priority', 'medium')
            item.setdefault('keywords', [])
            item.setdefault('related_policies', [])
            
            # Check for duplicate ID
            if any(existing['id'] == item['id'] for existing in items):
                return {"success": False, "error": "Item with this ID already exists"}
            
            items.append(item)
            await self._save_data(items)
            await self._log_operation("add_item", {"item_id": item['id'], "title": item.get('title', 'N/A')})
            
            return {"success": True, "item": item}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def update_item(self, item_id: str, updated_item: Dict) -> Dict:
        """Update existing knowledge item"""
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
            await self._log_operation("update_item", {"item_id": item_id, "title": updated_item.get('title', 'N/A')})
            
            return {"success": True, "item": updated_item}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def delete_item(self, item_id: str) -> Dict:
        """Delete knowledge item"""
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
        """Search knowledge base items"""
        try:
            items = await self._load_data()
            query = query.lower().strip()
            
            if not query:
                return items
            
            matching_items = []
            
            for item in items:
                # Search in title, content, keywords, and category
                searchable_text = " ".join([
                    item.get('title', ''),
                    item.get('content', ''),
                    item.get('category', ''),
                    " ".join(item.get('keywords', []))
                ]).lower()
                
                if query in searchable_text:
                    # Calculate relevance score
                    score = 0
                    if query in item.get('title', '').lower():
                        score += 10
                    if query in item.get('keywords', []):
                        score += 8
                    if query in item.get('category', '').lower():
                        score += 5
                    if query in item.get('content', '').lower():
                        score += 1
                    
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

    async def init_from_file(self, file_path: str) -> Dict:
        """Initialize knowledge base from JSON file"""
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
                if 'title' not in item or 'content' not in item:
                    continue
                
                # Add missing fields
                if 'id' not in item:
                    item['id'] = f"kb_{str(uuid.uuid4())[:8]}"
                
                item.setdefault('created_at', datetime.now().isoformat())
                item.setdefault('updated_at', datetime.now().isoformat())
                item.setdefault('status', 'active')
                item.setdefault('priority', 'medium')
                item.setdefault('keywords', [])
                item.setdefault('category', 'general')
                
                processed_items.append(item)
            
            # Save processed items
            await self._save_data(processed_items)
            await self._log_operation("init_from_file", {
                "file_path": file_path,
                "items_loaded": len(processed_items)
            })
            
            return {
                "success": True,
                "message": f"Successfully loaded {len(processed_items)} items from {file_path}",
                "items_count": len(processed_items)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def export_all(self) -> Dict:
        """Export entire knowledge base"""
        try:
            items = await self._load_data()
            export_data = {
                "export_time": datetime.now().isoformat(),
                "items_count": len(items),
                "items": items
            }
            
            # Create export file
            export_filename = f"knowledge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        """Process updates from crawler and update knowledge base"""
        try:
            processed_count = 0
            added_count = 0
            updated_count = 0
            
            for update in updates:
                if update.get('type') == 'new_file' or update.get('type') == 'modified_file':
                    # Extract information from the update
                    new_item = await self._extract_knowledge_from_update(update)
                    
                    if new_item:
                        # Check if item already exists
                        existing_items = await self._load_data()
                        existing_item = None
                        
                        for item in existing_items:
                            if (item.get('source_file') == update.get('filename') or 
                                item.get('title') == new_item.get('title')):
                                existing_item = item
                                break
                        
                        if existing_item:
                            # Update existing item
                            result = await self.update_item(existing_item['id'], new_item)
                            if result.get('success'):
                                updated_count += 1
                        else:
                            # Add new item
                            result = await self.add_item(new_item)
                            if result.get('success'):
                                added_count += 1
                        
                        processed_count += 1
            
            await self._log_operation("process_updates", {
                "processed_count": processed_count,
                "added_count": added_count,
                "updated_count": updated_count
            })
            
            return {
                "success": True,
                "processed_count": processed_count,
                "added_count": added_count,
                "updated_count": updated_count
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _extract_knowledge_from_update(self, update: Dict) -> Optional[Dict]:
        """Extract knowledge item from update information"""
        try:
            # This is a simplified extraction - in real implementation,
            # you would parse the actual HTML content
            
            update_type = update.get('update_type', 'unknown')
            description = update.get('description', '')
            category = update.get('category', 'general')
            
            if update_type == 'policy_change':
                return {
                    "title": f"政策变更: {category}",
                    "content": description,
                    "category": category,
                    "keywords": [category, "政策变更", "更新"],
                    "effective_date": datetime.now().strftime('%Y-%m-%d'),
                    "status": "active",
                    "priority": update.get('priority', 'medium'),
                    "source": "系统自动提取",
                    "source_file": update.get('filename', ''),
                    "auto_generated": True
                }
            
            elif update_type == 'new_regulation':
                return {
                    "title": f"新法规: {category}",
                    "content": description,
                    "category": category,
                    "keywords": [category, "新法规", "法规"],
                    "effective_date": datetime.now().strftime('%Y-%m-%d'),
                    "status": "active",
                    "priority": update.get('priority', 'medium'),
                    "source": "系统自动提取",
                    "source_file": update.get('filename', ''),
                    "auto_generated": True
                }
            
            return None
            
        except Exception as e:
            print(f"Error extracting knowledge from update: {e}")
            return None

    async def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
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
            
            # Priority breakdown
            priorities = {}
            for item in items:
                priority = item.get('priority', 'unknown')
                priorities[priority] = priorities.get(priority, 0) + 1
            
            # Recent updates (last 7 days)
            recent_updates = 0
            cutoff_date = (datetime.now() - timedelta(days=7)).isoformat()
            for item in items:
                if item.get('updated_at', '') > cutoff_date:
                    recent_updates += 1
            
            return {
                "total_items": total_items,
                "active_items": active_items,
                "inactive_items": total_items - active_items,
                "categories": categories,
                "priorities": priorities,
                "recent_updates": recent_updates,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}

    async def get_item_by_id(self, item_id: str) -> Optional[Dict]:
        """Get specific item by ID"""
        try:
            items = await self._load_data()
            for item in items:
                if item.get('id') == item_id:
                    return item
            return None
        except Exception:
            return None

    async def backup_data(self) -> Dict:
        """Create backup of knowledge base"""
        try:
            backup_filename = f"knowledge_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            items = await self._load_data()
            backup_data = {
                "backup_time": datetime.now().isoformat(),
                "items_count": len(items),
                "items": items
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            await self._log_operation("backup_data", {"backup_path": backup_path})
            
            return {
                "success": True,
                "backup_path": backup_path,
                "items_backed_up": len(items)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)} 