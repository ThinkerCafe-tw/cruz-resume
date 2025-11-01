# GitHub Actions 設定指南

## 🔑 設定 Secret: GEMINI_API_KEY

在使用自動翻譯 workflow 之前，需要先在 GitHub 設定 API Key。

### 步驟 1: 取得 Gemini API Key

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入你的 Google 帳號
3. 點擊 "Create API Key"
4. 複製產生的 API Key

### 步驟 2: 在 GitHub 設定 Secret

1. 前往你的 GitHub Repository
2. 點擊 **Settings** (設定)
3. 在左側選單選擇 **Secrets and variables** → **Actions**
4. 點擊 **New repository secret**
5. 填寫：
   - **Name**: `GEMINI_API_KEY`
   - **Value**: 貼上你的 Gemini API Key
6. 點擊 **Add secret**

### 步驟 3: 驗證設定

前往 **Actions** 標籤，應該會看到 "🌐 Auto-Translate Resume" workflow。

## 🚀 如何使用 Workflow

### 手動觸發翻譯

1. 前往 GitHub Repository 的 **Actions** 標籤
2. 在左側選擇 "🌐 Auto-Translate Resume"
3. 點擊右上角的 **Run workflow** 按鈕
4. 選擇選項：
   - **Dry run**: 選擇 `false` (正式執行) 或 `true` (測試模式)
5. 點擊綠色的 **Run workflow** 按鈕

### Workflow 執行流程

```
1. 📥 Checkout Repository
   ↓
2. 🐍 Setup Python 3.11
   ↓
3. 📦 Install Dependencies
   ↓
4. 🤖 Run Translation Script
   ↓
5. 📊 Check for Changes
   ↓
6. 💾 Commit and Push (如果有更改)
   ↓
7. 📝 Generate Summary
```

### 查看執行結果

執行完成後：
- ✅ 成功：會顯示綠色勾勾，data.json 已更新
- ❌ 失敗：會顯示紅色叉叉，檢查 logs 查看錯誤

點擊任一 workflow run，可以看到：
- **Summary**: 翻譯結果摘要
- **Logs**: 詳細執行日誌
- **Changes**: data.json 的變更內容

## 🔍 Dry Run 模式

如果你想測試翻譯但不儲存結果：

1. 執行 workflow 時選擇 `dry_run: true`
2. 腳本會執行翻譯但不會 commit 更改
3. 可在 logs 中查看翻譯結果

## 📊 自動 Commit Message 格式

成功執行後，會自動產生以下格式的 commit：

```
🌐 Auto-translate: Update all languages

- Translated from zh-TW to en, ja, ko, ar
- Using Gemini 2.5 Flash API
- Timestamp: 2025-11-01 12:34:56 UTC

🤖 Generated with [Cruz Resume Translation Workflow]
```

## ⚠️ 故障排除

### 錯誤：Missing GEMINI_API_KEY

**原因**: GitHub Secret 未設定或名稱錯誤

**解決**:
1. 確認 Secret 名稱是 `GEMINI_API_KEY`（大小寫要完全一致）
2. 重新設定 Secret
3. 重新執行 workflow

### 錯誤：API quota exceeded

**原因**: Gemini API 免費額度用完

**解決**:
1. 等待配額重置（通常是每分鐘 15 次請求）
2. 或升級至付費方案
3. 暫時減少翻譯語言數量

### 錯誤：Permission denied

**原因**: Workflow 沒有寫入權限

**解決**:
1. 前往 **Settings** → **Actions** → **General**
2. 在 "Workflow permissions" 選擇 "Read and write permissions"
3. 點擊 **Save**

### 錯誤：JSON parse error

**原因**: Gemini 回傳的不是有效 JSON

**解決**:
1. 檢查 logs 中的錯誤訊息
2. 可能需要調整 `scripts/prompts/*.txt` 提示詞
3. 降低 `temperature` 參數提高穩定性

## 🔒 安全性注意事項

- ✅ API Key 儲存在 GitHub Secrets，安全加密
- ✅ Secrets 不會在 logs 中顯示
- ✅ 只有 repository owner 可以修改 Secrets
- ⚠️  不要在 code 或 commit message 中暴露 API Key
- ⚠️  定期輪換 API Key

## 📈 最佳實踐

1. **定期執行**: 每次更新 zh-TW 原文後執行一次
2. **先測試**: 使用 dry run 模式確認翻譯品質
3. **檢查差異**: 執行後檢查 commit 的變更內容
4. **備份管理**: 定期清理 `data/backups/` 舊備份

## 🔗 相關資源

- [GitHub Actions 文件](https://docs.github.com/en/actions)
- [GitHub Secrets 文件](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Gemini API 文件](https://ai.google.dev/docs)
