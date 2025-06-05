import os
import json
import shutil
from datetime import datetime
from typing import List, Dict, Optional
import uuid

class VersionManager:
    def __init__(self):
        self.versions_dir = "data/versions"
        self.current_version_file = "data/current_version.json"
        os.makedirs(self.versions_dir, exist_ok=True)
        
        # Initialize current version if not exists
        if not os.path.exists(self.current_version_file):
            self._init_current_version()

    def _init_current_version(self):
        """Initialize current version file"""
        initial_version = {
            "version": "1.0.0",
            "release_date": datetime.now().isoformat(),
            "release_notes": "Initial version",
            "status": "active"
        }
        
        with open(self.current_version_file, 'w', encoding='utf-8') as f:
            json.dump(initial_version, f, ensure_ascii=False, indent=2)

    async def get_all_versions(self) -> List[Dict]:
        """Get all available versions"""
        versions = []
        
        if os.path.exists(self.versions_dir):
            for version_file in os.listdir(self.versions_dir):
                if version_file.endswith('.json'):
                    version_path = os.path.join(self.versions_dir, version_file)
                    try:
                        with open(version_path, 'r', encoding='utf-8') as f:
                            version_data = json.load(f)
                            versions.append(version_data)
                    except Exception as e:
                        print(f"Error loading version {version_file}: {e}")
        
        # Sort by release date (newest first)
        versions.sort(key=lambda x: x.get('release_date', ''), reverse=True)
        return versions

    async def get_current_version(self) -> Dict:
        """Get current active version"""
        try:
            with open(self.current_version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading current version: {e}")
            return {"version": "unknown", "error": str(e)}

    async def create_release(self, version: str, changes: List[Dict], release_notes: str) -> Dict:
        """Create a new version release"""
        try:
            # Create version data
            version_data = {
                "version": version,
                "release_date": datetime.now().isoformat(),
                "release_notes": release_notes,
                "changes": changes,
                "status": "active",
                "id": str(uuid.uuid4()),
                "created_by": "system",
                "files_included": []
            }
            
            # Process changes
            processed_changes = await self._process_changes(changes)
            version_data["processed_changes"] = processed_changes
            
            # Save version file
            version_filename = f"version_{version.replace('.', '_')}.json"
            version_path = os.path.join(self.versions_dir, version_filename)
            
            with open(version_path, 'w', encoding='utf-8') as f:
                json.dump(version_data, f, ensure_ascii=False, indent=2)
            
            # Update current version
            await self._update_current_version(version_data)
            
            return {
                "success": True,
                "version": version,
                "message": f"Version {version} created successfully",
                "data": version_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create version {version}"
            }

    async def _process_changes(self, changes: List[Dict]) -> List[Dict]:
        """Process changes for a version release"""
        processed = []
        
        for change in changes:
            change_type = change.get('type', 'unknown')
            change_data = change.get('data', {})
            
            processed_change = {
                "id": str(uuid.uuid4()),
                "type": change_type,
                "timestamp": datetime.now().isoformat(),
                "data": change_data,
                "status": "processed"
            }
            
            if change_type == "append":
                # Handle append operation
                processed_change["description"] = f"Added new item: {change_data.get('title', 'N/A')}"
                
            elif change_type == "replace":
                # Handle replace operation
                processed_change["description"] = f"Replaced item: {change_data.get('old_title', 'N/A')} -> {change_data.get('new_title', 'N/A')}"
                
            elif change_type == "abolish":
                # Handle abolish operation
                processed_change["description"] = f"Abolished item: {change_data.get('title', 'N/A')}"
                processed_change["reason"] = change_data.get('reason', 'Policy change')
                
            processed.append(processed_change)
        
        return processed

    async def _update_current_version(self, version_data: Dict):
        """Update current version file"""
        current_version = {
            "version": version_data["version"],
            "release_date": version_data["release_date"],
            "release_notes": version_data["release_notes"],
            "status": "active",
            "id": version_data["id"]
        }
        
        with open(self.current_version_file, 'w', encoding='utf-8') as f:
            json.dump(current_version, f, ensure_ascii=False, indent=2)

    async def get_version_details(self, version: str) -> Dict:
        """Get details of a specific version"""
        version_filename = f"version_{version.replace('.', '_')}.json"
        version_path = os.path.join(self.versions_dir, version_filename)
        
        try:
            with open(version_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": f"Version {version} not found"}
        except Exception as e:
            return {"error": str(e)}

    async def rollback_to_version(self, version: str) -> Dict:
        """Rollback to a specific version"""
        try:
            # Get version details
            version_data = await self.get_version_details(version)
            
            if "error" in version_data:
                return {
                    "success": False,
                    "error": version_data["error"]
                }
            
            # Update current version
            await self._update_current_version(version_data)
            
            # Create rollback log
            rollback_log = {
                "action": "rollback",
                "target_version": version,
                "rollback_date": datetime.now().isoformat(),
                "previous_version": (await self.get_current_version()).get("version", "unknown")
            }
            
            # Save rollback log
            log_path = f"data/rollback_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(rollback_log, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "message": f"Successfully rolled back to version {version}",
                "rollback_log": rollback_log
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def compare_versions(self, version1: str, version2: str) -> Dict:
        """Compare two versions"""
        try:
            v1_data = await self.get_version_details(version1)
            v2_data = await self.get_version_details(version2)
            
            if "error" in v1_data or "error" in v2_data:
                return {
                    "error": "One or both versions not found"
                }
            
            comparison = {
                "version1": {
                    "version": version1,
                    "date": v1_data.get("release_date"),
                    "changes_count": len(v1_data.get("changes", []))
                },
                "version2": {
                    "version": version2,
                    "date": v2_data.get("release_date"),
                    "changes_count": len(v2_data.get("changes", []))
                },
                "differences": {
                    "added_changes": [],
                    "removed_changes": [],
                    "modified_changes": []
                }
            }
            
            # Simple comparison logic (can be enhanced)
            v1_changes = {c.get('id', str(i)): c for i, c in enumerate(v1_data.get("changes", []))}
            v2_changes = {c.get('id', str(i)): c for i, c in enumerate(v2_data.get("changes", []))}
            
            # Find differences
            for change_id, change in v2_changes.items():
                if change_id not in v1_changes:
                    comparison["differences"]["added_changes"].append(change)
            
            for change_id, change in v1_changes.items():
                if change_id not in v2_changes:
                    comparison["differences"]["removed_changes"].append(change)
            
            return comparison
            
        except Exception as e:
            return {"error": str(e)}

    async def create_backup(self) -> Dict:
        """Create backup of all versions"""
        try:
            backup_dir = f"data/backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Copy versions directory
            if os.path.exists(self.versions_dir):
                shutil.copytree(self.versions_dir, os.path.join(backup_dir, "versions"))
            
            # Copy current version file
            if os.path.exists(self.current_version_file):
                shutil.copy2(self.current_version_file, backup_dir)
            
            backup_info = {
                "backup_path": backup_dir,
                "backup_date": datetime.now().isoformat(),
                "files_backed_up": os.listdir(backup_dir)
            }
            
            # Save backup info
            with open(os.path.join(backup_dir, "backup_info.json"), 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "message": "Backup created successfully",
                "backup_info": backup_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_version_history(self) -> List[Dict]:
        """Get version history with change summary"""
        versions = await self.get_all_versions()
        
        history = []
        for version in versions:
            summary = {
                "version": version.get("version"),
                "release_date": version.get("release_date"),
                "release_notes": version.get("release_notes"),
                "changes_count": len(version.get("changes", [])),
                "status": version.get("status", "unknown")
            }
            
            # Summarize change types
            changes = version.get("changes", [])
            change_summary = {"append": 0, "replace": 0, "abolish": 0, "other": 0}
            
            for change in changes:
                change_type = change.get("type", "other")
                if change_type in change_summary:
                    change_summary[change_type] += 1
                else:
                    change_summary["other"] += 1
            
            summary["change_summary"] = change_summary
            history.append(summary)
        
        return history 