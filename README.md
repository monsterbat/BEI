# Blue Edge Index Analyzer

一個專業的Python應用程式，用於分析Excel數據並計算Blue Edge Index。

## 📋 功能特色

- 🔍 **Excel檔案處理**: 支援讀取和解析Excel檔案(.xlsx, .xls)
- 🎯 **自動數據偵測**: 智能偵測數據開始位置
- 📊 **Blue Edge Index計算**: 實現專業的Blue Edge Index演算法
- 🖥️ **直觀GUI介面**: 使用tkinter建立的使用者友善介面
- 📋 **結果複製功能**: 輕鬆複製計算結果到剪貼簿
- ⚙️ **參數可調整**: 支援自定義計算參數

## 🏗️ 專案架構

```
Blue_edge_index/
├── blue_edge_analyzer/          # 主要應用程式套件
│   ├── __init__.py
│   ├── core/                    # 核心功能模組
│   │   ├── __init__.py
│   │   ├── excel_processor.py   # Excel檔案處理
│   │   └── blue_edge_calculator.py # Blue Edge Index計算
│   ├── gui/                     # 使用者介面
│   │   ├── __init__.py
│   │   └── main_window.py       # 主視窗
│   └── utils/                   # 工具模組
│       ├── __init__.py
│       └── validators.py        # 資料驗證工具
├── main.py                      # 應用程式入口點
├── requirements.txt             # Python依賴套件
├── pyproject.toml              # 專案設定檔
├── setup_env.py                # 環境設定腳本
└── README.md                   # 專案說明文件
```

## 🚀 快速開始

### 系統需求

- Python 3.8 或以上版本
- 作業系統: Windows, macOS, Linux

### 自動安裝 (推薦)

1. **複製專案到本機**
   ```bash
   cd /path/to/your/project
   ```

2. **執行自動環境設定**
   ```bash
   python setup_env.py
   ```

3. **啟動虛擬環境**
   ```bash
   # macOS/Linux
   source venv/bin/activate
   
   # Windows
   venv\\Scripts\\activate
   ```

4. **執行應用程式**
   ```bash
   python main.py
   ```

### 手動安裝

1. **建立虛擬環境**
   ```bash
   python -m venv venv
   ```

2. **啟動虛擬環境**
   ```bash
   # macOS/Linux
   source venv/bin/activate
   
   # Windows
   venv\\Scripts\\activate
   ```

3. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

4. **執行應用程式**
   ```bash
   python main.py
   ```

## 📖 使用說明

### 基本操作流程

1. **啟動應用程式**
   - 執行 `python main.py` 開啟GUI介面

2. **選擇Excel檔案**
   - 點擊「選擇Excel檔案」按鈕
   - 選擇要分析的Excel檔案

3. **設定參數**
   - **資料開始行數**: 指定數據開始的行數（可使用自動偵測）
   - **前N%閾值**: 設定計算時使用的百分比閾值

4. **執行計算**
   - 點擊「開始計算 Blue Edge Index」
   - 系統會自動計算並顯示結果

5. **查看結果**
   - 結果會顯示在下方的文字區域
   - 包含詳細的計算資訊和判斷結果

6. **複製結果**
   - 點擊「複製結果」將結果複製到剪貼簿

### 進階功能

- **自動偵測**: 系統可以自動偵測數據開始位置
- **參數調整**: 可以調整閾值百分比來改變計算方式
- **結果分析**: 提供詳細的計算過程和統計資訊

## 🔧 開發指南

### 開發環境設定

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 程式碼格式化
black .

# 程式碼檢查
flake8 .

# 執行測試
pytest
```

### 專案結構說明

- **`blue_edge_analyzer/core/`**: 核心業務邏輯
  - `excel_processor.py`: Excel檔案讀取和處理
  - `blue_edge_calculator.py`: Blue Edge Index計算演算法

- **`blue_edge_analyzer/gui/`**: 使用者介面
  - `main_window.py`: 主視窗GUI實現

- **`blue_edge_analyzer/utils/`**: 輔助工具
  - `validators.py`: 資料驗證和檢查工具

### 擴展功能

如果需要擴展功能，建議：

1. 在對應的模組中添加新功能
2. 保持模組化設計原則
3. 添加適當的錯誤處理
4. 撰寫相應的測試

## 📊 Blue Edge Index 計算說明

Blue Edge Index 是一個用於分析數據分佈特性的指標：

1. **數據預處理**: 從Excel中提取矩陣數據的中間列
2. **閾值計算**: 取前N%的數據點
3. **指標計算**: 比較前N%數據與整體數據的關係
4. **結果判斷**: 根據計算結果判斷Pass/NG

## 🐛 故障排除

### 常見問題

1. **無法讀取Excel檔案**
   - 確認檔案格式為.xlsx或.xls
   - 檢查檔案是否損壞
   - 確認檔案沒有被其他程式開啟

2. **計算結果異常**
   - 檢查數據開始行數設定
   - 確認數據中包含有效的數值
   - 調整閾值百分比設定

3. **GUI介面問題**
   - 確認tkinter已正確安裝（通常隨Python一起安裝）
   - 在某些Linux發行版中可能需要額外安裝tkinter

### 取得幫助

如果遇到問題，請檢查：
1. Python版本是否符合需求
2. 所有依賴套件是否正確安裝
3. Excel檔案格式是否正確

## 📝 版本歷史

- **v1.0.0** (當前版本)
  - 初始版本發布
  - 基本Excel處理功能
  - Blue Edge Index計算
  - GUI使用者介面

## 📄 授權條款

本專案採用 MIT 授權條款。

## 👥 貢獻指南

歡迎提交Issues和Pull Requests來改善這個專案！

---

**注意**: 這是一個專業的數據分析工具，請確保您了解Blue Edge Index的計算原理後再使用。
