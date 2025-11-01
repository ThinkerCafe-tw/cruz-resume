# AI Translation Workflow

使用 Gemini 2.5 Flash API 自動翻譯履歷內容到多種語言。

## 功能特點

- ✅ **單一真理來源**: 只需維護繁體中文 (zh-TW) 原文
- 🤖 **AI 驅動翻譯**: 使用 Google Gemini 2.5 Flash 進行高品質翻譯
- 🌍 **多語言支援**: 自動翻譯至英文、日文、韓文、阿拉伯文
- 📝 **在地化提示詞**: 每種語言都有專屬的文化適配提示詞
- ✅ **結構驗證**: 自動驗證翻譯結果的 JSON 結構完整性
- 💾 **自動備份**: 翻譯前自動備份原始檔案

## 安裝

### 1. 安裝 Python 依賴

```bash
cd scripts
pip install -r requirements.txt
```

### 2. 設定 API Key

複製 `.env.example` 為 `.env`：

```bash
cp ../.env.example ../.env
```

編輯 `.env` 並填入你的 Gemini API Key：

```env
GEMINI_API_KEY=your_actual_api_key_here
```

**取得 API Key**: https://makersuite.google.com/app/apikey

## 使用方法

### 基本用法

```bash
python translate.py
```

這會：
1. 讀取 `data.json` 中的 `zh-TW` 原文
2. 呼叫 Gemini API 翻譯至 en, ja, ko, ar
3. 驗證翻譯結果結構
4. 自動備份原檔案到 `data/backups/`
5. 更新 `data.json` 中的對應語言區塊

### 執行流程

```
📖 Loading data from data.json...
✅ Data loaded successfully (5 languages)
📝 Source language: zh-TW (12 sections)

============================================================
🌍 Processing language: en
============================================================
🤖 Translating to en using Gemini gemini-2.0-flash-exp...
✅ Translation to en completed
✅ Structure validation passed
✅ en translation completed and validated

[重複 ja, ko, ar...]

💾 Backup created: data/backups/data_20251101_123456.json
💾 Saving data to data.json...
✅ Data saved successfully

============================================================
✅ Translation completed successfully!
============================================================
📊 Updated languages: en, ja, ko, ar
💾 Backup saved to: data/backups
```

## 檔案結構

```
scripts/
├── translate.py          # 主翻譯腳本
├── requirements.txt      # Python 依賴
├── prompts/             # 在地化提示詞
│   ├── en.txt           # 英文翻譯提示詞
│   ├── ja.txt           # 日文翻譯提示詞
│   ├── ko.txt           # 韓文翻譯提示詞
│   └── ar.txt           # 阿拉伯文翻譯提示詞
└── README.md            # 本文件

data/
└── backups/             # 自動備份目錄
    └── data_*.json      # 時間戳記備份檔案
```

## 在地化提示詞

每種語言都有專屬的提示詞檔案，確保翻譯符合當地文化與商業慣例：

- **英文 (en.txt)**: 西方商業風格，直接、簡潔
- **日文 (ja.txt)**: 日本商業敬語，謙虛、禮貌
- **韓文 (ko.txt)**: 韓國商業用語，正式、專業
- **阿拉伯文 (ar.txt)**: 阿拉伯商業慣例，右至左排版

## 錯誤處理

- ✅ 如果某個語言翻譯失敗，會跳過該語言並保留原有內容
- ✅ 翻譯前自動備份，出錯可復原
- ✅ 結構驗證失敗會顯示詳細錯誤訊息

## 配置選項

在 `translate.py` 中可修改：

```python
# 目標語言
TARGET_LANGUAGES = ["en", "ja", "ko", "ar"]

# Gemini 模型
GEMINI_MODEL = "gemini-2.0-flash-exp"

# 生成參數
GENERATION_CONFIG = {
    "temperature": 0.3,      # 降低可提高一致性
    "top_p": 0.95,
    "max_output_tokens": 8192,
}
```

## 最佳實踐

1. **更新流程**:
   ```
   修改 zh-TW 原文 → 本地預覽 → 執行翻譯 → 檢查結果 → 部署
   ```

2. **備份策略**:
   - 翻譯前自動備份
   - 定期檢查 `data/backups/` 並清理舊備份

3. **漸進式翻譯**:
   - 可修改 `TARGET_LANGUAGES` 只翻譯特定語言
   - 降低 API 呼叫成本

## 成本估算

- **Gemini 2.5 Flash API**: 免費額度每分鐘 15 次請求
- **估計成本**: 完整翻譯 4 種語言約 4 次 API 呼叫
- **建議**: 在免費額度內使用

## 故障排除

### 問題：找不到 GEMINI_API_KEY

```
❌ Error: GEMINI_API_KEY not found in environment variables
```

**解決**:
1. 確認 `.env` 檔案存在
2. 確認 `.env` 中有 `GEMINI_API_KEY=...`
3. 重新執行腳本

### 問題：JSON 解析失敗

```
❌ Failed to parse Gemini response as JSON
```

**解決**:
1. 檢查 Gemini API 回應（會顯示前 200 字元）
2. 可能需要調整提示詞，要求更嚴格的 JSON 格式
3. 降低 `temperature` 參數提高穩定性

### 問題：結構驗證失敗

```
❌ Missing keys in translation: {...}
```

**解決**:
1. 檢查哪些 key 遺失
2. 調整提示詞強調保留結構
3. 手動補充遺失的內容

## 進階使用

### 只翻譯特定語言

修改 `translate.py`:

```python
TARGET_LANGUAGES = ["en"]  # 只翻譯英文
```

### 自訂提示詞

編輯 `prompts/*.txt` 檔案，調整翻譯風格和要求。

### Dry Run 模式

在 `main()` 函數中註解掉 `save_data()` 行，只執行翻譯不儲存：

```python
# save_data(data, backup=True)  # 註解掉
print("Dry run mode: not saving")
```

## 授權

MIT License
