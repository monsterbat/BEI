# 測試數據生成器

本目錄包含用於生成Blue Edge Index測試數據的工具和配置檔案。

## 📁 檔案說明

- `test_data_generator.py`: 主要的數據生成程式
- `data_generator_config.py`: 數據生成配置檔案
- `README.md`: 本說明檔案（原TEST_DATA_GENERATOR_README.md）

## 🎯 用途

這些工具主要用於：
1. **開發和測試**: 生成各種類型的測試數據
2. **演算法驗證**: 建立已知特性的數據集來驗證Blue Edge Index計算
3. **性能測試**: 生成大量數據來測試程式性能

## 🛠️ 使用方法

```bash
# 安裝額外的依賴套件（用於視覺化）
pip install matplotlib seaborn

# 執行數據生成器
python test_data_generator.py
```

## ⚠️ 注意事項

- 這些工具僅供開發和測試使用
- 一般使用者不需要執行這些程式
- 生成的數據檔案可能很大，請注意磁碟空間

## 📊 數據類型

生成器可以建立多種類型的測試數據：
- Edge Decay型: 模擬邊緣衰減效應
- Uniform型: 均勻分佈數據
- 客製化型: 根據配置檔案自定義的數據模式