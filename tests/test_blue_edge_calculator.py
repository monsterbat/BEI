"""
Blue Edge Index計算器測試
"""

import pytest
import numpy as np
from blue_edge_analyzer.core.blue_edge_calculator import BlueEdgeCalculator


class TestBlueEdgeCalculator:
    """Blue Edge Index計算器測試類別"""
    
    def setup_method(self):
        """設定測試環境"""
        self.calculator = BlueEdgeCalculator()
    
    def test_init(self):
        """測試初始化"""
        assert self.calculator.threshold_percentage == 0.1
    
    def test_set_threshold_percentage(self):
        """測試設定閾值百分比"""
        self.calculator.set_threshold_percentage(0.2)
        assert self.calculator.threshold_percentage == 0.2
        
        # 測試無效值
        self.calculator.set_threshold_percentage(0.0)  # 無效
        assert self.calculator.threshold_percentage == 0.2  # 不變
        
        self.calculator.set_threshold_percentage(1.5)  # 無效
        assert self.calculator.threshold_percentage == 0.2  # 不變
    
    def test_calculate_blue_edge_index_basic(self):
        """測試基本Blue Edge Index計算"""
        # 測試遞增數據
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result, judgment = self.calculator.calculate_blue_edge_index(data)
        
        assert isinstance(result, float)
        assert judgment in ['Pass', 'NG']
        assert result > 0
    
    def test_calculate_blue_edge_index_empty(self):
        """測試空數據"""
        data = np.array([])
        result, judgment = self.calculator.calculate_blue_edge_index(data)
        
        assert result == 0.0
        assert judgment == 'NG'
    
    def test_get_calculation_details(self):
        """測試取得計算詳細資訊"""
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        details = self.calculator.get_calculation_details(data)
        
        assert 'total_data_points' in details
        assert 'top_10_percent_points' in details
        assert 'top_10_percent_avg' in details
        assert 'overall_avg' in details
        assert 'data_range' in details
        assert 'threshold_percentage' in details
        
        assert details['total_data_points'] == 10
        assert details['top_10_percent_points'] == 1  # 10% of 10 = 1
        assert details['overall_avg'] == 5.5
        assert details['data_range'] == (1, 10)
