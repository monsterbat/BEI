"""
Excel文件處理模組
負責讀取、解析和預處理Excel數據
"""

import pandas as pd
from typing import Tuple, Optional, List
import numpy as np


class ExcelProcessor:
    """Excel文件處理器"""
    
    def __init__(self):
        self.data = None
        self.file_path = None
    
    def load_excel(self, file_path: str, sheet_name: Optional[str] = None) -> bool:
        """
        載入Excel文件
        
        Args:
            file_path: Excel文件路徑
            sheet_name: 工作表名稱，預設為None（第一個工作表）
            
        Returns:
            bool: 載入是否成功
        """
        try:
            self.data = pd.read_excel(file_path, sheet_name=sheet_name)
            self.file_path = file_path
            return True
        except Exception as e:
            print(f"載入Excel文件失敗: {e}")
            return False
    
    def detect_data_start_row(self, column_index: int = 0) -> int:
        """
        自動偵測數據開始的行數
        
        Args:
            column_index: 要檢查的列索引
            
        Returns:
            int: 數據開始的行數
        """
        if self.data is None:
            return 0
        
        # 尋找第一個非空值的行
        for i, value in enumerate(self.data.iloc[:, column_index]):
            if pd.notna(value) and str(value).strip():
                return i
        return 0
    
    def get_matrix_data(self, start_row: int = 0, end_row: Optional[int] = None) -> np.ndarray:
        """
        取得矩陣數據
        
        Args:
            start_row: 開始行數
            end_row: 結束行數，預設為None（到最後一行）
            
        Returns:
            numpy.ndarray: 矩陣數據
        """
        if self.data is None:
            return np.array([])
        
        if end_row is None:
            end_row = len(self.data)
        
        return self.data.iloc[start_row:end_row].values
    
    def get_middle_column_data(self, matrix: np.ndarray) -> np.ndarray:
        """
        取得矩陣中間列的數據
        
        Args:
            matrix: 輸入矩陣
            
        Returns:
            numpy.ndarray: 中間列的數據
        """
        if matrix.size == 0:
            return np.array([])
        
        middle_col_index = matrix.shape[1] // 2
        return matrix[:, middle_col_index]
    
    def get_data_info(self) -> dict:
        """
        取得數據基本資訊
        
        Returns:
            dict: 包含數據形狀、列名等資訊
        """
        if self.data is None:
            return {}
        
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': dict(self.data.dtypes),
            'has_null': self.data.isnull().any().any(),
            'file_path': self.file_path
        }
