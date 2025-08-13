#!/bin/bash
# Blue Edge Index Analyzer - Linux 環境設定腳本
# 適用於 Ubuntu/Debian/CentOS/Fedora

set -e  # 遇到錯誤時停止執行

echo "========================================"
echo "Blue Edge Analyzer Linux 環境設定"
echo "========================================"

# 檢測Linux發行版
if command -v apt-get &> /dev/null; then
    DISTRO="debian"
    PKG_MANAGER="apt-get"
    INSTALL_CMD="sudo apt-get install -y"
elif command -v yum &> /dev/null; then
    DISTRO="redhat"
    PKG_MANAGER="yum"
    INSTALL_CMD="sudo yum install -y"
elif command -v dnf &> /dev/null; then
    DISTRO="fedora"
    PKG_MANAGER="dnf"
    INSTALL_CMD="sudo dnf install -y"
else
    echo "[警告] 無法自動檢測Linux發行版，請手動安裝Python和tkinter"
    DISTRO="unknown"
fi

echo "檢測到的系統: $DISTRO"

# 檢查Python是否已安裝
if ! command -v python3 &> /dev/null; then
    echo "[步驟 1/5] 安裝Python..."
    case $DISTRO in
        "debian")
            sudo apt-get update
            $INSTALL_CMD python3 python3-pip python3-venv python3-tk
            ;;
        "redhat")
            $INSTALL_CMD python3 python3-pip python3-tkinter
            ;;
        "fedora")
            $INSTALL_CMD python3 python3-pip python3-tkinter
            ;;
        *)
            echo "[錯誤] 請手動安裝 python3, python3-pip, python3-venv, python3-tkinter"
            exit 1
            ;;
    esac
else
    echo "✓ Python已安裝: $(python3 --version)"
    
    # 檢查tkinter是否可用
    if ! python3 -c "import tkinter" &> /dev/null; then
        echo "[步驟 1/5] 安裝tkinter..."
        case $DISTRO in
            "debian")
                $INSTALL_CMD python3-tk
                ;;
            "redhat"|"fedora")
                $INSTALL_CMD python3-tkinter
                ;;
        esac
    else
        echo "✓ tkinter已可用"
    fi
fi

# 檢查Python版本
echo "[步驟 2/5] 檢查Python版本..."
python3 -c "import sys; assert sys.version_info >= (3, 8), 'Python 3.8+ required'"
echo "✓ Python版本符合要求"

# 建立虛擬環境
echo "[步驟 3/5] 建立虛擬環境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 虛擬環境建立成功"
else
    echo "✓ 虛擬環境已存在"
fi

# 啟動虛擬環境並安裝依賴
echo "[步驟 4/5] 安裝依賴套件..."
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "✓ 依賴套件安裝完成"

# 測試GUI
echo "[步驟 5/5] 測試GUI支援..."
if python -c "import tkinter; print('✓ tkinter 支援正常')" 2>/dev/null; then
    echo "✓ GUI測試通過"
else
    echo "[警告] tkinter 測試失敗，可能需要安裝額外的GUI套件"
    echo "Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "CentOS/RHEL: sudo yum install tkinter"
    echo "Fedora: sudo dnf install python3-tkinter"
fi

echo ""
echo "========================================"
echo "🎉 環境設定完成！"
echo "========================================"
echo ""
echo "使用方法:"
echo "1. 啟動虛擬環境: source venv/bin/activate"
echo "2. 執行程式: python main.py"
echo "3. 退出虛擬環境: deactivate"
echo ""
