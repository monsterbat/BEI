#!/usr/bin/env python3
"""
Blue Edge Index Analyzer 快速啟動器
簡化的啟動方式，自動處理環境設定
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """快速啟動Blue Edge Analyzer"""
    print("🚀 Blue Edge Index Analyzer 快速啟動器")
    print("=" * 50)
    
    # 檢查虛擬環境
    project_root = Path(__file__).parent
    venv_path = project_root / "venv"
    
    if not venv_path.exists():
        print("❌ 未找到虛擬環境")
        print("請先執行環境設定：")
        print("  macOS:   python scripts/setup_env.py")
        print("  Windows: scripts\\setup_windows.bat")
        print("  Linux:   ./scripts/setup_linux.sh")
        return
    
    # 啟動主程式
    if os.name == 'nt':  # Windows
        python_exe = venv_path / "Scripts" / "python"
    else:  # macOS/Linux
        python_exe = venv_path / "bin" / "python"
    
    main_script = project_root / "main.py"
    
    print("✅ 啟動 Blue Edge Index Analyzer...")
    try:
        subprocess.run([str(python_exe), str(main_script)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 啟動失敗: {e}")
    except KeyboardInterrupt:
        print("\n👋 程式已關閉")

if __name__ == "__main__":
    main()
