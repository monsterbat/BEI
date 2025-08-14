"""
Excel和CSV文件處理模組
負責讀取、解析和預處理Excel和CSV數據
"""

import pandas as pd
from typing import Tuple, Optional, List
import numpy as np
import os


class ExcelProcessor:
    """Excel和CSV文件處理器"""
    
    def __init__(self):
        self.data = None
        self.file_path = None
        self.file_type = None  # 'excel' 或 'csv'
        self.available_sheets = []  # 可用的工作表清單
    
    def load_file(self, file_path: str, sheet_name: Optional[str] = None) -> bool:
        """
        載入Excel或CSV文件
        
        Args:
            file_path: 文件路徑
            sheet_name: 工作表名稱（僅適用於Excel），預設為None（第一個工作表）
            
        Returns:
            bool: 載入是否成功
        """
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.xlsx', '.xls']:
                self.file_type = 'excel'
                # 先取得所有工作表名稱
                excel_file = pd.ExcelFile(file_path)
                self.available_sheets = excel_file.sheet_names
                
                # 載入指定的工作表
                if sheet_name is None:
                    sheet_name = self.available_sheets[0]  # 預設第一個工作表
                
                self.data = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                
            elif file_ext == '.csv':
                self.file_type = 'csv'
                self.available_sheets = ['CSV資料']  # CSV只有一個"工作表"
                self.data = pd.read_csv(file_path, encoding='utf-8', header=None)
                
            else:
                print(f"不支援的檔案格式: {file_ext}")
                return False
            
            self.file_path = file_path
            return True
            
        except UnicodeDecodeError:
            # 嘗試其他編碼
            try:
                if self.file_type == 'csv':
                    self.data = pd.read_csv(file_path, encoding='big5', header=None)
                    return True
            except Exception as e:
                print(f"載入檔案失敗（編碼錯誤）: {e}")
                return False
        except Exception as e:
            print(f"載入檔案失敗: {e}")
            return False
    
    def get_available_sheets(self) -> List[str]:
        """
        取得可用的工作表清單
        
        Returns:
            List[str]: 工作表名稱清單
        """
        return self.available_sheets.copy()
    
    def get_file_type(self) -> Optional[str]:
        """
        取得檔案類型
        
        Returns:
            Optional[str]: 檔案類型 ('excel' 或 'csv')
        """
        return self.file_type
    
    def detect_data_start_row(self, column_index: int = 0) -> int:
        """
        自動偵測數值數據開始的行數
        
        Args:
            column_index: 要檢查的列索引
            
        Returns:
            int: 數據開始的行數
        """
        if self.data is None:
            return 0
        
        # 尋找第一個數值（非文字標題）的行
        for i in range(len(self.data)):
            # 檢查這一行是否包含數值數據
            row_data = self.data.iloc[i]
            numeric_count = 0
            total_non_nan = 0
            
            for val in row_data:
                if pd.notna(val):
                    total_non_nan += 1
                    # 嘗試轉換為數字
                    try:
                        float(val)
                        numeric_count += 1
                    except (ValueError, TypeError):
                        pass
            
            # 如果這一行有數值數據，且數值佔非空值的比例超過50%
            if total_non_nan > 0 and numeric_count / total_non_nan > 0.5 and numeric_count >= 1:
                return i
        
        return 0
    
    def detect_data_end_row(self, start_row: int = 0) -> int:
        """
        自動偵測數值數據結束的行數
        
        Args:
            start_row: 開始搜尋的行數
            
        Returns:
            int: 數據結束的行數
        """
        if self.data is None:
            return len(self.data) if self.data is not None else 0
        
        # 從start_row開始往下搜尋
        for i in range(start_row, len(self.data)):
            # 檢查這一行是否包含數值數據
            row_data = self.data.iloc[i]
            numeric_count = 0
            total_non_nan = 0
            
            for val in row_data:
                if pd.notna(val):
                    total_non_nan += 1
                    # 嘗試轉換為數字
                    try:
                        float(val)
                        numeric_count += 1
                    except (ValueError, TypeError):
                        pass
            
            # 如果這一行沒有數值數據，或數值佔比太低，認為數據結束
            if total_non_nan == 0 or (total_non_nan > 0 and numeric_count / total_non_nan < 0.5):
                return i  # 返回第一個非數據行的索引
        
        # 如果沒有找到結束行，返回最後一行
        return len(self.data)
    
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
            'file_path': self.file_path,
            'file_type': self.file_type,
            'available_sheets': self.available_sheets
        }
    
    def get_preview_data(self, start_row: int = 0, end_row: Optional[int] = None, max_rows: int = 20, max_cols: int = 10) -> dict:
        """
        取得數據預覽
        
        Args:
            start_row: 開始行數
            end_row: 結束行數，預設為None（到最後一行）
            max_rows: 最大顯示行數
            max_cols: 最大顯示列數
            
        Returns:
            dict: 包含預覽數據的字典
        """
        if self.data is None:
            return {}
        
        if end_row is None:
            end_row = len(self.data)
        
        # 限制預覽範圍
        preview_end_row = min(start_row + max_rows, end_row, len(self.data))
        preview_data = self.data.iloc[start_row:preview_end_row]
        
        # 限制列數
        if preview_data.shape[1] > max_cols:
            preview_data = preview_data.iloc[:, :max_cols]
            truncated_cols = True
        else:
            truncated_cols = False
        
        # 取得矩陣資料
        matrix_data = self.get_matrix_data(start_row=start_row, end_row=end_row)
        
        # 取得中間列資料
        middle_column_data = None
        middle_col_index = None
        if matrix_data.size > 0:
            middle_col_index = matrix_data.shape[1] // 2
            middle_column_data = self.get_middle_column_data(matrix_data)
        
        return {
            'preview_dataframe': preview_data,
            'matrix_shape': matrix_data.shape if matrix_data.size > 0 else (0, 0),
            'middle_column_index': middle_col_index,
            'middle_column_data': middle_column_data[:max_rows] if middle_column_data is not None else None,
            'start_row': start_row,
            'end_row': min(end_row, len(self.data)),
            'total_rows': len(self.data),
            'truncated_cols': truncated_cols,
            'actual_cols': self.data.shape[1]
        }
    
    def get_end_preview_data(self, end_row: int, max_rows: int = 10, max_cols: int = 10) -> dict:
        """
        取得結束行數附近的數據預覽
        
        Args:
            end_row: 結束行數
            max_rows: 最大顯示行數
            max_cols: 最大顯示列數
            
        Returns:
            dict: 包含預覽數據的字典
        """
        if self.data is None:
            return {}
        
        # 計算預覽範圍（從結束行往前取max_rows行）
        preview_start_row = max(0, end_row - max_rows)
        preview_end_row = min(end_row, len(self.data))
        
        preview_data = self.data.iloc[preview_start_row:preview_end_row]
        
        # 限制列數
        if preview_data.shape[1] > max_cols:
            preview_data = preview_data.iloc[:, :max_cols]
            truncated_cols = True
        else:
            truncated_cols = False
        
        # 取得矩陣資料
        matrix_data = self.get_matrix_data(start_row=preview_start_row, end_row=preview_end_row)
        
        # 取得中間列資料
        middle_column_data = None
        middle_col_index = None
        if matrix_data.size > 0:
            middle_col_index = matrix_data.shape[1] // 2
            middle_column_data = self.get_middle_column_data(matrix_data)
        
        return {
            'preview_dataframe': preview_data,
            'matrix_shape': matrix_data.shape if matrix_data.size > 0 else (0, 0),
            'middle_column_index': middle_col_index,
            'middle_column_data': middle_column_data[:max_rows] if middle_column_data is not None else None,
            'preview_start_row': preview_start_row,
            'preview_end_row': preview_end_row,
            'end_row': end_row,
            'total_rows': len(self.data),
            'truncated_cols': truncated_cols,
            'actual_cols': self.data.shape[1]
        }
