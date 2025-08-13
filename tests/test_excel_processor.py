"""
Excel處理器測試
"""

import pytest
import numpy as np
import pandas as pd
from blue_edge_analyzer.core.excel_processor import ExcelProcessor


class TestExcelProcessor:
    """Excel處理器測試類別"""
    
    def setup_method(self):
        """設定測試環境"""
        self.processor = ExcelProcessor()
    
    def test_init(self):
        """測試初始化"""
        assert self.processor.data is None
        assert self.processor.file_path is None
    
    def test_get_middle_column_data(self):
        """測試取得中間列數據"""
        # 測試3x3矩陣
        matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        result = self.processor.get_middle_column_data(matrix)
        expected = np.array([2, 5, 8])  # 中間列 (索引1)
        np.testing.assert_array_equal(result, expected)
        
        # 測試4x4矩陣
        matrix = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
        result = self.processor.get_middle_column_data(matrix)
        expected = np.array([3, 7, 11, 15])  # 中間列 (索引2)
        np.testing.assert_array_equal(result, expected)
    
    def test_get_middle_column_data_empty(self):
        """測試空矩陣"""
        matrix = np.array([])
        result = self.processor.get_middle_column_data(matrix)
        assert result.size == 0
    
    def test_detect_data_start_row(self):
        """測試自動偵測數據開始行數"""
        # 建立測試數據
        test_data = pd.DataFrame({
            'A': ['', '', 1, 2, 3],
            'B': ['', '', 4, 5, 6]
        })
        self.processor.data = test_data
        
        # 測試偵測
        start_row = self.processor.detect_data_start_row(column_index=0)
        assert start_row == 2  # 第一個非空值在索引2
