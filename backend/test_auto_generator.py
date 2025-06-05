#!/usr/bin/env python3
"""
测试自动生成功能
"""

import asyncio
import sys
import os

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.auto_generator import AutoGenerator

async def test_auto_generator():
    """测试自动生成器功能"""
    print("🤖 测试自动生成器功能...")
    
    # 创建自动生成器实例
    auto_gen = AutoGenerator()
    
    # 测试获取统计信息
    print("\n📊 获取统计信息...")
    stats = await auto_gen.get_stats()
    print(f"统计信息: {stats}")
    
    # 测试自动生成
    print("\n🚀 测试自动生成...")
    result = await auto_gen.auto_generate_from_crawler()
    print(f"生成结果: {result}")
    
    # 再次获取统计信息
    print("\n📊 生成后的统计信息...")
    stats_after = await auto_gen.get_stats()
    print(f"更新后统计: {stats_after}")
    
    print("\n✅ 测试完成！")

if __name__ == "__main__":
    asyncio.run(test_auto_generator()) 