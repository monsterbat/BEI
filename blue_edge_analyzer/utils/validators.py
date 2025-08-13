"""
資料驗證工具
"""

import os
import pandas as pd
from typing import Optional, List


def validate_excel_file(file_path: str) -> tuple[bool, str]:
    """
    驗證Excel檔案
    
    Args:
        file_path: Excel檔案路徑
        
    Returns:
        tuple[bool, str]: (是否有效, 錯誤訊息)
    """
    if not os.path.exists(file_path):
        return False, "檔案不存在"
    
    if not file_path.lower().endswith(('.xlsx', '.xls')):
        return False, "不是有效的Excel檔案格式"
    
    try:
        # 嘗試讀取檔案
        pd.read_excel(file_path, nrows=1)
        return True, ""
    except Exception as e:
        return False, f"無法讀取Excel檔案: {str(e)}"


def validate_numeric_data(data: List) -> tuple[bool, str]:
    """
    驗證數值資料
    
    Args:
        data: 要驗證的資料列表
        
    Returns:
        tuple[bool, str]: (是否有效, 錯誤訊息)
    """
    if not data:
        return False, "資料為空"
    
    try:
        # 嘗試轉換為數值
        numeric_data = pd.to_numeric(data, errors='coerce')
        valid_count = numeric_data.notna().sum()
        
        if valid_count == 0:
            return False, "沒有有效的數值資料"
        
        if valid_count < len(data) * 0.5:
            return False, f"有效數值資料比例過低 ({valid_count}/{len(data)})"
        
        return True, ""
    except Exception as e:
        return False, f"資料驗證失敗: {str(e)}"


def validate_parameters(start_row: int, threshold_percent: float) -> tuple[bool, str]:
    """
    驗證計算參數
    
    Args:
        start_row: 開始行數
        threshold_percent: 閾值百分比
        
    Returns:
        tuple[bool, str]: (是否有效, 錯誤訊息)
    """
    if start_row < 0:
        return False, "開始行數不能為負數"
    
    if not (0 < threshold_percent <= 100):
        return False, "閾值百分比必須在1-100之間"
    
    return True, ""
