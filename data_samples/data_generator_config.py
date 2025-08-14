"""
測試數據生成器配置檔案
用於控制生成參數的設定
"""

class DataGeneratorConfig:
    """數據生成器配置類別"""
    
    # 基本參數
    DISPLAY_SIZE_MM = 40.0          # 顯示器尺寸 (mm)
    RESOLUTION_MM = 0.1             # 解析度 (mm)
    CENTER_BRIGHTNESS = 30000       # 中心亮度值
    
    # 均勻數據參數
    UNIFORM_NOISE_LEVEL = 0.02      # 雜訊程度 (2%)
    UNIFORM_MIN_RATIO = 0.93        # 最小值比例 (93% of center)
    UNIFORM_MAX_RATIO = 1.07        # 最大值比例 (107% of center)
    
    # 邊緣衰減參數
    DECAY_START_POSITION = 20       # 衰減開始位置 (從邊緣往內幾格)
    DECAY_PERCENTAGES = [0.10, 0.15, 0.20, 0.30]  # 衰減百分比
    EDGE_NOISE_LEVEL = 0.01         # 邊緣區域雜訊程度 (1%)
    
    # 視覺化參數
    FIGURE_SIZE = (15, 6)           # 圖表大小
    DPI = 300                       # 圖片解析度
    COLORMAP = 'viridis'            # 色彩映射
    CONTOUR_LEVELS = 20             # 等高線層數
    
    # 檔案輸出參數
    OUTPUT_DIR = "test_data"        # 輸出目錄
    EXCEL_ENGINE = 'openpyxl'       # Excel引擎
    
    @classmethod
    def get_matrix_size(cls) -> int:
        """計算矩陣大小"""
        return int(cls.DISPLAY_SIZE_MM / cls.RESOLUTION_MM)
    
    @classmethod
    def get_decay_start_distance_mm(cls) -> float:
        """取得衰減開始距離 (mm)"""
        return cls.DECAY_START_POSITION * cls.RESOLUTION_MM
    
    @classmethod
    def print_config(cls):
        """印出目前配置"""
        print("=== 數據生成器配置 ===")
        print(f"顯示器尺寸: {cls.DISPLAY_SIZE_MM}mm x {cls.DISPLAY_SIZE_MM}mm")
        print(f"解析度: {cls.RESOLUTION_MM}mm")
        print(f"矩陣大小: {cls.get_matrix_size()}x{cls.get_matrix_size()}")
        print(f"中心亮度: {cls.CENTER_BRIGHTNESS}")
        print(f"衰減開始位置: {cls.DECAY_START_POSITION}格 ({cls.get_decay_start_distance_mm()}mm)")
        print(f"衰減百分比: {[f'{p*100:.0f}%' for p in cls.DECAY_PERCENTAGES]}")
        print(f"輸出目錄: {cls.OUTPUT_DIR}")


# 預設配置實例
config = DataGeneratorConfig()

if __name__ == "__main__":
    DataGeneratorConfig.print_config()
