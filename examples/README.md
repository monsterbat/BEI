# 範例數據和測試檔案

本目錄包含Blue Edge Index Analyzer的範例數據和測試檔案。

## 📁 目錄結構

### `sample_data/`
包含範例測試數據：
- **sample_edge_decay.xlsx**: 邊緣衰減型數據範例

## 📊 數據說明

### sample_edge_decay.xlsx
模擬真實的Blue Edge現象，數據在邊緣部分有明顯的衰減特性。前10%的數據具有明顯的邊緣效應，適合用來驗證演算法的正確性。

### 如何生成更多測試數據
如果您需要更多類型的測試數據，可以使用 `data_samples/` 目錄中的數據生成工具：

```bash
cd data_samples
python test_data_generator.py
```

## 🧪 使用方式

1. **載入範例數據**：
   - 在Blue Edge Analyzer中點擊「選擇Excel檔案」
   - 選擇本目錄中的任一.xlsx檔案
   - 程式會自動分析並計算Blue Edge Index

2. **測試不同參數**：
   - 嘗試不同的「前N%閾值」設定
   - 觀察不同數據類型的計算結果差異

3. **驗證演算法**：
   - Edge Decay數據應該會產生較高的Blue Edge Index
   - Uniform數據應該會產生較低的Blue Edge Index

## 🔍 預期結果

- **Edge Decay數據**: Blue Edge Index > 1.0（通常為Pass）
- **Uniform數據**: Blue Edge Index ≈ 1.0（可能為NG）

這些範例數據可以幫助您：
- 驗證程式功能是否正常
- 理解Blue Edge Index的計算邏輯
- 測試不同參數設定的影響
