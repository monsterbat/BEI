"""
Blue Edge Index 計算模組
包含核心的Blue Edge Index計算算法
"""

import numpy as np
from typing import Tuple, Optional


class BlueEdgeCalculator:
    """Blue Edge Index 計算器"""
    
    def __init__(self):
        self.threshold_percentage = 0.1  # 前10%的閾值
    
    def calculate_blue_edge_index(self, data: np.ndarray) -> Tuple[float, str]:
        """
        計算Blue Edge Index
        
        Args:
            data: 輸入的數據陣列
            
        Returns:
            Tuple[float, str]: (計算結果, 判斷結果 'Pass'/'NG')
        """
        if len(data) == 0:
            return 0.0, 'NG'
        
        # 移除NaN值
        clean_data = data[~np.isnan(data.astype(float, errors='ignore'))]
        
        if len(clean_data) == 0:
            return 0.0, 'NG'
        
        try:
            # 計算前10%位置的索引
            top_10_percent_index = int(len(clean_data) * self.threshold_percentage)
            if top_10_percent_index == 0:
                top_10_percent_index = 1
            
            # 取得前10%的數據
            top_10_percent_data = clean_data[:top_10_percent_index]
            
            # 計算平均值
            top_10_percent_avg = np.mean(top_10_percent_data)
            
            # 計算整體平均值
            overall_avg = np.mean(clean_data)
            
            # 計算Blue Edge Index (這裡是範例計算方式，您可以根據實際需求調整)
            if overall_avg != 0:
                blue_edge_index = top_10_percent_avg / overall_avg
            else:
                blue_edge_index = 0.0
            
            # 判斷Pass/NG (這裡設定一個範例閾值，您可以根據實際需求調整)
            judgment = 'Pass' if blue_edge_index > 1.0 else 'NG'
            
            return blue_edge_index, judgment
            
        except Exception as e:
            print(f"計算Blue Edge Index時發生錯誤: {e}")
            return 0.0, 'NG'
    
    def set_threshold_percentage(self, percentage: float):
        """
        設定閾值百分比
        
        Args:
            percentage: 百分比 (0.0 - 1.0)
        """
        if 0.0 < percentage <= 1.0:
            self.threshold_percentage = percentage
    
    def get_calculation_details(self, data: np.ndarray) -> dict:
        """
        取得詳細的計算資訊
        
        Args:
            data: 輸入的數據陣列
            
        Returns:
            dict: 包含詳細計算資訊的字典
        """
        if len(data) == 0:
            return {}
        
        clean_data = data[~np.isnan(data.astype(float, errors='ignore'))]
        
        if len(clean_data) == 0:
            return {}
        
        top_10_percent_index = int(len(clean_data) * self.threshold_percentage)
        if top_10_percent_index == 0:
            top_10_percent_index = 1
        
        top_10_percent_data = clean_data[:top_10_percent_index]
        
        return {
            'total_data_points': len(clean_data),
            'top_10_percent_points': len(top_10_percent_data),
            'top_10_percent_avg': np.mean(top_10_percent_data),
            'overall_avg': np.mean(clean_data),
            'data_range': (np.min(clean_data), np.max(clean_data)),
            'threshold_percentage': self.threshold_percentage
        }
