import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re
import random

class AnnouncementCrawler:
    def __init__(self):
        self.data_dir = "data"
        self.announcements_dir = "data/announcements"
        self.status_file = "data/crawler_status.json"
        self.hash_file = "data/announcement_hashes.json"
        self.last_check_file = "data/last_check.json"
        
        # Initialize directories and files
        os.makedirs(self.announcements_dir, exist_ok=True)
        self._init_status_files()

    def _init_status_files(self):
        """Initialize status tracking files"""
        if not os.path.exists(self.status_file):
            initial_status = {
                "status": "idle",
                "last_check": None,
                "last_update": None,
                "total_checks": 0,
                "updates_found": 0,
                "errors": 0
            }
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(initial_status, f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(self.hash_file):
            with open(self.hash_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(self.last_check_file):
            with open(self.last_check_file, 'w', encoding='utf-8') as f:
                json.dump({"last_check": None, "files_checked": []}, f, ensure_ascii=False, indent=2)

    async def check_for_updates(self) -> Dict:
        """Check for updates in announcement files"""
        await self._update_status("checking")
        
        try:
            # Get current file hashes
            current_hashes = await self._get_current_hashes()
            
            # Load stored hashes
            stored_hashes = await self._load_stored_hashes()
            
            # Compare hashes to find changes
            changes = await self._compare_hashes(stored_hashes, current_hashes)
            
            # Simulate random updates (for demonstration)
            simulated_changes = await self._simulate_random_updates()
            changes.extend(simulated_changes)
            
            # Update stored hashes
            await self._save_hashes(current_hashes)
            
            # Update status
            await self._update_status("idle")
            await self._increment_check_count()
            
            if changes:
                await self._increment_update_count()
            
            # Update last check
            await self._update_last_check()
            
            result = {
                "has_updates": len(changes) > 0,
                "updates": changes,
                "check_time": datetime.now().isoformat(),
                "files_checked": len(current_hashes),
                "changes_found": len(changes)
            }
            
            return result
            
        except Exception as e:
            await self._update_status("error")
            await self._increment_error_count()
            return {
                "has_updates": False,
                "error": str(e),
                "check_time": datetime.now().isoformat()
            }

    async def _get_current_hashes(self) -> Dict[str, str]:
        """Get MD5 hashes of all HTML files"""
        hashes = {}
        
        if os.path.exists(self.announcements_dir):
            for filename in os.listdir(self.announcements_dir):
                if filename.endswith('.html'):
                    filepath = os.path.join(self.announcements_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            hash_md5 = hashlib.md5(content.encode()).hexdigest()
                            hashes[filename] = hash_md5
                    except Exception as e:
                        print(f"Error reading file {filename}: {e}")
        
        return hashes

    async def _load_stored_hashes(self) -> Dict[str, str]:
        """Load previously stored file hashes"""
        try:
            with open(self.hash_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    async def _save_hashes(self, hashes: Dict[str, str]):
        """Save current file hashes"""
        try:
            with open(self.hash_file, 'w', encoding='utf-8') as f:
                json.dump(hashes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving hashes: {e}")

    async def _compare_hashes(self, stored: Dict[str, str], current: Dict[str, str]) -> List[Dict]:
        """Compare stored and current hashes to find changes"""
        changes = []
        
        # Check for new files
        for filename, hash_value in current.items():
            if filename not in stored:
                changes.append({
                    "type": "new_file",
                    "filename": filename,
                    "hash": hash_value,
                    "timestamp": datetime.now().isoformat()
                })
        
        # Check for modified files
        for filename, hash_value in current.items():
            if filename in stored and stored[filename] != hash_value:
                changes.append({
                    "type": "modified_file",
                    "filename": filename,
                    "old_hash": stored[filename],
                    "new_hash": hash_value,
                    "timestamp": datetime.now().isoformat()
                })
        
        # Check for deleted files
        for filename, hash_value in stored.items():
            if filename not in current:
                changes.append({
                    "type": "deleted_file",
                    "filename": filename,
                    "hash": hash_value,
                    "timestamp": datetime.now().isoformat()
                })
        
        return changes

    async def _simulate_random_updates(self) -> List[Dict]:
        """Simulate random updates for demonstration purposes"""
        # 30% chance of having updates
        if random.random() > 0.3:
            return []
        
        simulated_updates = []
        update_types = ["policy_change", "new_regulation", "rate_adjustment", "deadline_extension"]
        
        num_updates = random.randint(1, 3)
        for _ in range(num_updates):
            update_type = random.choice(update_types)
            
            simulated_update = {
                "type": "simulated_update",
                "update_type": update_type,
                "description": self._get_update_description(update_type),
                "priority": random.choice(["high", "medium", "low"]),
                "category": random.choice(["增值税", "企业所得税", "个人所得税", "消费税"]),
                "timestamp": datetime.now().isoformat(),
                "simulated": True
            }
            
            simulated_updates.append(simulated_update)
        
        return simulated_updates

    def _get_update_description(self, update_type: str) -> str:
        """Get description for simulated update types"""
        descriptions = {
            "policy_change": "检测到税务政策变更，需要更新知识库",
            "new_regulation": "发现新的税务法规，需要添加到系统",
            "rate_adjustment": "税率调整公告，需要更新相关税率信息",
            "deadline_extension": "税务申报期限延长，需要更新时间信息"
        }
        return descriptions.get(update_type, "检测到税务相关更新")

    async def parse_html_file(self, html_path: str) -> Dict:
        """Parse specific HTML file and extract tax information"""
        try:
            if not os.path.exists(html_path):
                return {"error": f"File not found: {html_path}"}
            
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse HTML content
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract information
            parsed_info = {
                "filename": os.path.basename(html_path),
                "parse_time": datetime.now().isoformat(),
                "content": {}
            }
            
            # Extract title
            title_elem = soup.find('title')
            if title_elem:
                parsed_info["content"]["title"] = title_elem.get_text().strip()
            
            # Extract announcement content
            announcement_div = soup.find('div', class_='announcement')
            if announcement_div:
                # Extract category
                category_elem = announcement_div.find('div', class_='category')
                if category_elem:
                    parsed_info["content"]["category"] = category_elem.get_text().strip()
                
                # Extract main content
                content_div = announcement_div.find('div', class_='content')
                if content_div:
                    parsed_info["content"]["main_content"] = content_div.get_text().strip()
                
                # Extract meta information
                meta_div = announcement_div.find('div', class_='meta')
                if meta_div:
                    meta_text = meta_div.get_text()
                    parsed_info["content"]["meta"] = self._parse_meta_info(meta_text)
            
            # Extract policy items if batch announcement
            items = []
            item_divs = soup.find_all('div', class_='item')
            for item_div in item_divs:
                item_info = {}
                
                # Extract item title
                h3_elem = item_div.find('h3')
                if h3_elem:
                    item_info["title"] = h3_elem.get_text().strip()
                
                # Extract item content
                content_div = item_div.find('div', class_='item-content')
                if content_div:
                    item_info["content"] = content_div.get_text().strip()
                
                # Extract item meta
                meta_div = item_div.find('div', class_='item-meta')
                if meta_div:
                    item_info["meta"] = meta_div.get_text().strip()
                
                if item_info:
                    items.append(item_info)
            
            if items:
                parsed_info["content"]["items"] = items
            
            return parsed_info
            
        except Exception as e:
            return {"error": str(e)}

    def _parse_meta_info(self, meta_text: str) -> Dict:
        """Parse meta information from text"""
        meta_info = {}
        
        # Extract announcement ID
        id_match = re.search(r'公告编号:\s*([^\s|]+)', meta_text)
        if id_match:
            meta_info["announcement_id"] = id_match.group(1).strip()
        
        # Extract effective date
        date_match = re.search(r'生效日期:\s*([^\s|]+)', meta_text)
        if date_match:
            meta_info["effective_date"] = date_match.group(1).strip()
        
        # Extract publish time
        time_match = re.search(r'发布时间:\s*([^\s|]+)', meta_text)
        if time_match:
            meta_info["publish_time"] = time_match.group(1).strip()
        
        return meta_info

    async def get_status(self) -> Dict:
        """Get current crawler status"""
        try:
            with open(self.status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            # Add additional runtime information
            last_check_info = await self._get_last_check_info()
            status.update(last_check_info)
            
            return status
            
        except Exception as e:
            return {"error": str(e)}

    async def _get_last_check_info(self) -> Dict:
        """Get information about last check"""
        try:
            with open(self.last_check_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"last_check": None, "files_checked": []}

    async def _update_status(self, status: str):
        """Update crawler status"""
        try:
            current_status = await self.get_status()
            current_status["status"] = status
            current_status["last_status_update"] = datetime.now().isoformat()
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(current_status, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error updating status: {e}")

    async def _increment_check_count(self):
        """Increment total check count"""
        try:
            current_status = await self.get_status()
            current_status["total_checks"] = current_status.get("total_checks", 0) + 1
            current_status["last_check"] = datetime.now().isoformat()
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(current_status, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error incrementing check count: {e}")

    async def _increment_update_count(self):
        """Increment updates found count"""
        try:
            current_status = await self.get_status()
            current_status["updates_found"] = current_status.get("updates_found", 0) + 1
            current_status["last_update"] = datetime.now().isoformat()
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(current_status, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error incrementing update count: {e}")

    async def _increment_error_count(self):
        """Increment error count"""
        try:
            current_status = await self.get_status()
            current_status["errors"] = current_status.get("errors", 0) + 1
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(current_status, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error incrementing error count: {e}")

    async def _update_last_check(self):
        """Update last check information"""
        try:
            files_checked = []
            if os.path.exists(self.announcements_dir):
                files_checked = [f for f in os.listdir(self.announcements_dir) if f.endswith('.html')]
            
            last_check_info = {
                "last_check": datetime.now().isoformat(),
                "files_checked": files_checked,
                "files_count": len(files_checked)
            }
            
            with open(self.last_check_file, 'w', encoding='utf-8') as f:
                json.dump(last_check_info, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error updating last check: {e}")

    async def get_stats(self) -> Dict:
        """Get crawler statistics"""
        status = await self.get_status()
        
        stats = {
            "total_checks": status.get("total_checks", 0),
            "updates_found": status.get("updates_found", 0),
            "errors": status.get("errors", 0),
            "last_check": status.get("last_check"),
            "last_update": status.get("last_update"),
            "current_status": status.get("status", "unknown")
        }
        
        # Calculate uptime and success rate
        if stats["total_checks"] > 0:
            stats["success_rate"] = (stats["total_checks"] - stats["errors"]) / stats["total_checks"] * 100
        else:
            stats["success_rate"] = 0
        
        return stats 