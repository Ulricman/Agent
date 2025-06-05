#!/usr/bin/env python3
"""
测试HTML管理API功能的脚本
用于验证所有HTML文件操作功能是否正常工作
"""

import asyncio
import json
import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api_endpoint(method, endpoint, data=None, params=None):
    """测试API端点"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n--- 测试 {method} {endpoint} ---")
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            print(f"不支持的HTTP方法: {method}")
            return None
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return result
        else:
            print(f"错误响应: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器。请确保后端已启动 (python start_backend.py)")
        return None
    except Exception as e:
        print(f"❌ 请求错误: {str(e)}")
        return None

def main():
    """主测试函数"""
    print("=" * 60)
    print("HTML文件管理API功能测试")
    print("=" * 60)
    
    # 测试1: 获取文件列表
    print("\n🔍 测试1: 获取HTML文件列表")
    files_result = test_api_endpoint("GET", "/html/files")
    
    # 测试2: 创建新文件
    print("\n📝 测试2: 创建新HTML文件")
    create_data = {
        "filename": f"test_announcement_{int(time.time())}",
        "title": "API测试公告",
        "content": "这是通过API创建的测试公告内容。\n\n包含多行文本和特殊字符：《》""''",
        "category": "API测试",
        "effective_date": datetime.now().strftime("%Y-%m-%d"),
        "announcement_id": f"API-TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "overwrite": True
    }
    
    create_result = test_api_endpoint("POST", "/html/create", data=create_data)
    created_filename = None
    if create_result and create_result.get("code") == 200:
        created_filename = create_result["data"]["filename"]
        print(f"✅ 成功创建文件: {created_filename}")
    
    # 测试3: 获取特定文件内容
    if created_filename:
        print(f"\n📄 测试3: 获取文件内容 ({created_filename})")
        content_result = test_api_endpoint("GET", f"/html/files/{created_filename}")
        
        if content_result and content_result.get("code") == 200:
            content_size = len(content_result["data"]["content"])
            print(f"✅ 成功获取文件内容，大小: {content_size} 字符")
    
    # 测试4: 复制文件
    if created_filename:
        print(f"\n📋 测试4: 复制文件")
        copy_data = {
            "target_filename": f"copied_{created_filename}"
        }
        copy_result = test_api_endpoint("POST", f"/html/files/{created_filename}/copy", data=copy_data)
        
        if copy_result and copy_result.get("code") == 200:
            print("✅ 文件复制成功")
    
    # 测试5: URL抓取模拟
    print("\n🕷️ 测试5: URL抓取模拟")
    crawl_data = {
        "url": "https://example.com/tax-policy-2024",
        "filename": f"crawled_test_{int(time.time())}",
        "overwrite": True
    }
    
    crawl_result = test_api_endpoint("POST", "/html/create-from-url", data=crawl_data)
    crawled_filename = None
    if crawl_result and crawl_result.get("code") == 200:
        crawled_filename = crawl_result["data"]["filename"]
        print(f"✅ URL抓取模拟成功: {crawled_filename}")
    
    # 测试6: 批量删除测试文件
    print("\n🗑️ 测试6: 批量删除测试文件")
    files_to_delete = []
    if created_filename:
        files_to_delete.append(created_filename)
        files_to_delete.append(f"copied_{created_filename}")
    if crawled_filename:
        files_to_delete.append(crawled_filename)
    
    if files_to_delete:
        batch_delete_data = {
            "filenames": files_to_delete
        }
        batch_result = test_api_endpoint("POST", "/html/batch-delete", data=batch_delete_data)
        
        if batch_result and batch_result.get("code") == 200:
            success_count = batch_result["data"]["success_count"]
            total_count = batch_result["data"]["total_count"]
            print(f"✅ 批量删除完成: {success_count}/{total_count} 个文件")
    
    # 测试7: 再次获取文件列表（验证删除效果）
    print("\n🔍 测试7: 验证删除效果 - 重新获取文件列表")
    final_files_result = test_api_endpoint("GET", "/html/files")
    
    if final_files_result and final_files_result.get("code") == 200:
        file_count = len(final_files_result["data"])
        print(f"✅ 当前HTML文件总数: {file_count}")
        
        if file_count > 0:
            print("📋 现有文件列表:")
            for i, file_info in enumerate(final_files_result["data"][:5], 1):  # 显示前5个文件
                print(f"  {i}. {file_info['filename']} - {file_info['title']} ({file_info['size_human']})")
            if file_count > 5:
                print(f"  ... 还有 {file_count - 5} 个文件")
    
    print("\n" + "=" * 60)
    print("✅ HTML文件管理API功能测试完成")
    print("=" * 60)
    
    # 显示API端点总结
    print("\n📋 已实现的API端点总结:")
    api_endpoints = [
        "GET    /html/files                    - 获取所有HTML文件列表",
        "POST   /html/create                   - 创建新HTML文件（支持自定义文件名）",
        "DELETE /html/files/{filename}         - 删除指定HTML文件",
        "GET    /html/files/{filename}         - 获取指定文件内容",
        "POST   /html/files/{filename}/copy    - 复制文件到新文件名",
        "POST   /html/batch-delete             - 批量删除多个文件",
        "POST   /html/create-from-url          - 模拟从URL抓取内容创建文件",
        "GET    /static/announcements/{filename} - 直接访问HTML文件",
        "GET    /html-manager                  - HTML文件管理界面"
    ]
    
    for endpoint in api_endpoints:
        print(f"  {endpoint}")
    
    print(f"\n🌐 访问HTML管理界面: {BASE_URL}/html-manager")

if __name__ == "__main__":
    main() 