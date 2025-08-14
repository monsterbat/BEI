"""
顯示器測試數據生成器
專門用於生成Blue Edge分析用的測試Excel檔案

功能：
1. 生成400x400矩陣數據（對應40mm x 40mm，解析度0.1mm）
2. 創建不同邊緣衰減程度的測試數據
3. 生成偽色圖和等高線圖進行視覺化
4. 輸出Excel檔案供分析使用
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import cm
import seaborn as sns
from typing import Tuple, List
import os
from datetime import datetime


class DisplayTestDataGenerator:
    """顯示器測試數據生成器"""
    
    def __init__(self, size_mm: float = 40.0, resolution_mm: float = 0.1):
        """
        初始化生成器
        
        Args:
            size_mm: 顯示器尺寸 (mm)
            resolution_mm: 解析度 (mm)
        """
        self.size_mm = size_mm
        self.resolution_mm = resolution_mm
        self.matrix_size = int(size_mm / resolution_mm)  # 400x400
        self.center_value = 30000  # 中心亮度值
        
        print(f"初始化測試數據生成器:")
        print(f"  - 顯示器尺寸: {size_mm}mm x {size_mm}mm")
        print(f"  - 解析度: {resolution_mm}mm")
        print(f"  - 矩陣大小: {self.matrix_size}x{self.matrix_size}")
        print(f"  - 中心亮度值: {self.center_value}")
    
    def generate_uniform_data(self, noise_level: float = 0.02) -> np.ndarray:
        """
        生成均勻分佈的測試數據
        
        Args:
            noise_level: 雜訊程度 (0.0-1.0)
            
        Returns:
            np.ndarray: 400x400的均勻數據矩陣
        """
        # 基礎均勻數據
        base_matrix = np.full((self.matrix_size, self.matrix_size), self.center_value, dtype=float)
        
        # 加入輕微的隨機變化，模擬實際測量的微小差異
        noise = np.random.normal(0, self.center_value * noise_level, (self.matrix_size, self.matrix_size))
        
        # 確保數值在合理範圍內 (28000-32000)
        result = base_matrix + noise
        result = np.clip(result, self.center_value * 0.93, self.center_value * 1.07)
        
        return result
    
    def generate_edge_decay_data(self, decay_percentage: float, decay_start_position: int = 20) -> np.ndarray:
        """
        生成邊緣衰減的測試數據
        
        Args:
            decay_percentage: 衰減百分比 (0.1 = 10%)
            decay_start_position: 從邊緣開始衰減的位置 (格數)
            
        Returns:
            np.ndarray: 400x400的邊緣衰減數據矩陣
        """
        # 先生成均勻數據作為基礎
        matrix = self.generate_uniform_data(noise_level=0.01)
        
        # 計算衰減後的邊緣值
        edge_value = self.center_value * (1 - decay_percentage)
        
        # 創建距離矩陣（距離最近邊緣的距離）
        y_indices, x_indices = np.ogrid[:self.matrix_size, :self.matrix_size]
        
        # 計算到各邊緣的距離
        dist_to_top = y_indices
        dist_to_bottom = self.matrix_size - 1 - y_indices
        dist_to_left = x_indices
        dist_to_right = self.matrix_size - 1 - x_indices
        
        # 找到到最近邊緣的距離
        min_edge_distance = np.minimum(
            np.minimum(dist_to_top, dist_to_bottom),
            np.minimum(dist_to_left, dist_to_right)
        )
        
        # 創建衰減遮罩
        decay_mask = min_edge_distance < decay_start_position
        
        # 在衰減區域內，根據距離邊緣的遠近進行平滑衰減
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                edge_dist = min_edge_distance[i, j]
                if edge_dist < decay_start_position:
                    # 使用平滑的衰減曲線 (cosine函數)
                    decay_ratio = 0.5 * (1 + np.cos(np.pi * edge_dist / decay_start_position))
                    current_value = self.center_value * (1 - decay_percentage * decay_ratio)
                    
                    # 加入一些隨機雜訊
                    noise = np.random.normal(0, current_value * 0.01)
                    matrix[i, j] = current_value + noise
        
        return matrix
    
    def create_visualization(self, data: np.ndarray, title: str, save_path: str = None):
        """
        創建數據視覺化圖表（偽色圖和等高線圖）
        
        Args:
            data: 數據矩陣
            title: 圖表標題
            save_path: 儲存路徑
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 偽色圖
        im1 = ax1.imshow(data, cmap='viridis', aspect='equal')
        ax1.set_title(f'{title} - 偽色圖')
        ax1.set_xlabel('X軸位置 (0.1mm/格)')
        ax1.set_ylabel('Y軸位置 (0.1mm/格)')
        
        # 添加色彩條
        cbar1 = plt.colorbar(im1, ax=ax1)
        cbar1.set_label('亮度值')
        
        # 等高線圖
        x = np.arange(0, self.matrix_size)
        y = np.arange(0, self.matrix_size)
        X, Y = np.meshgrid(x, y)
        
        # 創建等高線
        contour_levels = np.linspace(data.min(), data.max(), 20)
        cs = ax2.contour(X, Y, data, levels=contour_levels, colors='black', linewidths=0.5)
        ax2.clabel(cs, inline=True, fontsize=8, fmt='%.0f')
        
        # 填充等高線
        cs_filled = ax2.contourf(X, Y, data, levels=contour_levels, cmap='viridis', alpha=0.7)
        ax2.set_title(f'{title} - 等高線圖')
        ax2.set_xlabel('X軸位置 (0.1mm/格)')
        ax2.set_ylabel('Y軸位置 (0.1mm/格)')
        
        # 添加色彩條
        cbar2 = plt.colorbar(cs_filled, ax=ax2)
        cbar2.set_label('亮度值')
        
        # 顯示統計資訊
        stats_text = f'最大值: {data.max():.0f}\n最小值: {data.min():.0f}\n平均值: {data.mean():.0f}\n標準差: {data.std():.0f}'
        ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"視覺化圖表已儲存: {save_path}")
        
        plt.show()
    
    def save_to_excel(self, data: np.ndarray, filename: str, sheet_name: str = 'TestData'):
        """
        將數據儲存為Excel檔案
        
        Args:
            data: 數據矩陣
            filename: 檔案名稱
            sheet_name: 工作表名稱
        """
        # 創建DataFrame
        df = pd.DataFrame(data)
        
        # 儲存為Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
        
        print(f"Excel檔案已儲存: {filename}")
        print(f"  - 工作表: {sheet_name}")
        print(f"  - 數據大小: {data.shape}")
        print(f"  - 數值範圍: {data.min():.0f} ~ {data.max():.0f}")
    
    def generate_test_suite(self, output_dir: str = "test_data"):
        """
        生成完整的測試數據套件
        
        Args:
            output_dir: 輸出目錄
        """
        # 創建輸出目錄
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"\n開始生成測試數據套件...")
        print(f"輸出目錄: {output_dir}")
        
        # 1. 生成均勻數據
        print("\n1. 生成均勻分佈數據...")
        uniform_data = self.generate_uniform_data()
        uniform_filename = os.path.join(output_dir, f"uniform_data_{timestamp}.xlsx")
        uniform_viz_path = os.path.join(output_dir, f"uniform_data_{timestamp}.png")
        
        self.save_to_excel(uniform_data, uniform_filename, "UniformData")
        self.create_visualization(uniform_data, "均勻分佈測試數據", uniform_viz_path)
        
        # 2. 生成不同衰減程度的數據
        decay_percentages = [0.10, 0.15, 0.20, 0.30]  # 10%, 15%, 20%, 30%
        
        for decay_pct in decay_percentages:
            print(f"\n2. 生成邊緣衰減數據 ({decay_pct*100:.0f}%)...")
            
            decay_data = self.generate_edge_decay_data(decay_pct)
            decay_filename = os.path.join(output_dir, f"edge_decay_{int(decay_pct*100)}percent_{timestamp}.xlsx")
            decay_viz_path = os.path.join(output_dir, f"edge_decay_{int(decay_pct*100)}percent_{timestamp}.png")
            
            self.save_to_excel(decay_data, decay_filename, f"EdgeDecay_{int(decay_pct*100)}pct")
            self.create_visualization(decay_data, f"邊緣衰減 {decay_pct*100:.0f}% 測試數據", decay_viz_path)
        
        print(f"\n✅ 測試數據套件生成完成！")
        print(f"總共生成了 {len(decay_percentages) + 1} 個Excel檔案和對應的視覺化圖表")


def main():
    """主程式"""
    print("=== 顯示器測試數據生成器 ===")
    print("專門用於Blue Edge Index分析的測試數據生成")
    
    # 創建生成器
    generator = DisplayTestDataGenerator(size_mm=40.0, resolution_mm=0.1)
    
    # 生成測試數據套件
    generator.generate_test_suite()
    
    print("\n程式執行完成！")
    print("您可以使用生成的Excel檔案來測試您的Blue Edge分析器。")


if __name__ == "__main__":
    main()
