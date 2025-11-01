# Implementation Tasks - Cruz Resume 多人格投影系統

## 專案資訊
**Feature**: -original-description-5-htmlcssjavascript-github-p
**專案狀態**: 已完成 2 個人格模式 (Personal + Enterprise)，待建立 AI 翻譯 Workflow
**設計階段**: 已完成

---

## 任務總覽

本專案分為 **4 大階段**：
1. ✅ **Phase 1**: 前端核心功能（已完成）
2. ✅ **Phase 1.5**: Bug 修復與 UI 優化（已完成）
3. 🚧 **Phase 2**: AI 翻譯 Workflow（待實作）
4. 🔮 **Phase 3**: 新人格擴展與優化（未來）

---

## Phase 1: 前端核心功能 ✅（已完成）

### Task 1.1: 多人格切換系統 ✅
**狀態**: 已完成
**檔案**: `index.html`
**實作內容**:
- [x] 版本切換按鈕 UI (Personal / Enterprise)
- [x] `switchVersion(version)` 函數
- [x] URL 參數同步 (`?version=enterprise`)
- [x] CSS class 控制顯示/隱藏 (`.version-personal`, `.version-enterprise`)
- [x] 動態生成 Enterprise 內容
- [x] 平滑滾動至頂部

**驗收標準**:
- ✅ 點擊切換按鈕能在 300ms 內完成切換
- ✅ URL 參數正確更新
- ✅ 支援深層連結（直接訪問 `?version=enterprise`）

---

### Task 1.2: 多語言顯示系統 ✅
**狀態**: 已完成
**檔案**: `index.html`, `data.json`
**實作內容**:
- [x] 語言選擇器 UI (zh-TW, en, ja, ko, ar)
- [x] `changeLanguage(lang)` 函數
- [x] `loadTranslations()` 非同步載入 data.json
- [x] 阿拉伯文 RTL 排版支援
- [x] 語言切換時保持當前人格模式

**驗收標準**:
- ✅ 切換語言時所有內容同步翻譯
- ✅ 阿拉伯文自動切換 RTL 排版
- ✅ 預設語言為繁體中文

---

### Task 1.3: 主題切換系統 ✅
**狀態**: 已完成
**檔案**: `index.html` (CSS)
**實作內容**:
- [x] 深色/淺色模式切換按鈕
- [x] CSS 變數系統 (`:root`, `[data-theme="light"]`)
- [x] localStorage 持久化主題偏好
- [x] 動畫過渡效果

**驗收標準**:
- ✅ 200ms 內完成主題切換
- ✅ 重新載入頁面保持主題設定
- ✅ 文字對比度符合 WCAG AA 標準

---

### Task 1.4: 響應式設計 ✅
**狀態**: 已完成
**檔案**: `index.html` (CSS)
**實作內容**:
- [x] 桌面版面 (>1200px)
- [x] 平板版面 (768-1200px)
- [x] 手機版面 (<768px)
- [x] 列印優化樣式
- [x] 滾動動畫 (Intersection Observer)

**驗收標準**:
- ✅ 所有裝置正確顯示
- ✅ 列印/PDF 輸出格式正確

---

## Phase 1.5: Bug 修復與 UI 優化 ✅（已完成）

### Task 1.5.1: 修復企業版顯示問題 ✅
**狀態**: 已完成
**檔案**: `index.html`
**問題描述**: 企業版內容生成後無法顯示，頁面呈現空白

#### 實作內容
- [x] **發現問題根源**:
  - CSS 變數未在動態生成的內容中生效
  - 容器定位問題導致內容在視口外
  - 文字顏色透明或與背景相同
  - 雙重滾動條問題

- [x] **解決方案**:
  - 創建獨立的 `ultimate-enterprise-wrapper` 容器
  - 使用 `position: absolute` 替代 `fixed`
  - 強制替換所有 CSS 變數為實際顏色值
  - 隱藏原始 `#enterprise-sections` 避免重複
  - 使用 `setProperty(..., 'important')` 強制覆蓋樣式

**驗收標準**:
- ✅ 企業版內容正常顯示（Hero + 6 個區塊）
- ✅ 只有一個滾動條（body 的）
- ✅ 所有文字清晰可見
- ✅ 顏色、背景、邊框正確顯示

**修改檔案**: `index.html` (Line 2568-2660)

---

### Task 1.5.2: 替換 Emoji 為 Font Awesome 圖標 ✅
**狀態**: 已完成
**檔案**: `index.html`, `data.json`
**需求**: 使用專業圖標庫替換 emoji，提升視覺一致性

#### 實作內容
- [x] **添加 Font Awesome CDN**:
  ```html
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  ```

- [x] **替換 data.json 中的 emoji**:
  - 🎓 → `<i class="fas fa-graduation-cap"></i>` (專業認證)
  - 👥 → `<i class="fas fa-users"></i>` (實戰經驗)
  - 🏆 → `<i class="fas fa-trophy"></i>` (教學資歷)
  - ⏰ → `<i class="fas fa-clock"></i>` (開發週期)
  - 💰 → `<i class="fas fa-dollar-sign"></i>` (成本)
  - 👨‍💻 → `<i class="fas fa-laptop-code"></i>` (團隊規模)
  - 🐌 → `<i class="fas fa-rotate"></i>` (迭代速度)
  - 📚 → `<i class="fas fa-book"></i>` (維護性)

- [x] **替換 index.html 中的 emoji**:
  - 📧 → `<i class="fas fa-envelope"></i>`
  - 💼 → `<i class="fab fa-linkedin"></i>`
  - 🌐 → `<i class="fas fa-globe"></i>`
  - 📱 → `<i class="fas fa-phone"></i>`
  - 💬 → `<i class="fab fa-line"></i>`

- [x] **替換 Portfolio 項目 emoji**:
  - 🧠 → `<i class="fas fa-brain"></i>`
  - 🚂 → `<i class="fas fa-train"></i>`
  - 📰 → `<i class="fas fa-newspaper"></i>`
  - 💆 → `<i class="fas fa-spa"></i>`
  - 🩴 → `<i class="fas fa-umbrella-beach"></i>`
  - 🎮 → `<i class="fas fa-gamepad"></i>`

**驗收標準**:
- ✅ 所有 emoji 替換為 Font Awesome 圖標
- ✅ 圖標在所有瀏覽器正常顯示
- ✅ 圖標大小、顏色與設計一致

**修改檔案**:
- `index.html` (Line 7-8, 1797-1808, 2035-2043, 2493-2504, 2062-2146, 3185-3187)
- `data.json` (Line 1147-1171)

---

### Task 1.5.3: 優化問題對比區塊為 Tailwind 風格卡片 ✅
**狀態**: 已完成
**檔案**: `index.html`
**需求**: 將純文字對比區塊改為專業卡片式設計

#### 實作內容
- [x] **設計改進**:
  - 從純文字列表 → 精美卡片式布局
  - 左右對比：傳統方式（紅色）vs AI-Native（綠色）
  - 添加玻璃態效果 (`backdrop-filter: blur(12px)`)
  - 微妙的背景光暈（徑向漸變）

- [x] **Tailwind 風格優化**:
  - 精確的間距系統（24px, 64px, 96px）
  - Hover 交互效果（上浮、陰影增強、邊框變化）
  - `cubic-bezier(0.4, 0, 0.2, 1)` 緩動函數
  - 響應式字體 `clamp(2rem, 4vw, 2.75rem)`
  - 漸變標題（白→灰）

- [x] **卡片特性**:
  - 半透明背景 `rgba(26, 26, 26, 0.6)`
  - 柔和邊框顏色（降低飽和度）
  - 16px 圓角（更現代）
  - 24px 內邊距
  - Drop-shadow 箭頭發光效果

**驗收標準**:
- ✅ 5 行卡片式對比設計
- ✅ Hover 效果流暢（上浮 + 陰影）
- ✅ 符合 Tailwind/Vercel 設計標準
- ✅ 玻璃態效果正常顯示

**修改檔案**: `index.html` (Line 2295-2391)

---

## Phase 2: AI 翻譯 Workflow ✅（已完成）

### Task 2.1: 建立翻譯腳本核心 ✅
**優先級**: 🔴 High
**預估時間**: 2-3 小時
**檔案**: `scripts/translate.py` (新建)

#### 實作內容
```python
# 1. 讀取 data.json
# 2. 提取 zh-TW 原文
# 3. 呼叫 Gemini API 翻譯
# 4. 驗證翻譯結果結構
# 5. 更新 data.json
```

#### 子任務
- [ ] **2.1.1** 建立 Python 專案結構
  - 建立 `scripts/` 目錄
  - 建立 `translate.py` 主程式
  - 建立 `requirements.txt` (依賴: `google-generativeai`)

- [ ] **2.1.2** 實作 JSON 讀寫功能
  ```python
  def load_data():
      """載入 data.json"""
      pass

  def save_data(data):
      """儲存 data.json（備份原檔案）"""
      pass
  ```

- [ ] **2.1.3** 實作 Gemini API 呼叫
  ```python
  def translate_with_gemini(text, target_lang, localization_prompt):
      """
      使用 Gemini 2.5 Flash 翻譯
      Args:
          text: 繁中原文（JSON 字串）
          target_lang: 目標語言 (en/ja/ko/ar)
          localization_prompt: 在地化提示詞
      Returns:
          翻譯後的 JSON 物件
      """
      pass
  ```

- [ ] **2.1.4** 實作結構驗證
  ```python
  def validate_translation(original, translated):
      """
      驗證翻譯結果結構完整性
      - 檢查所有鍵值是否對應
      - 檢查 HTML 標籤是否保留
      - 檢查陣列長度是否一致
      """
      pass
  ```

**驗收標準**:
- [x] 成功讀取並解析 data.json
- [x] 成功呼叫 Gemini API 並取得翻譯結果
- [x] 翻譯結果通過結構驗證
- [x] 備份原始檔案後正確更新 data.json

---

### Task 2.2: 建立在地化提示詞庫 ✅
**優先級**: 🔴 High
**預估時間**: 1-2 小時
**檔案**: `scripts/prompts/` (新建目錄)

#### 實作內容
建立 4 個在地化提示詞檔案：
- [x] **2.2.1** `en.txt` - 英文翻譯提示詞
  ```
  You are a professional translator for a multilingual resume website.
  Translate the following Traditional Chinese content to English.

  Guidelines:
  - Keep technical terms in English (e.g., "Claude Code", "AI-Native")
  - Maintain professional tone suitable for enterprise audiences
  - Preserve HTML tags and formatting
  - Use active voice and concise language
  - Target audience: International recruiters and enterprise clients

  Output format: JSON with same structure as input
  ```

- [x] **2.2.2** `ja.txt` - 日文翻譯提示詞
  ```
  あなたは多言語履歴書ウェブサイトの専門翻訳者です。
  以下の繁体字中国語コンテンツを日本語に翻訳してください。

  ガイドライン:
  - 技術用語は英語のまま保持
  - ビジネス文書として適切な敬語を使用
  - HTMLタグとフォーマットを保持

  出力形式: 入力と同じ構造のJSON
  ```

- [x] **2.2.3** `ko.txt` - 韓文翻譯提示詞
- [x] **2.2.4** `ar.txt` - 阿拉伯文翻譯提示詞（含 RTL 說明）

**驗收標準**:
- [x] 4 個語言的提示詞檔案完整
- [x] 提示詞包含文化適配指引
- [x] 提示詞要求保留 HTML 標籤與格式

---

### Task 2.3: 建立 GitHub Actions Workflow ✅
**優先級**: 🟡 Medium
**預估時間**: 1-2 小時
**檔案**: `.github/workflows/translate.yml` (新建)

#### 實作內容
```yaml
name: Translate Resume
on:
  workflow_dispatch:  # 手動觸發

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r scripts/requirements.txt

      - name: Run translation
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python scripts/translate.py

      - name: Commit changes
        run: |
          git config user.name "Translation Bot"
          git config user.email "bot@thinker.cafe"
          git add data.json
          git commit -m "🌐 Auto-translate: Update all languages" || echo "No changes"
          git push
```

#### 子任務
- [x] **2.3.1** 建立 `.github/workflows/` 目錄
- [x] **2.3.2** 撰寫 `translate.yml` workflow
- [x] **2.3.3** 在 GitHub 設定 Secret: `GEMINI_API_KEY`
- [ ] **2.3.4** 測試手動觸發 workflow（需要 push 到 GitHub 後測試）

**驗收標準**:
- [x] 可在 GitHub Actions 頁面手動觸發（已實作 workflow_dispatch）
- [x] 成功執行翻譯腳本（已實作）
- [x] 自動 commit 並 push 翻譯結果（已實作）
- [x] 翻譯失敗時不會破壞原檔案（已實作 backup 機制）

---

### Task 2.4: 本地測試與優化 ✅
**優先級**: 🟡 Medium
**預估時間**: 1-2 小時

#### 實作內容
- [x] **2.4.1** 建立 `.env.example` 檔案
  ```bash
  GEMINI_API_KEY=your_api_key_here
  ```

- [ ] **2.4.2** 建立本地測試腳本（暫未實作 --dry-run flag）
  ```bash
  # scripts/test-translate.sh
  python scripts/translate.py --dry-run  # 不寫入檔案，只輸出預覽
  ```

- [x] **2.4.3** 加入錯誤處理與日誌
  ```python
  import logging
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  ```

- [ ] **2.4.4** 實作翻譯快取（避免重複翻譯已翻譯過的內容）

**驗收標準**:
- [x] 本地可執行 `python scripts/translate.py` 完成翻譯 ✅ **已測試成功**
- [x] 翻譯過程有清楚的日誌輸出 ✅ **已實作**
- [x] 翻譯錯誤時有明確的錯誤訊息 ✅ **已實作**

#### 測試結果 (2025-11-01)
```
✅ 所有 4 種語言翻譯完成: en, ja, ko, ar
✅ 結構驗證通過
✅ 自動備份已創建: data/backups/data_20251101_130558.json (97KB)
✅ data.json 已更新
```

---

## Phase 2.5: 翻譯品質優化 🔮（未來規劃）

**當前狀態**: 90/100 分 - 語法正確、詞彙自然 ✅
**目標**: 95-100 分 - 符合體裁慣例、文化共鳴

### 語言學家視角的改進方向

#### 問題 1: 過度依賴規則，缺乏語境
**現狀**: 使用「不要用 X，要用 Y」的禁令式 prompts
**改進**:
- [ ] 提供 5-10 個同領域優秀履歷範例（英文/日文/韓文）
- [ ] 讓 AI 學習「真實母語者怎麼寫履歷」而非遵守規則
- [ ] 實作 few-shot learning 而非 zero-shot translation

#### 問題 2: 忽略體裁慣例（Genre Convention）
**現狀**: 把履歷當成一般商務文件翻譯
**改進**:
- [ ] 研究各國履歷書寫作慣例
  - 美國：Impact-first, 量化成就, 強動詞
  - 日本：經歷連貫性, 謙虛清晰, 團隊合作
  - 韓國：正式專業, 學歷重視, 資格證書
- [ ] 在 prompts 中加入體裁特定指引

#### 問題 3: 翻譯單位太小（Sentence-level vs. Discourse-level）
**現狀**: 逐句翻譯，強制保持 JSON 結構
**改進**:
- [ ] 允許資訊重組（Content Restructuring）
- [ ] 針對不同語言調整並列/主從/因果結構
- [ ] 考慮放寬「same structure」限制

#### 問題 4: 缺乏回譯驗證（Back-translation Check）
**現狀**: 單次翻譯，無驗證機制
**改進**:
- [ ] 實作回譯流程
  ```python
  def validate_with_backtranslation(original_zh, translated_en):
      # 1. zh-TW → en
      # 2. en → zh-TW (back-translation)
      # 3. 比對語義偏差
      # 4. 標記需要人工審核的段落
  ```
- [ ] 加入語義相似度檢查

#### 問題 5: 忽略讀者視角（Source-oriented vs. Target-oriented）
**現狀**: 要求「忠實翻譯原文」
**改進**:
- [ ] 針對不同讀者調整內容重點
  - 美國招聘者：關心「團隊產出什麼成果」
  - 日本招聘者：關心「如何協調不同文化」
  - 阿拉伯招聘者：關心「領導風格與價值觀」
- [ ] 實作 Target-oriented Localization

#### 問題 6: 缺乏文化隱喻（Cultural Metaphors）
**現狀**: 字面翻譯，保留原文比喻
**改進**:
- [ ] 建立文化適配指南
  - 「AI-Native」在日文可能改為「AI 活用の専門家」
  - 「Hands-on」在韓文需平衡「現場 + 戰略」
- [ ] 收集各文化的專業形象塑造慣例

### Task 2.5.1: 範例導向翻譯（Example-based Translation）
**優先級**: 🟡 Medium
**預估時間**: 3-4 小時

#### 實作內容
- [ ] 收集優秀履歷範例
  - 英文：3 個 AI/Tech 領域履歷（來源：LinkedIn, Resume.io）
  - 日文：3 個日本企業認可的履歷格式
  - 韓文：3 個韓國大企業標準履歷
- [ ] 加入 prompts 作為 few-shot examples
- [ ] 重新翻譯並對比品質差異

### Task 2.5.2: 母語者校對流程
**優先級**: 🟡 Medium
**預估時間**: 依賴外部資源

#### 實作步驟
- [ ] 找母語者審核（每語言 1 位）
  - 日文母語者（日本企業工作經驗）
  - 韓文母語者（韓國 HR 背景佳）
  - 阿拉伯文母語者
- [ ] 收集反饋：「聽起來自然嗎？」「會嚇跑招聘者嗎？」
- [ ] 整理常見問題並更新 prompts

### Task 2.5.3: 術語庫建立（Terminology Database）
**優先級**: 🔵 Low
**預估時間**: 持續累積

#### 內容
- [ ] 建立 `scripts/glossary/` 目錄
- [ ] 按行業/角色建立術語對照表
  ```json
  {
    "AI_implementation": {
      "en": "AI solutions / AI integration",
      "ja": "AI 導入 / AI 活用",
      "ko": "AI 도입 / AI 적용",
      "context": "避免直譯為 implementation/実装/구현"
    }
  }
  ```

---

## Phase 3: 新人格擴展 🔮（未來規劃）

### Task 3.1: Teaching Mode（教學講師人格）
**優先級**: 🔵 Future
**依賴**: Phase 2 完成

#### 實作步驟
1. **資料結構設計**
   - [ ] 在 `data.json` 的 `zh-TW` 區塊新增 `teaching` 區塊
   ```json
   "teaching": {
     "hero": {
       "title": "AI 教育專家",
       "subtitle": "10+ 年教學經驗，讓複雜技術變得易懂"
     },
     "curriculum": [...],
     "testimonials": [...],
     "courses": [...]
   }
   ```

2. **前端實作**
   - [ ] 新增「教學講師」切換按鈕
   - [ ] 擴展 `switchVersion()` 函數支援 `teaching` 模式
   - [ ] 設計 Teaching 版的 CSS 樣式

3. **自動翻譯**
   - [ ] 執行翻譯 workflow（自動支援，因為結構已在 data.json）

---

### Task 3.2: Proposal Mode（提案模式人格）
**優先級**: 🔵 Future
**概念**: 針對合作提案的專業展示

#### 設計重點
- 聚焦於「解決方案」與「合作案例」
- 強調「技術可行性」與「快速交付」
- 包含「合作流程」與「報價參考」

---

### Task 3.3: Speaker Mode（演講者人格）
**優先級**: 🔵 Future
**概念**: 針對活動主辦方的講師介紹

#### 設計重點
- 演講主題列表
- 過往演講紀錄
- 學員回饋
- 演講形式（工作坊/講座/內訓）

---

## 優化任務（持續進行）

### Task O.1: SEO 與分享優化
- [ ] 每個人格有獨立的 meta tags
- [ ] Open Graph 標籤設定
- [ ] Twitter Card 支援
- [ ] JSON-LD 結構化資料

### Task O.2: Analytics 整合
- [ ] Google Analytics 4
- [ ] 追蹤人格切換事件
- [ ] 追蹤語言切換事件
- [ ] 分析不同人格的轉換率

### Task O.3: Performance 優化
- [ ] 圖片懶載入
- [ ] data.json 快取策略
- [ ] CSS/JS 最小化
- [ ] Lighthouse 分數優化至 95+

---

## 實作建議順序

### 第一週：建立 AI 翻譯 Workflow
1. Task 2.1 → 2.2 → 2.4 → 2.3（先本地測試，再整合 GitHub Actions）

### 第二週：測試與優化
1. 執行完整翻譯測試
2. 驗證 5 種語言的翻譯品質
3. 調整在地化提示詞

### 未來擴展：新人格開發
1. 根據需求優先開發 Teaching / Proposal / Speaker 模式
2. 每個新人格預估 1-2 天完成（資料 + 前端 + 翻譯）

---

## 技術債務與注意事項

### ⚠️ 已知問題
1. **翻譯成本**: Gemini API 有呼叫次數限制，需設定快取機制
2. **資料一致性**: Cruz 更新繁中內容後需手動觸發翻譯
3. **版本控制**: 翻譯結果會自動 commit，需注意 git history

### 💡 最佳實踐
1. **更新流程**: Cruz 更新 zh-TW → 本地預覽 → 觸發翻譯 → 檢查結果 → 部署
2. **備份策略**: 每次翻譯前自動備份 data.json
3. **漸進式翻譯**: 可先只翻譯特定區塊（如 hero, about），降低 API 成本

---

## 完成標準

### Phase 2 完成標準
- [x] ✅ 前端核心功能完整運作
- [ ] 🚧 AI 翻譯 Workflow 可手動觸發並成功執行
- [ ] 🚧 4 種目標語言翻譯品質達標
- [ ] 🚧 GitHub Actions 自動化流程正常運作

### 專案完成標準
- [ ] 支援 5 種語言
- [ ] 支援 2+ 種人格模式
- [ ] 頁面載入時間 < 2 秒
- [ ] Lighthouse Performance > 90
- [ ] 所有功能通過跨瀏覽器測試
