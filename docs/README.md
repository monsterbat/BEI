# 專案文件

本目錄包含專案的設定檔案和文件。

## 📋 檔案說明

- **`pyproject.toml`**: Python 專案設定檔（PEP 518標準）

## 📝 專案設定

`pyproject.toml` 包含：
- 專案metadata（名稱、版本、作者等）
- 依賴套件管理
- 建置工具設定
- 程式碼格式化設定（black）
- 程式碼檢查設定（flake8）

## 🔧 使用方式

這些設定檔案通常不需要手動編輯，它們會被開發工具自動使用：
- `pip install -e .` 會讀取 pyproject.toml
- `black .` 會使用其中的格式化設定
- `flake8 .` 會使用其中的檢查規則
