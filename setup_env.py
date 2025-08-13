#!/usr/bin/env python3
"""
環境設定腳本
自動建立虛擬環境並安裝依賴套件
"""

import subprocess
import sys
import os
from pathlib import Path


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


def setup_virtual_environment():
    """設定虛擬環境"""
    print("🚀 開始設定Blue Edge Analyzer開發環境")
    
    # 確認Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ 錯誤: 需要Python 3.8或以上版本")
        return False
    
    # 取得專案根目錄
    project_root = Path(__file__).parent
    venv_path = project_root / "venv"
    
    print(f"專案目錄: {project_root}")
    print(f"虛擬環境路徑: {venv_path}")
    
    # 建立虛擬環境
    if not venv_path.exists():
        print("\n📦 建立虛擬環境...")
        if not run_command(f"python -m venv {venv_path}", "建立虛擬環境"):
            return False
    else:
        print("\n✅ 虛擬環境已存在")
    
    # 確定啟動腳本路徑
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
        python_exe = venv_path / "Scripts" / "python"
        pip_exe = venv_path / "Scripts" / "pip"
    else:  # macOS/Linux
        activate_script = venv_path / "bin" / "activate"
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    # 升級pip
    print("\n🔄 升級pip...")
    if not run_command(f"{python_exe} -m pip install --upgrade pip", "升級pip"):
        return False
    
    # 安裝依賴套件
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        print("\n📚 安裝依賴套件...")
        if not run_command(f"{pip_exe} install -r {requirements_file}", "安裝requirements.txt"):
            return False
    
    # 安裝開發依賴 (可選)
    print("\n🛠️ 安裝開發工具...")
    dev_packages = ["pytest", "black", "flake8"]
    for package in dev_packages:
        run_command(f"{pip_exe} install {package}", f"安裝{package}")
    
    print("\n✅ 環境設定完成!")
    print("\n" + "="*60)
    print("🎉 Blue Edge Analyzer 開發環境設定完成!")
    print("="*60)
    
    print("\n📋 下一步:")
    if os.name == 'nt':
        print(f"1. 啟動虛擬環境: {venv_path}\\Scripts\\activate")
    else:
        print(f"1. 啟動虛擬環境: source {venv_path}/bin/activate")
    
    print("2. 執行應用程式: python main.py")
    print("3. 或執行測試: pytest")
    
    return True


def main():
    """主函式"""
    try:
        success = setup_virtual_environment()
        if not success:
            print("\n❌ 環境設定失敗")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 使用者中斷設定")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 未預期的錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
