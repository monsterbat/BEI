"""
Blue Edge Index Analyzer 打包配置
支援 PyInstaller 和 cx_Freeze 打包
"""

import os
import sys
from pathlib import Path

# 專案資訊
PROJECT_NAME = "BlueEdgeAnalyzer"
VERSION = "1.0.0"
DESCRIPTION = "Blue Edge Index 數據分析工具"
AUTHOR = "Your Name"

# 檔案路徑
PROJECT_ROOT = Path(__file__).parent
MAIN_SCRIPT = PROJECT_ROOT / "main.py"
ICON_FILE = PROJECT_ROOT / "assets" / "icon.ico"  # 如果有圖示檔案

# PyInstaller 配置
PYINSTALLER_CONFIG = {
    "name": PROJECT_NAME,
    "script": str(MAIN_SCRIPT),
    "onefile": True,  # 打包成單一執行檔
    "windowed": True,  # Windows下隱藏控制台視窗
    "icon": str(ICON_FILE) if ICON_FILE.exists() else None,
    "add_data": [
        # 如果需要包含額外檔案，在這裡添加
        # ("source_path", "dest_path"),
    ],
    "hidden_imports": [
        # 可能需要的隱藏導入
        "tkinter",
        "tkinter.ttk",
        "tkinter.filedialog",
        "tkinter.messagebox",
        "pandas",
        "numpy",
        "openpyxl",
    ],
    "exclude_modules": [
        # 排除不需要的模組以減少檔案大小
        "matplotlib",
        "scipy",
        "IPython",
        "jupyter",
    ],
}

# cx_Freeze 配置
CX_FREEZE_CONFIG = {
    "name": PROJECT_NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "author": AUTHOR,
    "executables": [
        {
            "script": str(MAIN_SCRIPT),
            "base": "Win32GUI" if sys.platform == "win32" else None,
            "icon": str(ICON_FILE) if ICON_FILE.exists() else None,
            "target_name": f"{PROJECT_NAME}.exe" if sys.platform == "win32" else PROJECT_NAME,
        }
    ],
    "options": {
        "build_exe": {
            "packages": ["tkinter", "pandas", "numpy", "openpyxl"],
            "excludes": ["matplotlib", "scipy", "IPython", "jupyter"],
            "include_files": [],  # 額外檔案
        }
    },
}


def generate_pyinstaller_spec():
    """生成 PyInstaller 規格檔案"""
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{PYINSTALLER_CONFIG["script"]}'],
    pathex=[],
    binaries=[],
    datas={PYINSTALLER_CONFIG["add_data"]},
    hiddenimports={PYINSTALLER_CONFIG["hidden_imports"]},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes={PYINSTALLER_CONFIG["exclude_modules"]},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{PYINSTALLER_CONFIG["name"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {'icon="' + str(ICON_FILE) + '",' if ICON_FILE.exists() else ''}
)
'''
    
    spec_file = PROJECT_ROOT / f"{PROJECT_NAME}.spec"
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print(f"PyInstaller 規格檔案已生成: {spec_file}")
    return spec_file


def generate_cx_freeze_setup():
    """生成 cx_Freeze setup.py 檔案"""
    setup_content = f'''
import sys
from cx_Freeze import setup, Executable

# 依賴套件
packages = ["tkinter", "pandas", "numpy", "openpyxl"]
excludes = ["matplotlib", "scipy", "IPython", "jupyter"]

# 執行檔設定
executables = [
    Executable(
        "{MAIN_SCRIPT}",
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="{CX_FREEZE_CONFIG['executables'][0]['target_name']}",
        {'icon="' + str(ICON_FILE) + '"' if ICON_FILE.exists() else '# icon=None'}
    )
]

# 打包設定
setup(
    name="{CX_FREEZE_CONFIG['name']}",
    version="{CX_FREEZE_CONFIG['version']}",
    description="{CX_FREEZE_CONFIG['description']}",
    author="{CX_FREEZE_CONFIG['author']}",
    options={{
        "build_exe": {{
            "packages": packages,
            "excludes": excludes,
            "include_files": [],
        }}
    }},
    executables=executables,
)
'''
    
    setup_file = PROJECT_ROOT / "setup_cx_freeze.py"
    with open(setup_file, 'w', encoding='utf-8') as f:
        f.write(setup_content.strip())
    
    print(f"cx_Freeze setup.py 已生成: {setup_file}")
    return setup_file


if __name__ == "__main__":
    print("Blue Edge Analyzer 打包配置工具")
    print("=" * 40)
    
    # 生成配置檔案
    generate_pyinstaller_spec()
    generate_cx_freeze_setup()
    
    print("\n打包命令:")
    print("PyInstaller: pyinstaller BlueEdgeAnalyzer.spec")
    print("cx_Freeze:   python setup_cx_freeze.py build")
