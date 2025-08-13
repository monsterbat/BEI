#!/usr/bin/env python3
"""
Blue Edge Index Analyzer 主程式
執行此檔案來啟動應用程式
"""

import sys
import os

# 將專案根目錄添加到Python路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blue_edge_analyzer.gui.main_window import run_application

if __name__ == "__main__":
    run_application()
