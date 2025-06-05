import os
import json
from datetime import datetime
from typing import List, Dict
import random

class HTMLGenerator:
    def __init__(self):
        self.template_dir = "templates"
        self.output_dir = "data/announcements"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Sample tax announcement data
        self.sample_categories = [
            "增值税", "企业所得税", "个人所得税", "消费税", 
            "进出口税", "资源税", "环境保护税", "印花税"
        ]
        
        self.sample_announcements = [
            {
                "title": "关于调整增值税税率的公告",
                "content": "根据《中华人民共和国增值税暂行条例》规定，现对增值税税率进行如下调整：一般纳税人销售货物或者提供加工、修理修配劳务的税率为13%；销售交通运输、邮政、基础电信、建筑、不动产租赁服务，销售不动产，转让土地使用权的税率为9%。",
                "category": "增值税",
                "effective_date": "2024-01-01",
                "announcement_id": "VAT-2024-001"
            },
            {
                "title": "企业所得税优惠政策延续公告",
                "content": "为支持小微企业发展，对年应纳税所得额不超过100万元的部分，减按12.5%计入应纳税所得额，按20%的税率缴纳企业所得税；对年应纳税所得额超过100万元但不超过300万元的部分，减按50%计入应纳税所得额，按20%的税率缴纳企业所得税。",
                "category": "企业所得税",
                "effective_date": "2024-01-01",
                "announcement_id": "CIT-2024-002"
            },
            {
                "title": "个人所得税专项附加扣除标准调整",
                "content": "自2024年1月1日起，个人所得税专项附加扣除标准调整如下：子女教育每个子女每月1000元；继续教育每月300元或400元；大病医疗每年限额80000元；住房贷款利息每月1000元；住房租金每月800元、1100元、1500元；赡养老人每月2000元。",
                "category": "个人所得税",
                "effective_date": "2024-01-01",
                "announcement_id": "IIT-2024-003"
            }
        ]

    async def generate_sample_announcement(self) -> str:
        """Generate a sample tax announcement HTML"""
        announcement = random.choice(self.sample_announcements)
        html_content = self._create_html_template(announcement)
        
        # Save to file
        filename = f"announcement_{announcement['announcement_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return html_content

    async def create_announcement(self, items: List[Dict]) -> str:
        """Create announcement from provided items"""
        html_content = self._create_batch_html_template(items)
        
        # Save to file
        filename = f"batch_announcement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return html_content

    def _create_html_template(self, announcement: Dict) -> str:
        """Create HTML template for single announcement"""
        return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{announcement['title']}</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .announcement {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #e74c3c;
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
            color: #7f8c8d;
            font-size: 14px;
        }}
        .content {{
            color: #34495e;
            font-size: 16px;
            line-height: 1.8;
        }}
        .category {{
            background: #3498db;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            display: inline-block;
            margin-bottom: 10px;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #95a5a6;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="announcement">
        <div class="header">
            <div class="category">{announcement['category']}</div>
            <h1 class="title">{announcement['title']}</h1>
            <div class="meta">
                公告编号: {announcement['announcement_id']} | 
                生效日期: {announcement['effective_date']} | 
                发布时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        
        <div class="content">
            <p>{announcement['content']}</p>
        </div>
        
        <div class="footer">
            <p>本公告自发布之日起施行。</p>
            <p>国家税务总局</p>
            <p>{datetime.now().strftime('%Y年%m月%d日')}</p>
        </div>
    </div>
</body>
</html>
"""

    def _create_batch_html_template(self, items: List[Dict]) -> str:
        """Create HTML template for batch announcements"""
        items_html = ""
        for i, item in enumerate(items, 1):
            items_html += f"""
            <div class="item">
                <h3>{i}. {item.get('title', 'N/A')}</h3>
                <div class="item-meta">
                    <span class="category">{item.get('category', 'N/A')}</span>
                    <span class="date">生效日期: {item.get('effective_date', 'N/A')}</span>
                    <span class="status status-{item.get('status', 'active')}">{item.get('status', 'active')}</span>
                </div>
                <div class="item-content">
                    {item.get('content', 'N/A')}
                </div>
            </div>
            """
        
        return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>税务政策批量公告</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", Arial, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .announcement {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #e74c3c;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .title {{
            color: #2c3e50;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .meta {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        .item {{
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ecf0f1;
            border-radius: 5px;
            background: #fafafa;
        }}
        .item h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        .item-meta {{
            margin-bottom: 15px;
        }}
        .category {{
            background: #3498db;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin-right: 10px;
        }}
        .date {{
            color: #7f8c8d;
            font-size: 12px;
            margin-right: 10px;
        }}
        .status {{
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 12px;
            color: white;
        }}
        .status-active {{ background: #27ae60; }}
        .status-draft {{ background: #f39c12; }}
        .status-archived {{ background: #95a5a6; }}
        .item-content {{
            color: #34495e;
            line-height: 1.7;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #95a5a6;
            font-size: 12px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="announcement">
        <div class="header">
            <h1 class="title">税务政策批量公告</h1>
            <div class="meta">
                发布时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                共 {len(items)} 项政策
            </div>
        </div>
        
        <div class="content">
            {items_html}
        </div>
        
        <div class="footer">
            <p>以上政策自各自生效日期起施行。如有疑问，请咨询当地税务部门。</p>
            <p>国家税务总局</p>
            <p>{datetime.now().strftime('%Y年%m月%d日')}</p>
        </div>
    </div>
</body>
</html>
"""

    async def create_sample_files(self):
        """Create sample HTML files for testing"""
        for i, announcement in enumerate(self.sample_announcements):
            html_content = self._create_html_template(announcement)
            filename = f"sample_announcement_{i+1}.html"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
        return f"Created {len(self.sample_announcements)} sample HTML files"

    def get_all_announcements(self) -> List[Dict]:
        """Get list of all generated announcement files with metadata"""
        if not os.path.exists(self.output_dir):
            return []
        
        files = []
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(self.output_dir, filename)
                try:
                    stat = os.stat(filepath)
                    size = stat.st_size
                    created = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Try to extract title from HTML content
                    title = self._extract_title_from_file(filepath)
                    
                    files.append({
                        'filename': filename,
                        'title': title,
                        'size': size,
                        'size_human': self._format_file_size(size),
                        'created': created,
                        'modified': modified,
                        'url_path': f"/static/announcements/{filename}"
                    })
                except Exception as e:
                    # If file reading fails, include basic info
                    files.append({
                        'filename': filename,
                        'title': 'Unknown',
                        'size': 0,
                        'size_human': '0 B',
                        'created': 'Unknown',
                        'modified': 'Unknown',
                        'url_path': f"/static/announcements/{filename}",
                        'error': str(e)
                    })
        
        # Sort by creation time (newest first)
        files.sort(key=lambda x: x['created'], reverse=True)
        return files

    def _extract_title_from_file(self, filepath: str) -> str:
        """Extract title from HTML file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Try to find title tag
                if '<title>' in content and '</title>' in content:
                    start = content.find('<title>') + 7
                    end = content.find('</title>')
                    return content[start:end].strip()
                # Try to find h1 tag
                elif '<h1 class="title">' in content:
                    start = content.find('<h1 class="title">') + 18
                    end = content.find('</h1>', start)
                    return content[start:end].strip()
                else:
                    return "未知标题"
        except Exception:
            return "读取失败"

    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    async def create_named_announcement(self, filename: str, content_data: Dict, 
                                      overwrite: bool = False) -> Dict:
        """Create announcement with custom filename"""
        if not filename.endswith('.html'):
            filename += '.html'
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Check if file exists
        if os.path.exists(filepath) and not overwrite:
            return {
                'success': False,
                'message': f'文件 {filename} 已存在，请选择覆盖或使用不同的文件名'
            }
        
        try:
            # Generate HTML content based on type
            if content_data.get('type') == 'batch':
                html_content = self._create_batch_html_template(content_data.get('items', []))
            else:
                html_content = self._create_html_template(content_data)
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                'success': True,
                'message': f'成功{"覆盖" if overwrite and os.path.exists(filepath) else "创建"}文件 {filename}',
                'filename': filename,
                'filepath': filepath,
                'size': len(html_content.encode('utf-8'))
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'创建文件失败: {str(e)}'
            }

    async def delete_announcement(self, filename: str) -> Dict:
        """Delete announcement file"""
        if not filename.endswith('.html'):
            filename += '.html'
        
        filepath = os.path.join(self.output_dir, filename)
        
        if not os.path.exists(filepath):
            return {
                'success': False,
                'message': f'文件 {filename} 不存在'
            }
        
        try:
            os.remove(filepath)
            return {
                'success': True,
                'message': f'成功删除文件 {filename}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'删除文件失败: {str(e)}'
            }

    async def get_announcement_content(self, filename: str) -> Dict:
        """Get content of specific announcement file"""
        if not filename.endswith('.html'):
            filename += '.html'
        
        filepath = os.path.join(self.output_dir, filename)
        
        if not os.path.exists(filepath):
            return {
                'success': False,
                'message': f'文件 {filename} 不存在'
            }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'success': True,
                'filename': filename,
                'content': content,
                'size': len(content.encode('utf-8'))
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'读取文件失败: {str(e)}'
            }

    async def copy_announcement(self, source_filename: str, target_filename: str) -> Dict:
        """Copy announcement file with new name"""
        if not source_filename.endswith('.html'):
            source_filename += '.html'
        if not target_filename.endswith('.html'):
            target_filename += '.html'
        
        source_path = os.path.join(self.output_dir, source_filename)
        target_path = os.path.join(self.output_dir, target_filename)
        
        if not os.path.exists(source_path):
            return {
                'success': False,
                'message': f'源文件 {source_filename} 不存在'
            }
        
        if os.path.exists(target_path):
            return {
                'success': False,
                'message': f'目标文件 {target_filename} 已存在'
            }
        
        try:
            import shutil
            shutil.copy2(source_path, target_path)
            return {
                'success': True,
                'message': f'成功复制文件 {source_filename} 到 {target_filename}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'复制文件失败: {str(e)}'
            }

    async def batch_delete_announcements(self, filenames: List[str]) -> Dict:
        """Delete multiple announcement files"""
        results = []
        success_count = 0
        
        for filename in filenames:
            result = await self.delete_announcement(filename)
            results.append({
                'filename': filename,
                'success': result['success'],
                'message': result['message']
            })
            if result['success']:
                success_count += 1
        
        return {
            'success': success_count > 0,
            'message': f'成功删除 {success_count} 个文件，共 {len(filenames)} 个文件',
            'results': results,
            'success_count': success_count,
            'total_count': len(filenames)
        } 