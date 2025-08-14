# 程式打包工具

本目錄包含將Python程式打包成執行檔的工具。

## 📋 檔案說明

- **`build.py`**: 自動打包主程式
- **`build_config.py`**: 打包設定和配置生成器

## 🚀 使用方法

### 自動打包
```bash
cd build_tools
python build.py --clean
```

### 手動設定
```bash
# 生成配置檔案
python build_config.py

# 使用 PyInstaller
pyinstaller BlueEdgeAnalyzer.spec

# 使用 cx_Freeze  
python setup_cx_freeze.py build
```

## 📦 輸出結果

打包完成後，執行檔會放在 `dist/` 目錄中：
- Windows: `BlueEdgeAnalyzer.exe`
- macOS/Linux: `BlueEdgeAnalyzer`
