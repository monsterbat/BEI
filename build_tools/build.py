#!/usr/bin/env python3
"""
Blue Edge Index Analyzer 自動打包腳本
支援多平台自動打包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse

PROJECT_ROOT = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"

def run_command(command, description=""):
    """執行命令並處理錯誤"""
    print(f"\n{'='*50}")
    print(f"執行: {description}")
    print(f"命令: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print("輸出:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"錯誤: {e}")
        if e.stderr:
            print(f"錯誤訊息: {e.stderr}")
        return False

def check_dependencies():
    """檢查打包工具是否已安裝"""
    print("檢查打包工具...")
    
    tools = {
        "pyinstaller": "pip install pyinstaller",
        "cx_freeze": "pip install cx_freeze"
    }
    
    available_tools = []
    for tool, install_cmd in tools.items():
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
            print(f"✓ {tool} 已安裝")
            available_tools.append(tool)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"✗ {tool} 未安裝，安裝命令: {install_cmd}")
    
    return available_tools

def clean_build():
    """清理建置目錄"""
    print("清理建置目錄...")
    
    dirs_to_clean = [DIST_DIR, BUILD_DIR, PROJECT_ROOT / "__pycache__"]
    
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"✓ 已清理: {dir_path}")

def build_with_pyinstaller():
    """使用 PyInstaller 打包"""
    print("\n使用 PyInstaller 打包...")
    
    # 生成配置檔案
    from build_config import generate_pyinstaller_spec
    spec_file = generate_pyinstaller_spec()
    
    # 執行打包
    if run_command(f"pyinstaller {spec_file}", "PyInstaller 打包"):
        print("✓ PyInstaller 打包成功")
        return True
    else:
        print("✗ PyInstaller 打包失敗")
        return False

def build_with_cx_freeze():
    """使用 cx_Freeze 打包"""
    print("\n使用 cx_Freeze 打包...")
    
    # 生成配置檔案
    from build_config import generate_cx_freeze_setup
    setup_file = generate_cx_freeze_setup()
    
    # 執行打包
    if run_command(f"python {setup_file} build", "cx_Freeze 打包"):
        print("✓ cx_Freeze 打包成功")
        return True
    else:
        print("✗ cx_Freeze 打包失敗")
        return False

def create_portable_package():
    """建立可攜式套件"""
    print("\n建立可攜式套件...")
    
    portable_dir = DIST_DIR / "BlueEdgeAnalyzer_Portable"
    portable_dir.mkdir(parents=True, exist_ok=True)
    
    # 複製必要檔案
    files_to_copy = [
        "main.py",
        "requirements.txt",
        "README.md",
        "blue_edge_analyzer/",
    ]
    
    for file_path in files_to_copy:
        src = PROJECT_ROOT / file_path
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, portable_dir / file_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src, portable_dir / file_path)
    
    # 建立啟動腳本
    if sys.platform == "win32":
        start_script = portable_dir / "start.bat"
        with open(start_script, 'w') as f:
            f.write("""@echo off
echo 啟動 Blue Edge Analyzer...
python main.py
pause
""")
    else:
        start_script = portable_dir / "start.sh"
        with open(start_script, 'w') as f:
            f.write("""#!/bin/bash
echo "啟動 Blue Edge Analyzer..."
python3 main.py
""")
        os.chmod(start_script, 0o755)
    
    print(f"✓ 可攜式套件已建立: {portable_dir}")

def main():
    parser = argparse.ArgumentParser(description="Blue Edge Analyzer 打包工具")
    parser.add_argument("--tool", choices=["pyinstaller", "cx_freeze", "portable", "all"], 
                       default="all", help="選擇打包工具")
    parser.add_argument("--clean", action="store_true", help="打包前清理建置目錄")
    
    args = parser.parse_args()
    
    print("🚀 Blue Edge Analyzer 自動打包工具")
    print("=" * 50)
    
    # 清理建置目錄
    if args.clean:
        clean_build()
    
    # 檢查依賴
    available_tools = check_dependencies()
    
    success_count = 0
    total_count = 0
    
    # 執行打包
    if args.tool == "all" or args.tool == "pyinstaller":
        if "pyinstaller" in available_tools:
            total_count += 1
            if build_with_pyinstaller():
                success_count += 1
        else:
            print("跳過 PyInstaller（未安裝）")
    
    if args.tool == "all" or args.tool == "cx_freeze":
        if "cx_freeze" in available_tools:
            total_count += 1
            if build_with_cx_freeze():
                success_count += 1
        else:
            print("跳過 cx_Freeze（未安裝）")
    
    if args.tool == "all" or args.tool == "portable":
        total_count += 1
        create_portable_package()
        success_count += 1
    
    # 結果統計
    print("\n" + "=" * 50)
    print("🎉 打包完成！")
    print(f"成功: {success_count}/{total_count}")
    
    if DIST_DIR.exists():
        print(f"\n打包結果位於: {DIST_DIR}")
        for item in DIST_DIR.iterdir():
            print(f"  - {item.name}")

if __name__ == "__main__":
    main()

