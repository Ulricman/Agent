import os
import json
import shutil
import zipfile
import datetime
from typing import Dict, List, Optional
from pathlib import Path

class BackupManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.backup_dir = self.data_dir / "backups"
        self.html_dir = self.data_dir / "announcements"
        self.system_backup_dir = self.backup_dir / "system"
        
        # 确保备份目录存在
        self.backup_dir.mkdir(exist_ok=True)
        self.system_backup_dir.mkdir(exist_ok=True)
        
        # 定义需要备份的数据文件
        self.data_files = [
            "knowledge_base.json",
            "qa_database.json", 
            "system_log.json",
            "crawler_status.json",
            "current_version.json",
            "knowledge_log.json",
            "qa_log.json",
            "announcement_hashes.json"
        ]
        
        # 定义默认数据
        self.default_data = {
            "knowledge_base.json": [
                {
                    "id": "kb_001",
                    "title": "增值税一般纳税人标准",
                    "content": "年应征增值税销售额超过500万元的纳税人应当申请认定为增值税一般纳税人。年应税销售额未超过规定标准的纳税人，会计核算健全，能够提供准确税务资料的，可以申请成为一般纳税人。",
                    "category": "增值税",
                    "keywords": ["增值税", "一般纳税人", "认定标准", "销售额"],
                    "effective_date": "2024-01-01",
                    "status": "active",
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
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
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
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
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
                    "source": "个人所得税法",
                    "related_policies": ["IIT-2024-003"],
                    "priority": "high"
                }
            ],
            "qa_database.json": [
                {
                    "id": "qa_001",
                    "question": "增值税一般纳税人的认定标准是什么？",
                    "answer": "增值税一般纳税人的认定标准主要有：1）年应征增值税销售额超过500万元；2）年应税销售额未超过标准但会计核算健全，能够提供准确税务资料的纳税人也可申请认定。",
                    "category": "增值税",
                    "keywords": ["增值税", "一般纳税人", "认定标准"],
                    "confidence": 0.95,
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
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
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
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
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
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
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
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
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
                    "source": "税务登记管理办法",
                    "related_questions": [],
                    "priority": "medium",
                    "status": "active"
                }
            ],
            "system_log.json": {
                "logs": [],
                "created_at": datetime.datetime.now().isoformat()
            },
            "crawler_status.json": {
                "status": "idle",
                "total_checks": 0,
                "updates_found": 0,
                "errors": 0,
                "last_check": None,
                "last_update": None,
                "success_rate": 100.0
            },
            "current_version.json": {
                "version": "1.0.0",
                "release_date": datetime.datetime.now().isoformat(),
                "release_notes": "初始版本"
            },
            "knowledge_log.json": {
                "operations": [],
                "created_at": datetime.datetime.now().isoformat()
            },
            "qa_log.json": {
                "operations": [],
                "created_at": datetime.datetime.now().isoformat()
            },
            "announcement_hashes.json": {
                "files": {},
                "last_updated": datetime.datetime.now().isoformat()
            }
        }

    def create_backup(self, backup_name: Optional[str] = None) -> Dict:
        """创建完整的系统备份"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            if not backup_name:
                backup_name = f"system_backup_{timestamp}"
            
            backup_path = self.system_backup_dir / backup_name
            backup_path.mkdir(exist_ok=True)
            
            # 备份数据文件
            data_backup_dir = backup_path / "data"
            data_backup_dir.mkdir(exist_ok=True)
            
            backed_up_files = []
            for file_name in self.data_files:
                source_file = self.data_dir / file_name
                if source_file.exists():
                    shutil.copy2(source_file, data_backup_dir / file_name)
                    backed_up_files.append(file_name)
            
            # 备份HTML文件
            html_backup_dir = backup_path / "announcements"
            if self.html_dir.exists():
                shutil.copytree(self.html_dir, html_backup_dir, dirs_exist_ok=True)
            
            # 创建备份信息文件
            backup_info = {
                "name": backup_name,
                "timestamp": timestamp,
                "created_at": datetime.datetime.now().isoformat(),
                "backed_up_files": backed_up_files,
                "html_files_count": len(list(html_backup_dir.glob("*.html"))) if html_backup_dir.exists() else 0,
                "backup_size": self._get_directory_size(backup_path),
                "type": "full_backup"
            }
            
            with open(backup_path / "backup_info.json", "w", encoding="utf-8") as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)
            
            # 创建ZIP压缩包
            zip_path = self.system_backup_dir / f"{backup_name}.zip"
            self._create_zip_backup(backup_path, zip_path)
            
            # 删除临时目录
            shutil.rmtree(backup_path)
            
            backup_info["zip_path"] = str(zip_path)
            backup_info["zip_size"] = zip_path.stat().st_size
            
            return {
                "success": True,
                "backup_info": backup_info,
                "message": f"备份创建成功: {backup_name}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "备份创建失败"
            }

    def restore_backup(self, backup_name: str) -> Dict:
        """从备份恢复系统"""
        try:
            zip_path = self.system_backup_dir / f"{backup_name}.zip"
            if not zip_path.exists():
                return {
                    "success": False,
                    "error": "备份文件不存在",
                    "message": f"找不到备份: {backup_name}"
                }
            
            # 创建临时恢复目录
            temp_dir = self.system_backup_dir / f"temp_restore_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            temp_dir.mkdir(exist_ok=True)
            
            try:
                # 解压备份文件
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # 获取备份信息
                backup_info_path = temp_dir / "backup_info.json"
                if backup_info_path.exists():
                    with open(backup_info_path, "r", encoding="utf-8") as f:
                        backup_info = json.load(f)
                else:
                    backup_info = {"backed_up_files": self.data_files}
                
                # 恢复数据文件
                data_backup_dir = temp_dir / "data"
                restored_files = []
                if data_backup_dir.exists():
                    for file_name in backup_info.get("backed_up_files", []):
                        backup_file = data_backup_dir / file_name
                        target_file = self.data_dir / file_name
                        if backup_file.exists():
                            shutil.copy2(backup_file, target_file)
                            restored_files.append(file_name)
                
                # 恢复HTML文件
                html_backup_dir = temp_dir / "announcements"
                restored_html_count = 0
                if html_backup_dir.exists():
                    # 清空现有HTML文件
                    if self.html_dir.exists():
                        shutil.rmtree(self.html_dir)
                    # 恢复HTML文件
                    shutil.copytree(html_backup_dir, self.html_dir)
                    restored_html_count = len(list(self.html_dir.glob("*.html")))
                
                return {
                    "success": True,
                    "backup_info": backup_info,
                    "restored_files": restored_files,
                    "restored_html_count": restored_html_count,
                    "message": f"系统已成功恢复到备份: {backup_name}"
                }
                
            finally:
                # 清理临时目录
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "备份恢复失败"
            }

    def reset_to_default(self) -> Dict:
        """重置系统到默认状态"""
        try:
            # 创建重置前的自动备份
            auto_backup_result = self.create_backup(f"auto_backup_before_reset_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # 重置数据文件到默认状态
            reset_files = []
            for file_name, default_content in self.default_data.items():
                target_file = self.data_dir / file_name
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(default_content, f, ensure_ascii=False, indent=2)
                reset_files.append(file_name)
            
            # 清空HTML文件目录，只保留示例文件
            if self.html_dir.exists():
                # 删除所有现有文件
                for file_path in self.html_dir.glob("*"):
                    if file_path.is_file():
                        file_path.unlink()
            else:
                self.html_dir.mkdir(exist_ok=True)
            
            # 创建默认的示例HTML文件
            self._create_default_html_files()
            
            # 清空版本目录
            versions_dir = self.data_dir / "versions"
            if versions_dir.exists():
                shutil.rmtree(versions_dir)
            versions_dir.mkdir(exist_ok=True)
            
            return {
                "success": True,
                "reset_files": reset_files,
                "auto_backup": auto_backup_result.get("backup_info"),
                "message": "系统已重置到默认状态，重置前的数据已自动备份"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "系统重置失败"
            }

    def list_backups(self) -> List[Dict]:
        """列出所有可用的备份"""
        backups = []
        
        try:
            for zip_file in self.system_backup_dir.glob("*.zip"):
                # 尝试从ZIP文件中读取备份信息
                try:
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        if "backup_info.json" in zip_ref.namelist():
                            with zip_ref.open("backup_info.json") as f:
                                backup_info = json.load(f)
                        else:
                            # 如果没有备份信息文件，创建基本信息
                            backup_info = {
                                "name": zip_file.stem,
                                "created_at": datetime.datetime.fromtimestamp(zip_file.stat().st_mtime).isoformat(),
                                "type": "legacy_backup"
                            }
                    
                    backup_info["zip_size"] = zip_file.stat().st_size
                    backup_info["zip_size_human"] = self._format_file_size(zip_file.stat().st_size)
                    backups.append(backup_info)
                    
                except Exception as e:
                    # 如果无法读取ZIP文件，跳过
                    continue
            
            # 按创建时间排序
            backups.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
        except Exception as e:
            pass
        
        return backups

    def delete_backup(self, backup_name: str) -> Dict:
        """删除指定的备份"""
        try:
            zip_path = self.system_backup_dir / f"{backup_name}.zip"
            if not zip_path.exists():
                return {
                    "success": False,
                    "error": "备份文件不存在",
                    "message": f"找不到备份: {backup_name}"
                }
            
            zip_path.unlink()
            
            return {
                "success": True,
                "message": f"备份已删除: {backup_name}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "备份删除失败"
            }

    def get_system_status(self) -> Dict:
        """获取系统状态信息"""
        try:
            status = {
                "data_files": {},
                "html_files_count": 0,
                "total_size": 0,
                "backups_count": len(list(self.system_backup_dir.glob("*.zip"))),
                "last_backup": None
            }
            
            # 检查数据文件状态
            for file_name in self.data_files:
                file_path = self.data_dir / file_name
                if file_path.exists():
                    file_stat = file_path.stat()
                    status["data_files"][file_name] = {
                        "exists": True,
                        "size": file_stat.st_size,
                        "modified": datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                    }
                    status["total_size"] += file_stat.st_size
                else:
                    status["data_files"][file_name] = {"exists": False}
            
            # 检查HTML文件
            if self.html_dir.exists():
                html_files = list(self.html_dir.glob("*.html"))
                status["html_files_count"] = len(html_files)
                for html_file in html_files:
                    status["total_size"] += html_file.stat().st_size
            
            # 获取最近的备份信息
            backups = self.list_backups()
            if backups:
                status["last_backup"] = backups[0]
            
            status["total_size_human"] = self._format_file_size(status["total_size"])
            
            return status
            
        except Exception as e:
            return {
                "error": str(e),
                "message": "获取系统状态失败"
            }

    def _create_zip_backup(self, source_dir: Path, zip_path: Path):
        """创建ZIP压缩备份"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    arc_path = file_path.relative_to(source_dir)
                    zip_ref.write(file_path, arc_path)

    def _get_directory_size(self, directory: Path) -> int:
        """计算目录大小"""
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass
        return total_size

    def _format_file_size(self, bytes_size: int) -> str:
        """格式化文件大小"""
        if bytes_size == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = float(bytes_size)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.2f} {units[unit_index]}"

    def _create_default_html_files(self):
        """创建默认的示例HTML文件"""
        default_html_template = """<!DOCTYPE html>
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
            background: #f5f5f5;
        }}
        .announcement {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #e1e5e9;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .title {{
            color: #2c3e50;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .meta {{
            color: #6c757d;
            font-size: 14px;
        }}
        .content {{
            color: #343a40;
            line-height: 1.8;
        }}
        .category {{
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="announcement">
        <div class="header">
            <div class="category">{category}</div>
            <h1 class="title">{title}</h1>
            <div class="meta">
                <span>发布日期: {date}</span> | 
                <span>生效日期: {effective_date}</span> |
                <span>公告编号: {announcement_id}</span>
            </div>
        </div>
        <div class="content">
            {content}
        </div>
    </div>
</body>
</html>"""

        # 默认示例文件
        default_files = [
            {
                "filename": "sample_announcement_1.html",
                "title": "关于调整增值税税率的公告",
                "category": "增值税",
                "content": """
                <p>为贯彻落实党中央、国务院决策部署，推进增值税实质性减税，现将调整增值税税率有关政策公告如下：</p>
                
                <h3>一、纳税人发生增值税应税销售行为或者进口货物</h3>
                <p>原适用17%和11%税率的，税率分别调整为16%、10%。</p>
                
                <h3>二、纳税人购进农产品</h3>
                <p>原适用11%扣除率的，扣除率调整为10%。</p>
                
                <h3>三、纳税人购进用于生产销售或委托加工17%税率货物的农产品</h3>
                <p>按照12%的扣除率计算进项税额。</p>
                
                <p>本公告自2018年5月1日起执行。</p>
                """,
                "date": "2024-01-01",
                "effective_date": "2024-01-01",
                "announcement_id": "VAT-2024-001"
            },
            {
                "filename": "sample_announcement_2.html", 
                "title": "企业所得税优惠政策延续公告",
                "category": "企业所得税",
                "content": """
                <p>为支持小微企业发展，现将有关企业所得税优惠政策公告如下：</p>
                
                <h3>一、对小型微利企业年应纳税所得额不超过100万元的部分</h3>
                <p>减按25%计入应纳税所得额，按20%的税率缴纳企业所得税。</p>
                
                <h3>二、对年应纳税所得额超过100万元但不超过300万元的部分</h3>
                <p>减按50%计入应纳税所得额，按20%的税率缴纳企业所得税。</p>
                
                <h3>三、小型微利企业判定标准</h3>
                <p>从业人数不超过300人、资产总额不超过5000万元、年度应纳税所得额不超过300万元。</p>
                
                <p>本公告执行期限为2024年1月1日至2024年12月31日。</p>
                """,
                "date": "2024-01-01", 
                "effective_date": "2024-01-01",
                "announcement_id": "CIT-2024-002"
            },
            {
                "filename": "sample_announcement_3.html",
                "title": "个人所得税专项附加扣除标准调整",
                "category": "个人所得税", 
                "content": """
                <p>根据《个人所得税法》有关规定，现将个人所得税专项附加扣除标准调整公告如下：</p>
                
                <h3>一、子女教育专项附加扣除</h3>
                <p>纳税人的子女接受全日制学历教育的相关支出，按照每个子女每月1000元的标准定额扣除。</p>
                
                <h3>二、继续教育专项附加扣除</h3>
                <p>纳税人在中国境内接受学历（学位）继续教育的支出，在学历（学位）教育期间按照每月400元定额扣除。</p>
                
                <h3>三、大病医疗专项附加扣除</h3>
                <p>在一个纳税年度内，纳税人发生的与基本医保相关的医药费用支出，扣除医保报销后个人负担累计超过15000元的部分，由纳税人在办理年度汇算清缴时，在80000元限额内据实扣除。</p>
                
                <p>本公告自2024年1月1日起执行。</p>
                """,
                "date": "2024-01-01",
                "effective_date": "2024-01-01", 
                "announcement_id": "IIT-2024-003"
            }
        ]

        for file_info in default_files:
            html_content = default_html_template.format(**file_info)
            file_path = self.html_dir / file_info["filename"]
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content) 