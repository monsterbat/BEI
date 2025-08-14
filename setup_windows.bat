@echo off
REM Blue Edge Index Analyzer - Windows 環境設定腳本
REM 適用於 Windows 10/11

echo ========================================
echo Blue Edge Analyzer Windows 環境設定
echo ========================================

REM 檢查Python是否已安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未找到Python，請先安裝Python 3.8或以上版本
    echo 下載地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 顯示Python版本
echo 檢測到的Python版本:
python --version

REM 檢查Python版本是否符合要求
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 需要Python 3.8或以上版本
    pause
    exit /b 1
)

REM 建立虛擬環境
echo.
echo [步驟 1/4] 建立虛擬環境...
if not exist venv (
    python -m venv venv
    if errorlevel 1 (
        echo [錯誤] 虛擬環境建立失敗
        pause
        exit /b 1
    )
    echo ✓ 虛擬環境建立成功
) else (
    echo ✓ 虛擬環境已存在
)

REM 啟動虛擬環境並升級pip
echo.
echo [步驟 2/4] 升級pip...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [警告] pip升級失敗，繼續安裝...
)

REM 安裝依賴套件
echo.
echo [步驟 3/4] 安裝依賴套件...
pip install -r requirements.txt
if errorlevel 1 (
    echo [錯誤] 依賴套件安裝失敗
    pause
    exit /b 1
)

REM 測試tkinter
echo.
echo [步驟 4/4] 測試GUI支援...
python -c "import tkinter; print('✓ tkinter 支援正常')" 2>nul
if errorlevel 1 (
    echo [警告] tkinter 可能不可用，某些Windows版本需要重新安裝Python並勾選tkinter選項
)

echo.
echo ========================================
echo 🎉 環境設定完成！
echo ========================================
echo.
echo 使用方法:
echo 1. 啟動虛擬環境: venv\Scripts\activate.bat
echo 2. 執行程式: python main.py
echo 3. 退出虛擬環境: deactivate
echo.
echo 按任意鍵繼續...
pause >nul

