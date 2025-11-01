# Requirements Document

## Introduction
**Project**: Cruz Resume - 多人格投影系統 (Multi-Persona Projection System)
**Feature**: -original-description-5-htmlcssjavascript-github-p
**Description**: 一個根據不同受眾動態呈現不同專業面向的智能履歷系統

Generated on: 2025-10-31T23:44:38.304Z
Updated on: 2025-11-01 (架構分析後優化)

---

## 專案願景 (Project Vision)

### 核心概念
傳統履歷是**靜態、單一視角**的。Cruz Resume 是一個**人格投影系統**，能夠：
- 根據不同受眾（企業客戶、學員、雇主、合作夥伴）展示不同的專業面向
- 讓每個受眾都能看到「他們需要的那個 Cruz」
- 保持**一套核心數據結構**，透過智能切換呈現不同內容重點

### 業務價值
- **溝通效率**: 無需準備多份履歷，一個系統服務多元受眾
- **專業形象**: 展示系統化思考與技術實力
- **轉換率**: 不同模式優化不同目標（企業詢問率、學員報名意願、面試邀約數）

---

## 系統架構層次

### Layer 1: AI 驅動多語言系統 (AI-Powered i18n)
- **支援語言**: 繁中 (zh-TW), 英文 (en), 日文 (ja), 韓文 (ko), 阿拉伯文 (ar)
- **翻譯架構**:
  - **單一真理來源**: `data.json` 只保留繁體中文 (zh-TW) 原文
  - **手動觸發翻譯**: 透過 workflow（GitHub Actions / n8n / 本地腳本）觸發
  - **AI 翻譯引擎**: Gemini 2.5 Flash API
  - **在地化提示詞**: 每種語言有專屬的「在地化轉化翻譯提示詞」確保文化適配
  - **輸出更新**: 翻譯完成後自動更新 `data.json` 對應語言區塊
- **維護優勢**: Cruz 只需維護繁中版本，其他語言自動生成
- **特殊支援**: 阿拉伯文 RTL (Right-to-Left) 排版

### Layer 2: 多人格模式 (Multi-Persona)
目前實作 2 種人格，架構支援未來擴展：

#### 已實作人格
1. **Personal Mode** (個人履歷模式)
   - **目標受眾**: HR、雇主、求職相關
   - **內容重點**: 完整工作經歷、教育背景、技能展示
   - **區塊**: hero, about, experience, education, teaching, skills, portfolio, cta

2. **Enterprise Mode** (企業顧問模式)
   - **目標受眾**: 企業決策者、潛在客戶
   - **內容重點**: 解決方案能力、快速交付、成功案例
   - **銷售漏斗**: hero → trustIndicators → problemStatement → caseStudies → methodology → collaborationModels → contactForm

#### 未來可擴展人格
3. **Teaching Mode** (教學講師模式) - 給學員看
4. **Proposal Mode** (提案模式) - 給合作夥伴看
5. **Speaker Mode** (演講者模式) - 給活動主辦方看

---

## Functional Requirements

### FR-1: 多人格切換系統
**Objective:** 提供流暢的人格模式切換功能

#### Acceptance Criteria
1. WHEN 使用者點擊版本切換按鈕 THEN 系統應在 300ms 內完成切換
2. WHEN 切換人格 THEN URL 參數應同步更新 (如 `?version=enterprise`)
3. WHEN 透過 URL 直接訪問 THEN 應正確載入指定人格 (支援深層連結)
4. WHEN 切換人格 THEN 頁面應平滑滾動至頂部，不閃爍
5. IF 未指定人格 THEN 預設顯示 Personal Mode

#### Technical Details
- 使用 CSS class `.version-personal` 和 `.version-enterprise` 控制顯示/隱藏
- JavaScript 函數 `switchVersion(version)` 負責切換邏輯
- 支援 `window.history.pushState` 更新 URL 不重新載入頁面

---

### FR-2: 多語言內容管理與翻譯 Workflow
**Objective:** 提供完整的多語言支援、切換與 AI 翻譯流程

#### Acceptance Criteria - 前端顯示
1. WHEN 切換語言 THEN 所有內容（包括當前人格）應同步翻譯
2. WHEN 切換語言 THEN 語言選擇器應顯示當前語言
3. WHEN 語言為阿拉伯文 THEN 自動切換為 RTL 排版
4. WHEN 載入頁面 THEN 預設語言為繁體中文 (zh-TW)
5. WHEN 切換語言或人格 THEN 數據應從 `data.json` 正確載入

#### Acceptance Criteria - 翻譯 Workflow
1. WHEN Cruz 更新繁中內容 THEN 可手動觸發翻譯 workflow
2. WHEN 觸發翻譯 workflow THEN 應讀取 `data.json` 的 `zh-TW` 區塊作為來源
3. WHEN 呼叫 Gemini 2.5 Flash API THEN 應使用對應語言的「在地化提示詞」
4. WHEN 翻譯完成 THEN 應自動更新 `data.json` 對應語言區塊 (en, ja, ko, ar)
5. WHEN 翻譯發生錯誤 THEN 應保留原有翻譯，並記錄錯誤日誌
6. WHEN 翻譯完成 THEN 可選擇是否自動 commit & push 到 GitHub

#### Data Structure
```javascript
{
  "zh-TW": {              // 【原文】Cruz 手動維護
    "hero": {...},
    "about": {...},
    "experience": {...},
    "enterprise": {       // Enterprise 版完整內容
      "hero": {...},
      "trustIndicators": {...},
      ...
    }
  },
  "en": { ... },          // 【翻譯】workflow 自動生成
  "ja": { ... },          // 【翻譯】workflow 自動生成
  "ko": { ... },          // 【翻譯】workflow 自動生成
  "ar": { ... }           // 【翻譯】workflow 自動生成（含 RTL 優化）
}
```

#### Translation Workflow 設計
```
1. 觸發：手動執行 workflow（GitHub Actions / n8n / 本地腳本）
2. 讀取：載入 data.json 的 zh-TW 原文
3. 翻譯：對每種目標語言：
   - 載入該語言的「在地化提示詞」
   - 呼叫 Gemini 2.5 Flash API
   - 驗證翻譯結果結構完整性
4. 更新：將翻譯結果寫回 data.json
5. 輸出：（可選）自動 commit & push
```

---

### FR-3: 響應式設計與動畫
**Objective:** 提供優秀的多裝置體驗

#### Acceptance Criteria
1. WHEN 在桌面裝置 (>1200px) THEN 應顯示完整版面
2. WHEN 在平板裝置 (768-1200px) THEN 應自動調整排版
3. WHEN 在手機裝置 (<768px) THEN 應顯示行動優化版本
4. WHEN 滾動頁面 THEN 內容應以淡入動畫呈現
5. WHEN 列印或匯出 PDF THEN 應使用列印優化樣式

---

### FR-4: 主題切換
**Objective:** 支援深色/淺色模式切換

#### Acceptance Criteria
1. WHEN 點擊主題切換按鈕 THEN 應在 200ms 內完成切換
2. WHEN 切換主題 THEN 所有顏色變數應正確更新
3. WHEN 重新載入頁面 THEN 應記住使用者的主題偏好 (localStorage)
4. WHEN 在深色模式 THEN 文字對比度應符合 WCAG AA 標準

---

### FR-5: Enterprise 版銷售漏斗
**Objective:** 提供完整的企業客戶轉換流程

#### Acceptance Criteria
1. WHEN 進入 Enterprise 模式 THEN 應依序呈現：
   - Hero (痛點導向開場)
   - Trust Indicators (信任背書)
   - Problem Statement (問題陳述 + 傳統 vs AI-Native 對比)
   - Case Studies (實際案例 + Demo 連結)
   - Methodology (工作方法 4 步驟)
   - Collaboration Models (3 種合作方式)
   - Contact Form (免費診斷預約)

2. WHEN 顯示對比表 THEN 應清楚呈現傳統開發 vs AI-Native 的差異
3. WHEN 顯示案例 THEN 應包含痛點、成果、時間對比
4. WHEN 點擊 CTA 按鈕 THEN 應引導至聯絡表單或預約系統

---

## Non-Functional Requirements

### NFR-1: Performance
- 頁面載入時間 < 2 秒（任何裝置）
- 人格切換時間 < 300ms
- 語言切換時間 < 500ms
- Lighthouse Performance Score > 90

### NFR-2: Accessibility
- WCAG 2.1 Level AA 合規
- 支援鍵盤導航
- 支援螢幕閱讀器
- 文字對比度 > 4.5:1

### NFR-3: Maintainability
- 使用純 HTML/CSS/JavaScript，無框架依賴
- 所有內容集中在 `data.json`，便於維護
- CSS 使用變數管理主題色
- 程式碼註解清楚，易於擴展新人格

### NFR-4: SEO & Sharing
- 每個人格有獨立的 meta tags
- 支援 Open Graph 標籤（社群分享優化）
- 語義化 HTML 標籤
- 可被搜尋引擎索引

### NFR-5: Scalability
- 架構支援未來新增人格模式（Teaching, Proposal, Speaker 等）
- 新增語言只需擴充 `data.json`
- 版本切換邏輯可複用於新人格
