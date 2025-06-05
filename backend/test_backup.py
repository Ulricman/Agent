#!/usr/bin/env python3
"""
备份功能测试脚本
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:8000"

def test_backup_status():
    """测试备份状态获取"""
    print("🔍 测试备份状态获取...")
    try:
        response = requests.get(f"{BASE_URL}/api/backup/status")
        result = response.json()
        print(f"状态码: {result['code']}")
        if result['code'] == 200:
            data = result['data']
            print(f"数据文件数量: {len(data.get('data_files', {}))}")
            print(f"HTML文件数量: {data.get('html_files_count', 0)}")
            print(f"备份数量: {data.get('backups_count', 0)}")
            print(f"系统总大小: {data.get('total_size_human', '0 B')}")
            print("✅ 备份状态获取成功")
        else:
            print(f"❌ 备份状态获取失败: {result['message']}")
        return result['code'] == 200
    except Exception as e:
        print(f"❌ 备份状态获取异常: {e}")
        return False

def test_backup_list():
    """测试备份列表获取"""
    print("\n📋 测试备份列表获取...")
    try:
        response = requests.get(f"{BASE_URL}/api/backup/list")
        result = response.json()
        print(f"状态码: {result['code']}")
        if result['code'] == 200:
            backups = result['data']
            print(f"备份数量: {len(backups)}")
            for backup in backups:
                print(f"  - {backup['name']} ({backup.get('zip_size_human', 'Unknown size')})")
            print("✅ 备份列表获取成功")
        else:
            print(f"❌ 备份列表获取失败: {result['message']}")
        return result['code'] == 200
    except Exception as e:
        print(f"❌ 备份列表获取异常: {e}")
        return False

def test_create_backup():
    """测试创建备份"""
    print("\n💾 测试创建备份...")
    try:
        backup_name = f"test_backup_{int(time.time())}"
        response = requests.post(f"{BASE_URL}/api/backup/create", 
                               json={"backup_name": backup_name})
        result = response.json()
        print(f"状态码: {result['code']}")
        if result['code'] == 200:
            backup_info = result['data']
            print(f"备份名称: {backup_info['name']}")
            print(f"备份大小: {backup_info.get('zip_size_human', 'Unknown')}")
            print(f"文件数量: {len(backup_info.get('backed_up_files', []))}")
            print("✅ 备份创建成功")
            return backup_info['name']
        else:
            print(f"❌ 备份创建失败: {result['message']}")
            return None
    except Exception as e:
        print(f"❌ 备份创建异常: {e}")
        return None

def test_restore_backup(backup_name):
    """测试恢复备份"""
    print(f"\n🔄 测试恢复备份: {backup_name}...")
    try:
        response = requests.post(f"{BASE_URL}/api/backup/restore", 
                               json={"backup_name": backup_name})
        result = response.json()
        print(f"状态码: {result['code']}")
        if result['code'] == 200:
            print(f"恢复的文件数: {len(result['data'].get('restored_files', []))}")
            print(f"恢复的HTML文件数: {result['data'].get('restored_html_count', 0)}")
            print("✅ 备份恢复成功")
        else:
            print(f"❌ 备份恢复失败: {result['message']}")
        return result['code'] == 200
    except Exception as e:
        print(f"❌ 备份恢复异常: {e}")
        return False

def test_delete_backup(backup_name):
    """测试删除备份"""
    print(f"\n🗑️ 测试删除备份: {backup_name}...")
    try:
        response = requests.delete(f"{BASE_URL}/api/backup/delete/{backup_name}")
        result = response.json()
        print(f"状态码: {result['code']}")
        if result['code'] == 200:
            print("✅ 备份删除成功")
        else:
            print(f"❌ 备份删除失败: {result['message']}")
        return result['code'] == 200
    except Exception as e:
        print(f"❌ 备份删除异常: {e}")
        return False

def test_system_reset():
    """测试系统重置（谨慎使用）"""
    print("\n⚠️ 测试系统重置...")
    print("注意：此操作将重置所有数据到默认状态！")
    confirm = input("确定要继续吗？(输入 'YES' 确认): ")
    
    if confirm != 'YES':
        print("❌ 用户取消了系统重置测试")
        return False
    
    try:
        response = requests.post(f"{BASE_URL}/api/backup/reset")
        result = response.json()
        print(f"状态码: {result['code']}")
        if result['code'] == 200:
            print(f"重置的文件数: {len(result['data'].get('reset_files', []))}")
            if result['data'].get('auto_backup'):
                print(f"自动备份: {result['data']['auto_backup']['name']}")
            print("✅ 系统重置成功")
        else:
            print(f"❌ 系统重置失败: {result['message']}")
        return result['code'] == 200
    except Exception as e:
        print(f"❌ 系统重置异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始备份功能测试")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code != 200:
            print("❌ 后端服务器未运行，请先启动服务器")
            return
    except:
        print("❌ 无法连接到后端服务器，请确保服务器在 http://localhost:8000 运行")
        return
    
    print("✅ 后端服务器连接成功")
    
    # 测试序列
    tests_passed = 0
    total_tests = 0
    
    # 1. 测试备份状态
    total_tests += 1
    if test_backup_status():
        tests_passed += 1
    
    # 2. 测试备份列表
    total_tests += 1
    if test_backup_list():
        tests_passed += 1
    
    # 3. 测试创建备份
    total_tests += 1
    backup_name = test_create_backup()
    if backup_name:
        tests_passed += 1
        
        # 4. 测试恢复备份
        total_tests += 1
        if test_restore_backup(backup_name):
            tests_passed += 1
        
        # 5. 测试删除备份
        total_tests += 1
        if test_delete_backup(backup_name):
            tests_passed += 1
    else:
        total_tests += 2  # 跳过恢复和删除测试
    
    # 6. 可选：测试系统重置
    print(f"\n📊 测试结果: {tests_passed}/{total_tests} 通过")
    
    if tests_passed == total_tests:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查日志")
    
    # 询问是否测试系统重置
    print("\n" + "=" * 50)
    test_reset = input("是否测试系统重置功能？(y/N): ").lower()
    if test_reset == 'y':
        if test_system_reset():
            print("✅ 系统重置测试完成")
        else:
            print("❌ 系统重置测试失败")

if __name__ == "__main__":
    main() 