# 安裝和開發腳本

本目錄包含專案的安裝腳本和開發工具。

## 📋 檔案說明

- **`setup_env.py`**: macOS 環境自動設定腳本
- **`setup_windows.bat`**: Windows 環境設定腳本
- **`setup_linux.sh`**: Linux 環境設定腳本
- **`Makefile`**: 開發工具快速命令

## 🚀 使用方法

### 初次安裝
```bash
# macOS
python scripts/setup_env.py

# Windows
scripts\setup_windows.bat

# Linux
chmod +x scripts/setup_linux.sh
./scripts/setup_linux.sh
```

### 開發工具
```bash
# 使用 Makefile 命令
make help     # 查看所有可用命令
make test     # 執行測試
make format   # 程式碼格式化
make lint     # 程式碼檢查
```
