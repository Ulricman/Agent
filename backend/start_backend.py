#!/usr/bin/env python3
"""
Tax Knowledge Management Backend Startup Script
启动税务知识管理后端服务器
"""

import os
import sys
import asyncio
import uvicorn
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from modules.html_generator import HTMLGenerator
from modules.logger import StructuredLogger

async def initialize_backend():
    """Initialize backend components"""
    logger = StructuredLogger()
    
    try:
        # Create necessary directories
        directories = [
            "data",
            "data/announcements", 
            "data/backups",
            "data/backups/knowledge",
            "data/backups/qa",
            "data/versions",
            "templates",
            "static"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
        # Generate initial sample HTML files
        html_gen = HTMLGenerator()
        await html_gen.create_sample_files()
        
        logger.log_info("Backend initialization completed successfully")
        print("✅ 后端初始化完成")
        
    except Exception as e:
        logger.log_error(f"Backend initialization failed: {str(e)}")
        print(f"❌ 后端初始化失败: {str(e)}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🚀 启动税务知识管理后端服务器...")
    print("📍 Tax Knowledge Management Backend Server Starting...")
    
    # Initialize backend
    asyncio.run(initialize_backend())
    
    # Configuration
    host = "0.0.0.0"
    port = 8000
    
    print(f"\n🌐 服务器将在以下地址启动:")
    print(f"   - 本地访问: http://localhost:{port}")
    print(f"   - 网络访问: http://{host}:{port}")
    print(f"   - 管理界面: http://localhost:{port}")
    print(f"   - API文档: http://localhost:{port}/docs")
    print(f"\n💡 使用 Ctrl+C 停止服务器\n")
    
    # Start the server
    try:
        uvicorn.run(
            "app:app",
            host=host,
            port=port,
            reload=True,  # Enable auto-reload for development
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 