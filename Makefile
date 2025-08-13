# Blue Edge Analyzer Makefile
# 提供常用的開發命令

.PHONY: help setup install run test lint format clean

# 預設目標
help:
	@echo "Blue Edge Analyzer 開發工具"
	@echo ""
	@echo "可用命令:"
	@echo "  setup    - 設定開發環境"
	@echo "  install  - 安裝依賴套件"
	@echo "  run      - 執行應用程式"
	@echo "  test     - 執行測試"
	@echo "  lint     - 程式碼檢查"
	@echo "  format   - 程式碼格式化"
	@echo "  clean    - 清理暫存檔案"

# 設定開發環境
setup:
	python setup_env.py

# 安裝依賴套件
install:
	pip install -r requirements.txt
	pip install -e ".[dev]"

# 執行應用程式
run:
	python main.py

# 執行測試
test:
	pytest tests/ -v

# 程式碼檢查
lint:
	flake8 blue_edge_analyzer/ main.py setup_env.py
	flake8 tests/

# 程式碼格式化
format:
	black blue_edge_analyzer/ main.py setup_env.py tests/

# 清理暫存檔案
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
