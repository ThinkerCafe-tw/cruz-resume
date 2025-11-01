# Technical Design Document

## Project: Cruz Resume - 多人格投影系統

**Project Name:** Cruz Resume
**Architecture:** Static Web Application (Vanilla JS) + AI Translation Workflow
**Language:** JavaScript (Frontend) + Python/Node.js (Workflow)

Generated on: 2025-10-31T23:44:46.697Z
Updated on: 2025-11-01 (架構分析後優化)

---

## Architecture Overview

### System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Cruz Resume System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐        ┌──────────────────┐          │
│  │   Frontend       │◄───────│   data.json      │          │
│  │   (index.html)   │        │   (Single Source) │          │
│  │                  │        │   - zh-TW ✍️     │          │
│  │  • 多人格切換    │        │   - en 🤖        │          │
│  │  • 多語言顯示    │        │   - ja 🤖        │          │
│  │  • 主題切換      │        │   - ko 🤖        │          │
│  │  • 響應式設計    │        │   - ar 🤖        │          │
│  └─────────────────┘        └──────────────────┘          │
│                                      ▲                       │
│                                      │                       │
│                                      │ update                │
│                              ┌───────┴────────┐             │
│                              │  AI Translation │             │
│                              │    Workflow     │             │
│                              │                 │             │
│                              │ • Gemini 2.5    │             │
│                              │ • Localization  │             │
│                              │ • Validation    │             │
│                              └─────────────────┘             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 核心設計原則
1. **前後端分離**: 前端純靜態，翻譯在 workflow 執行
2. **單一真理來源**: Cruz 只維護繁中原文
3. **多層次架構**: 語言層 × 人格層 = 靈活組合
4. **無框架依賴**: 使用 Vanilla JavaScript 確保輕量高效

---

## Key Components

### 1. Frontend Layer (index.html)

#### 1.1 核心 JavaScript 模組

**A. 版本切換系統** (`switchVersion()`)
```javascript
// 職責：處理 Personal / Enterprise 人格切換
function switchVersion(version) {
  // 1. 更新 URL 參數 (?version=enterprise)
  // 2. 切換按鈕 active 狀態
  // 3. 顯示/隱藏對應 DOM 區塊
  // 4. 動態生成 Enterprise 內容（從 data.json）
  // 5. 平滑滾動至頂部
}
```

**B. 語言切換系統** (`changeLanguage()`)
```javascript
// 職責：載入指定語言內容並更新 DOM
function changeLanguage(lang) {
  // 1. 從 data.json 載入對應語言資料
  // 2. 更新所有文字內容
  // 3. 處理 RTL 排版（阿拉伯文）
  // 4. 保持當前人格模式
}
```

**C. 資料載入** (`loadTranslations()`)
```javascript
// 職責：非同步載入 data.json
async function loadTranslations() {
  // 1. fetch('data.json')
  // 2. 快取至全域變數 translations
  // 3. 初始化預設語言 (zh-TW)
  // 4. 檢查 URL 參數決定初始人格
}
```

**D. 主題切換** (Theme Toggle)
```javascript
// 職責：深色/淺色模式切換
// - CSS 變數切換
// - localStorage 持久化
```

#### 1.2 CSS 架構

**主題變數系統**
```css
:root {
  --bg-primary: #0a0a0a;
  --text-primary: #ffffff;
  --accent-primary: #00ff88;
  /* ... 深色模式預設值 */
}

[data-theme="light"] {
  --bg-primary: #ffffff;
  --text-primary: #1a1a1a;
  /* ... 淺色模式覆蓋值 */
}
```

**人格切換控制**
```css
/* Personal 模式區塊 */
.version-personal { display: block; }
.version-enterprise { display: none; }

/* Enterprise 模式時反轉 */
/* 由 JavaScript 動態控制 */
```

---

### 2. Data Layer (data.json)

#### 2.1 資料結構設計

```json
{
  "zh-TW": {
    "hero": { "name": "...", "tagline": "..." },
    "nav": { "about": "...", "experience": "..." },
    "about": { "title": "...", "content": "..." },
    "experience": { ... },
    "education": { ... },
    "teaching": { ... },
    "skills": { ... },
    "portfolio": { ... },
    "cta": { ... },
    "footer": { ... },

    "enterprise": {
      "hero": { ... },
      "trustIndicators": { ... },
      "problemStatement": {
        "comparison": [
          { "label": "⏰ 開發週期", "traditional": "...", "aiNative": "..." }
        ]
      },
      "caseStudies": { ... },
      "methodology": { ... },
      "collaborationModels": { ... },
      "contactForm": { ... }
    }
  }
}
```

#### 2.2 語言區塊結構
- **zh-TW**: ✍️ Cruz 手動維護（原文）
- **en, ja, ko, ar**: 🤖 AI Workflow 自動生成

---

### 3. AI Translation Workflow

#### 3.1 Workflow 架構

**執行環境選項**
- **GitHub Actions**: 雲端執行，自動 commit
- **n8n Cloud**: 視覺化流程，支援 webhook
- **本地腳本**: Python/Node.js，快速測試

#### 3.2 翻譯流程

```
Step 1: 載入繁中原文
├─ 讀取 data.json["zh-TW"]
└─ 提取需翻譯的文字內容

Step 2: 準備翻譯任務
├─ 目標語言: [en, ja, ko, ar]
└─ 載入各語言的「在地化提示詞」

Step 3: 呼叫 Gemini 2.5 Flash API
├─ 輸入: zh-TW 原文 + 在地化提示詞
├─ 模型: gemini-2.0-flash-exp
└─ 輸出: 目標語言翻譯 JSON

Step 4: 驗證翻譯結果
├─ 結構完整性檢查（鍵值對應）
├─ 特殊字元處理（如 HTML 標籤）
└─ RTL 標記檢查（阿拉伯文）

Step 5: 更新 data.json
├─ 合併翻譯結果至對應語言區塊
├─ 保留原有 zh-TW 不變
└─ 產生更新後的 data.json

Step 6: 輸出與部署（可選）
├─ 本地: 直接覆蓋 data.json
└─ GitHub: 自動 commit & push
```

#### 3.3 在地化提示詞範例

**英文 (en)**
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

**日文 (ja)**
```
あなたは多言語履歴書ウェブサイトの専門翻訳者です。
以下の繁体字中国語コンテンツを日本語に翻訳してください。

ガイドライン:
- 技術用語は英語のまま保持（例："Claude Code"、"AI-Native"）
- ビジネス文書として適切な敬語を使用
- HTMLタグとフォーマットを保持
- ターゲット読者: 日本企業の採用担当者および意思決定者

出力形式: 入力と同じ構造のJSON
```

**阿拉伯文 (ar)** - 特殊處理
```
أنت مترجم محترف لموقع سيرة ذاتية متعدد اللغات.
قم بترجمة المحتوى التالي من الصينية التقليدية إلى العربية.

إرشادات:
- احتفظ بالمصطلحات التقنية بالإنجليزية
- استخدم لغة مهنية مناسبة للعملاء من الشركات
- احتفظ بعلامات HTML والتنسيق
- أضف علامة RTL للنصوص العربية

تنسيق الإخراج: JSON بنفس هيكل الإدخال
```

---

## Implementation Details

### Technology Stack

**Frontend**
- HTML5 (語義化標籤)
- CSS3 (CSS Variables, Flexbox, Grid)
- Vanilla JavaScript (ES6+)
- No frameworks, no build tools

**Workflow**
- **翻譯引擎**: Gemini 2.5 Flash API (`gemini-2.0-flash-exp`)
- **執行環境**: GitHub Actions / n8n / Python/Node.js
- **版本控制**: Git (自動 commit 翻譯結果)

**Deployment**
- **主機**: GitHub Pages
- **CDN**: GitHub 自動提供
- **域名**: `thinkercafe-tw.github.io/cruz-resume`

---

## Interface Specifications

### API Interface (Gemini 2.5 Flash)

```javascript
// Gemini API 呼叫介面
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent

Headers:
  Content-Type: application/json
  x-goog-api-key: [API_KEY]

Body:
{
  "contents": [{
    "parts": [{
      "text": "[在地化提示詞] + [zh-TW 原文 JSON]"
    }]
  }],
  "generationConfig": {
    "temperature": 0.3,
    "topP": 0.95,
    "maxOutputTokens": 8192
  }
}

Response:
{
  "candidates": [{
    "content": {
      "parts": [{
        "text": "[翻譯後的 JSON 字串]"
      }]
    }
  }]
}
```

---

## Configuration

### Environment Variables (Workflow)

```bash
# Gemini API
GEMINI_API_KEY=your_api_key_here

# GitHub (若使用 Actions 自動 commit)
GITHUB_TOKEN=automatically_provided_by_actions

# Deployment
DEPLOY_BRANCH=main
```

### Workflow Configuration 範例 (GitHub Actions)

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
        run: pip install google-generativeai
      - name: Run translation
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python scripts/translate.py
      - name: Commit changes
        run: |
          git config user.name "Translation Bot"
          git config user.email "bot@thinker.cafe"
          git add data.json
          git commit -m "🌐 Auto-translate: Update all languages"
          git push
```

---

## 擴展性設計

### 新增人格模式 (例如: Teaching Mode)

1. **更新 data.json 結構**
```json
{
  "zh-TW": {
    // ... existing content
    "teaching": {
      "hero": { ... },
      "curriculum": { ... },
      "testimonials": { ... }
    }
  }
}
```

2. **新增前端切換按鈕**
```html
<button class="version-btn" data-version="teaching"
        onclick="switchVersion('teaching')">
  教學講師
</button>
```

3. **擴展 switchVersion() 函數**
```javascript
function switchVersion(version) {
  // ... existing logic
  if (version === 'teaching') {
    // 生成 Teaching 模式內容
    generateTeachingContent(translations[currentLang].teaching);
  }
}
```

4. **翻譯會自動支援**（因為結構已在 data.json）
