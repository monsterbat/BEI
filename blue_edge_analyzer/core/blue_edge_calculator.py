"""
Blue Edge Index 計算模組
包含核心的Blue Edge Index計算算法
"""

import numpy as np
from typing import Tuple, Optional


class BlueEdgeCalculator:
    """Blue Edge Index 計算器"""
    
    def __init__(self):
        self.topside_threshold_percentage = 0.1  # TopSide 前10%的閾值
        self.bottomside_threshold_percentage = 0.1  # BottomSide 後10%的閾值
        # 為了向後相容，保持舊的變數名
        self.threshold_percentage = 0.1
        # NG判斷閾值 - Index值大於此數值則判斷為NG
        self.ng_threshold = 10.0
    
    def calculate_blue_edge_index(self, data: np.ndarray) -> Tuple[float, str]:
        """
        計算Blue Edge Index
        
        Args:
            data: 輸入的數據陣列
            
        Returns:
            Tuple[float, str]: (最大值, 判斷結果 'Pass'/'NG')
        """
        if len(data) == 0:
            return 0.0, 'NG'
        
        # 移除NaN值
        try:
            # 嘗試轉換為float並移除NaN
            float_data = data.astype(float)
            clean_data = float_data[~np.isnan(float_data)]
        except (ValueError, TypeError):
            # 如果轉換失敗，嘗試逐個處理
            clean_list = []
            for val in data:
                try:
                    float_val = float(val)
                    if not np.isnan(float_val):
                        clean_list.append(float_val)
                except (ValueError, TypeError):
                    continue
            clean_data = np.array(clean_list)
        
        if len(clean_data) == 0:
            return 0.0, 'NG'
        
        try:
            # 計算前N%位置的索引
            threshold_index = int(len(clean_data) * self.topside_threshold_percentage)
            if threshold_index == 0:
                threshold_index = 1
            
            # 取得前N%的數據
            threshold_data = clean_data[:threshold_index]
            
            # 取得基準值（第threshold_index個數據，即最後一個）
            baseline_value = threshold_data[-1]  # 第N%位置的數據
            
            # 計算比值並應用公式（基準值 ÷ 各個數據）
            calculated_values = []
            for i in range(threshold_index):
                current_value = threshold_data[i]
                if current_value != 0:
                    ratio = baseline_value / current_value
                    result = (ratio - 1) * 100
                    calculated_values.append(result)
                else:
                    calculated_values.append(0.0)
            
            # 找出最大值和其位置
            if calculated_values:
                max_value = max(calculated_values)
                max_position = calculated_values.index(max_value) + 1  # 位置從1開始計數
            else:
                max_value = 0.0
                max_position = 0
            
            # 判斷Pass/NG - 使用使用者設定的NG閾值
            judgment = 'NG' if max_value > self.ng_threshold else 'Pass'
            
            return max_value, judgment
            
        except Exception as e:
            print(f"計算Blue Edge Index時發生錯誤: {e}")
            return 0.0, 'NG'
    
    def set_threshold_percentage(self, percentage: float):
        """
        設定閾值百分比（向後相容）
        
        Args:
            percentage: 百分比 (0.0 - 1.0)
        """
        if 0.0 < percentage <= 1.0:
            self.threshold_percentage = percentage
            self.topside_threshold_percentage = percentage
    
    def set_topside_threshold_percentage(self, percentage: float):
        """
        設定TopSide閾值百分比
        
        Args:
            percentage: 百分比 (0.0 - 1.0)
        """
        if 0.0 < percentage <= 1.0:
            self.topside_threshold_percentage = percentage
    
    def set_bottomside_threshold_percentage(self, percentage: float):
        """
        設定BottomSide閾值百分比
        
        Args:
            percentage: 百分比 (0.0 - 1.0)
        """
        if 0.0 < percentage <= 1.0:
            self.bottomside_threshold_percentage = percentage
    
    def set_ng_threshold(self, threshold: float):
        """
        設定NG判斷閾值
        
        Args:
            threshold: NG閾值，Index值大於此數值則判斷為NG
        """
        if threshold >= 0.0:
            self.ng_threshold = threshold
    
    def calculate_bottomside_blue_edge_index(self, data: np.ndarray) -> Tuple[float, str]:
        """
        計算BottomSide Blue Edge Index
        
        Args:
            data: 輸入的數據陣列
            
        Returns:
            Tuple[float, str]: (最大值, 判斷結果 'Pass'/'NG')
        """
        if len(data) == 0:
            return 0.0, 'NG'
        
        # 移除NaN值
        try:
            # 嘗試轉換為float並移除NaN
            float_data = data.astype(float)
            clean_data = float_data[~np.isnan(float_data)]
        except (ValueError, TypeError):
            # 如果轉換失敗，嘗試逐個處理
            clean_list = []
            for val in data:
                try:
                    float_val = float(val)
                    if not np.isnan(float_val):
                        clean_list.append(float_val)
                except (ValueError, TypeError):
                    continue
            clean_data = np.array(clean_list)
        
        if len(clean_data) == 0:
            return 0.0, 'NG'
        
        try:
            # 計算後N%位置的索引
            threshold_index = int(len(clean_data) * self.bottomside_threshold_percentage)
            if threshold_index == 0:
                threshold_index = 1
            
            # 取得後N%的數據（從底部開始）
            threshold_data = clean_data[-threshold_index:]  # 取最後N%個數據
            
            # 取得基準值（倒數第threshold_index個數據，即第一個）
            baseline_value = threshold_data[0]  # 倒數第N%位置的數據
            
            # 計算比值並應用公式（基準值 ÷ 各個數據）
            calculated_values = []
            for i in range(threshold_index):
                current_value = threshold_data[i]
                if current_value != 0:
                    ratio = baseline_value / current_value
                    result = (ratio - 1) * 100
                    calculated_values.append(result)
                else:
                    calculated_values.append(0.0)
            
            # 找出最大值和其位置
            if calculated_values:
                max_value = max(calculated_values)
                max_position = calculated_values.index(max_value) + 1  # 位置從1開始計數
            else:
                max_value = 0.0
                max_position = 0
            
            # 判斷Pass/NG - 使用使用者設定的NG閾值
            judgment = 'NG' if max_value > self.ng_threshold else 'Pass'
            
            return max_value, judgment
            
        except Exception as e:
            print(f"計算BottomSide Blue Edge Index時發生錯誤: {e}")
            return 0.0, 'NG'
    
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
        
        try:
            # 嘗試轉換為float並移除NaN
            float_data = data.astype(float)
            clean_data = float_data[~np.isnan(float_data)]
        except (ValueError, TypeError):
            # 如果轉換失敗，嘗試逐個處理
            clean_list = []
            for val in data:
                try:
                    float_val = float(val)
                    if not np.isnan(float_val):
                        clean_list.append(float_val)
                except (ValueError, TypeError):
                    continue
            clean_data = np.array(clean_list)
        
        if len(clean_data) == 0:
            return {}
        
        try:
            # 計算前N%位置的索引
            threshold_index = int(len(clean_data) * self.topside_threshold_percentage)
            if threshold_index == 0:
                threshold_index = 1
            
            # 取得前N%的數據
            threshold_data = clean_data[:threshold_index]
            
            # 取得基準值
            baseline_value = threshold_data[-1]
            
            # 計算所有比值和結果
            calculated_values = []
            calculation_details = []
            
            for i in range(threshold_index):
                current_value = threshold_data[i]
                position = i + 1
                
                if current_value != 0:
                    ratio = baseline_value / current_value
                    result = (ratio - 1) * 100
                else:
                    ratio = 0.0
                    result = 0.0
                
                calculated_values.append(result)
                calculation_details.append({
                    'position': position,
                    'current_value': current_value,
                    'baseline_value': baseline_value,
                    'ratio': ratio,
                    'final_result': result
                })
            
            # 找出最大值和其位置
            if calculated_values:
                max_value = max(calculated_values)
                max_position = calculated_values.index(max_value) + 1
            else:
                max_value = 0.0
                max_position = 0
            
            return {
                'total_data_points': len(clean_data),
                'threshold_points': threshold_index,
                'threshold_percentage': self.topside_threshold_percentage,
                'baseline_value': baseline_value,
                'baseline_position': threshold_index,
                'calculated_values': calculated_values,
                'calculation_details': calculation_details,
                'max_value': max_value,
                'max_position': max_position,
                'data_range': (np.min(clean_data), np.max(clean_data)),
                'side_type': 'TopSide'
            }
            
        except Exception as e:
            print(f"取得計算詳情時發生錯誤: {e}")
            return {}
    
    def get_bottomside_calculation_details(self, data: np.ndarray) -> dict:
        """
        取得BottomSide詳細的計算資訊
        
        Args:
            data: 輸入的數據陣列
            
        Returns:
            dict: 包含詳細計算資訊的字典
        """
        if len(data) == 0:
            return {}
        
        try:
            # 嘗試轉換為float並移除NaN
            float_data = data.astype(float)
            clean_data = float_data[~np.isnan(float_data)]
        except (ValueError, TypeError):
            # 如果轉換失敗，嘗試逐個處理
            clean_list = []
            for val in data:
                try:
                    float_val = float(val)
                    if not np.isnan(float_val):
                        clean_list.append(float_val)
                except (ValueError, TypeError):
                    continue
            clean_data = np.array(clean_list)
        
        if len(clean_data) == 0:
            return {}
        
        try:
            # 計算後N%位置的索引
            threshold_index = int(len(clean_data) * self.bottomside_threshold_percentage)
            if threshold_index == 0:
                threshold_index = 1
            
            # 取得後N%的數據（從底部開始）
            threshold_data = clean_data[-threshold_index:]
            
            # 取得基準值
            baseline_value = threshold_data[0]
            
            # 計算所有比值和結果
            calculated_values = []
            calculation_details = []
            
            for i in range(threshold_index):
                current_value = threshold_data[i]
                position = i + 1
                # 實際在原數據中的位置（從底部開始計算）
                actual_position_from_bottom = i + 1
                actual_position_from_top = len(clean_data) - threshold_index + i + 1
                
                if current_value != 0:
                    ratio = baseline_value / current_value
                    result = (ratio - 1) * 100
                else:
                    ratio = 0.0
                    result = 0.0
                
                calculated_values.append(result)
                calculation_details.append({
                    'position': position,
                    'position_from_bottom': actual_position_from_bottom,
                    'position_from_top': actual_position_from_top,
                    'current_value': current_value,
                    'baseline_value': baseline_value,
                    'ratio': ratio,
                    'final_result': result
                })
            
            # 找出最大值和其位置
            if calculated_values:
                max_value = max(calculated_values)
                max_position = calculated_values.index(max_value) + 1
            else:
                max_value = 0.0
                max_position = 0
            
            return {
                'total_data_points': len(clean_data),
                'threshold_points': threshold_index,
                'threshold_percentage': self.bottomside_threshold_percentage,
                'baseline_value': baseline_value,
                'baseline_position': 1,  # BottomSide的基準值是第1個（倒數第N%個）
                'calculated_values': calculated_values,
                'calculation_details': calculation_details,
                'max_value': max_value,
                'max_position': max_position,
                'data_range': (np.min(clean_data), np.max(clean_data)),
                'side_type': 'BottomSide'
            }
            
        except Exception as e:
            print(f"取得BottomSide計算詳情時發生錯誤: {e}")
            return {}
