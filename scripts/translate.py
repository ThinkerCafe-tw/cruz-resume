#!/usr/bin/env python3
"""
AI-Powered Translation Script for Cruz Resume
Uses Gemini 2.5 Flash API to translate Traditional Chinese to multiple languages
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data.json"
BACKUP_DIR = PROJECT_ROOT / "data" / "backups"
TARGET_LANGUAGES = ["en", "ja", "ko", "ar"]

# Gemini API Configuration
GEMINI_MODEL = "gemini-2.5-flash"
GENERATION_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.95,
    "max_output_tokens": 32768,  # Increased for larger content (portfolio section)
}


class TranslationError(Exception):
    """Custom exception for translation errors"""
    pass


def load_data() -> Dict[str, Any]:
    """
    Load data.json file

    Returns:
        Dict containing all language data

    Raises:
        FileNotFoundError: If data.json doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    print(f"📖 Loading data from {DATA_FILE}...")

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✅ Data loaded successfully ({len(data)} languages)")
    return data


def save_data(data: Dict[str, Any], backup: bool = True) -> None:
    """
    Save data to data.json with optional backup

    Args:
        data: Data dictionary to save
        backup: Whether to create a backup of the original file

    Raises:
        IOError: If file cannot be written
    """
    if backup:
        create_backup()

    print(f"💾 Saving data to {DATA_FILE}...")

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Data saved successfully")


def create_backup() -> None:
    """
    Create a timestamped backup of data.json
    """
    if not DATA_FILE.exists():
        print("⚠️  No data.json to backup")
        return

    # Create backup directory
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Generate backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"data_{timestamp}.json"

    # Copy file
    with open(DATA_FILE, 'r', encoding='utf-8') as src:
        with open(backup_file, 'w', encoding='utf-8') as dst:
            dst.write(src.read())

    print(f"💾 Backup created: {backup_file}")


def load_localization_prompt(language: str) -> str:
    """
    Load localization prompt for a specific language

    Args:
        language: Target language code (en, ja, ko, ar)

    Returns:
        Localization prompt string
    """
    prompts_dir = PROJECT_ROOT / "scripts" / "prompts"
    prompt_file = prompts_dir / f"{language}.txt"

    if not prompt_file.exists():
        print(f"⚠️  Prompt file not found: {prompt_file}, using default")
        return get_default_prompt(language)

    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()


def get_default_prompt(language: str) -> str:
    """
    Get default translation prompt for a language

    Args:
        language: Target language code

    Returns:
        Default prompt string
    """
    prompts = {
        "en": """You are a B2B marketing copywriter specializing in landing pages for tech education and consulting services.

## Target Audience Profile
- Age: 35-55, mid-senior managers in logistics, supply chain, manufacturing, retail
- Education: EMBA students from NCKU Transportation Management (Taiwan)
- Pain points: Budget constraints, need quick ROI, risk-averse, time-pressured
- Decision style: Value real cases over theory, prefer "try before buy" approach

## Translation Principles
1. **Content Type**: This is marketing copy (Landing Page), NOT a resume
   - Use persuasive language, not descriptive
   - Create emotional resonance with pain points
   - Include clear calls-to-action

2. **Writing Style**
   - Conversational and relatable (like talking to a colleague)
   - Short, punchy sentences with rhythm
   - Use specific numbers and contrasts for impact
   - Avoid corporate jargon and buzzwords

3. **Pain Point Amplification**
   - Make readers feel "Yes, that's exactly my problem!"
   - Use concrete scenarios and actions, not abstract concepts
   - Include emotional words: frustrating, tedious, time-consuming

4. **Keep Rhythm and Brevity**
   - Maintain the punch of original Chinese phrases
   - Example: "5天上線" → "Live in 5 days" (not "deployed within a 5-day timeframe")

5. **Trust Building**
   - Emphasize "Professor Lin's recommendation" (academic credibility)
   - Highlight "1200+ industry students" (social proof)
   - Use direct quotes when available

## Content-Specific Guidelines

**Hero Title**: Use questions or exclamations to create impact
**Case Studies**: Tell stories with empathy - show the struggle, then the relief
**Comparisons**: Use stark before/after contrasts with specific scenarios
**CTA**: Low-barrier, risk-free language ("Free consultation, no sales pressure")

## Technical Requirements
- Preserve all HTML tags and formatting exactly
- Keep technical terms in English (Claude Code, LINE Bot, etc.)
- Return valid JSON with same structure as input

Output format: Valid JSON ONLY, no markdown blocks or extra text.""",

        "ja": """あなたはB2B向けマーケティングコピーライターです。技術教育・コンサルティングサービスのランディングページ専門です。

## ターゲット読者
- 年齢: 35-55歳、物流・サプライチェーン・製造業の中堅管理職
- 学歴: 台湾・成功大学の交通管理EMBAの学生
- 課題: 予算制約、即効性重視、リスク回避、時間不足
- 意思決定: 理論より実例重視、「試してから決める」派

## 翻訳の原則
1. **コンテンツタイプ**: これはランディングページ（営業資料）であり、履歴書ではない
   - 説得力のある表現を使う（説明的ではなく）
   - 痛みに共感する表現で感情に訴える
   - 明確なCTA（行動喚起）を含める

2. **文体**
   - 「です・ます体」だが、過度な敬語は避ける（親しみやすさ重視）
   - 適度に口語表現を使い、親近感を出す
   - 短文でリズム感を保つ
   - ビジネス用語や横文字を避ける

3. **痛みの増幅**
   - 読者が「そう、それ！」と思う表現
   - 具体的なアクションと感情を入れる
   - 例: 「毎日2時間、Excelと格闘して疲弊」

4. **リズムと簡潔さ**
   - 中国語のパンチを維持
   - 例: 「5天上線」→「5日で稼働」（「5日間のデプロイ期間」ではなく）

5. **信頼構築**
   - 「林教授の推薦」を強調（学術的信頼）
   - 「1200名以上の実務家受講」（社会的証明）
   - 評価は直接引用する

## セクション別ガイドライン

**Hero Title（見出し）**: 疑問形や感嘆形でインパクトを
**Case Studies（事例）**: ストーリーで共感 - 苦労→安堵の流れ
**Comparisons（比較）**: ビフォー/アフターを鮮明に対比、具体的シーンで
**CTA（行動喚起）**: ハードルが低く、リスクフリーな表現

## 技術要件
- HTMLタグと書式を完全に保持
- 技術用語は英語のまま（Claude Code、LINE Bot等）
- 入力と同じ構造の有効なJSONを返す

出力形式: JSON のみ、マークダウンブロックや余分なテキストは不要。""",

        "ko": """당신은 B2B 마케팅 카피라이터입니다. 기술 교육 및 컨설팅 서비스의 랜딩 페이지 전문가입니다.

## 대상 독자
- 연령: 35-55세, 물류·공급망·제조업 중간관리자
- 학력: 대만 성공대학교 교통관리 EMBA 학생
- 고민: 예산 제약, 빠른 성과 필요, 리스크 회피, 시간 부족
- 의사결정: 이론보다 실제 사례 중시, "써보고 결정" 성향

## 번역 원칙
1. **콘텐츠 유형**: 이것은 랜딩 페이지(영업 자료)이지, 이력서가 아닙니다
   - 설득력 있는 표현 사용 (설명적이 아닌)
   - 고통에 공감하는 표현으로 감정 자극
   - 명확한 CTA(행동 유도) 포함

2. **문체**
   - "해요체" 사용 (전문적이면서 친근함)
   - 과도하게 격식 차린 표현 피하기
   - 현대적인 구어체 적절히 활용
   - 짧은 문장으로 리듬감 유지
   - 한자어보다 쉬운 순우리말 선호

3. **고통 증폭**
   - 독자가 "맞아, 바로 이거야!"라고 느끼게
   - 구체적인 행동과 감정 포함
   - 예: "매일 2시간씩 엑셀 정리에 지쳐 쓰러질 것 같아요"

4. **리듬과 간결함**
   - 중국어의 펀치 유지
   - 예: "5天上線" → "5일 만에 오픈" ("5일간의 배포 기간"이 아님)

5. **신뢰 구축**
   - "린 교수 추천" 강조 (학술적 신뢰)
   - "1200명 이상의 실무자 수강" (사회적 증명)
   - 평가는 직접 인용

## 섹션별 가이드라인

**Hero Title (제목)**: 의문형이나 감탄형으로 임팩트
**Case Studies (사례)**: 스토리로 공감 - 고생 → 해결의 흐름
**Comparisons (비교)**: Before/After 극명하게 대비, 구체적 장면으로
**CTA (행동 유도)**: 부담 없고 리스크 제로인 표현

## 기술 요구사항
- HTML 태그와 형식 완전히 보존
- 기술 용어는 영어 그대로 (Claude Code, LINE Bot 등)
- 입력과 동일한 구조의 유효한 JSON 반환

출력 형식: JSON만, 마크다운 블록이나 추가 텍스트 없이.""",

        "ar": """أنت كاتب محتوى تسويقي B2B متخصص في الصفحات المقصودة لخدمات التعليم التقني والاستشارات.

## الجمهور المستهدف
- العمر: 35-55 سنة، مديرون في الخدمات اللوجستية وسلسلة الإمداد والتصنيع
- التعليم: طلاب EMBA من جامعة تشنغ كونغ الوطنية - قسم إدارة النقل (تايوان)
- التحديات: قيود الميزانية، حاجة لنتائج سريعة، تجنب المخاطر، ضغط الوقت
- أسلوب القرار: تفضيل الحالات الواقعية على النظرية، نهج "جرب قبل أن تقرر"

## مبادئ الترجمة
1. **نوع المحتوى**: هذه صفحة مقصودة (مواد تسويقية)، وليست سيرة ذاتية
   - استخدم لغة مقنعة، وليست وصفية
   - أنشئ صدى عاطفي مع نقاط الألم
   - ضمّن دعوات واضحة لاتخاذ إجراء

2. **الأسلوب**
   - محادثة وقريبة (كأنك تتحدث مع زميل)
   - جمل قصيرة ذات إيقاع
   - استخدم أرقام محددة وتباينات للتأثير
   - تجنب المصطلحات الشركاتية والكلمات الطنانة

3. **تضخيم نقاط الألم**
   - اجعل القراء يشعرون "نعم، هذه بالضبط مشكلتي!"
   - استخدم سيناريوهات وإجراءات ملموسة، وليس مفاهيم مجردة
   - ضمّن كلمات عاطفية: محبط، مُمل، يستهلك الوقت

4. **الحفاظ على الإيقاع والإيجاز**
   - حافظ على قوة العبارات الصينية الأصلية
   - مثال: "5天上線" → "مباشر في 5 أيام" (وليس "نشر خلال إطار زمني 5 أيام")

5. **بناء الثقة**
   - أكد على "توصية البروفيسور لين" (مصداقية أكاديمية)
   - أبرز "أكثر من 1200 طالب من الصناعة" (إثبات اجتماعي)
   - استخدم الاقتباسات المباشرة عند توفرها

## إرشادات حسب نوع المحتوى

**عنوان البطل**: استخدم أسئلة أو تعجبات لإحداث تأثير
**دراسات الحالة**: احكِ قصصاً بتعاطف - أظهر النضال، ثم الراحة
**المقارنات**: استخدم تباينات قبل/بعد صارخة مع سيناريوهات محددة
**الدعوة لاتخاذ إجراء**: لغة منخفضة الحاجز، خالية من المخاطر

## المتطلبات التقنية
- احفظ جميع علامات HTML والتنسيق بدقة
- احتفظ بالمصطلحات التقنية بالإنجليزية (Claude Code، LINE Bot، إلخ)
- استخدم الأرقام الغربية (1, 2, 3) وليس الأرقام العربية الشرقية
- أرجع JSON صالح بنفس البنية

تنسيق الإخراج: JSON فقط، بدون كتل markdown أو نص إضافي."""
    }

    return prompts.get(language, prompts["en"])


def translate_with_gemini(content: Dict[str, Any], target_lang: str) -> Dict[str, Any]:
    """
    Translate content using Gemini 2.5 Flash API

    Args:
        content: Dictionary containing zh-TW content
        target_lang: Target language code (en, ja, ko, ar)

    Returns:
        Translated content dictionary

    Raises:
        TranslationError: If translation fails
    """
    # Initialize Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise TranslationError("GEMINI_API_KEY not found in environment variables")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)

    # Load localization prompt
    localization_prompt = load_localization_prompt(target_lang)

    # Prepare content for translation
    content_json = json.dumps(content, ensure_ascii=False, indent=2)

    # Construct full prompt
    full_prompt = f"""{localization_prompt}

Source content (Traditional Chinese):
```json
{content_json}
```

Translate the above JSON to {target_lang}. Return ONLY the translated JSON, nothing else."""

    print(f"🤖 Translating to {target_lang} using Gemini {GEMINI_MODEL}...")

    try:
        # Call Gemini API
        response = model.generate_content(
            full_prompt,
            generation_config=GENERATION_CONFIG
        )

        # Extract response text
        response_text = response.text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove trailing ```

        response_text = response_text.strip()

        # Parse JSON
        translated_content = json.loads(response_text)

        print(f"✅ Translation to {target_lang} completed")
        return translated_content

    except json.JSONDecodeError as e:
        raise TranslationError(f"Failed to parse Gemini response as JSON: {e}\nResponse: {response_text[:200]}")
    except Exception as e:
        raise TranslationError(f"Gemini API error: {e}")


def validate_translation(original: Dict[str, Any], translated: Dict[str, Any]) -> bool:
    """
    Validate translation structure matches original

    Args:
        original: Original zh-TW content
        translated: Translated content

    Returns:
        True if structure is valid

    Raises:
        TranslationError: If validation fails
    """
    def get_keys_recursive(obj: Any, prefix: str = "") -> set:
        """Recursively get all keys from nested dict/list"""
        keys = set()

        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{prefix}.{key}" if prefix else key
                keys.add(full_key)
                keys.update(get_keys_recursive(value, full_key))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                keys.update(get_keys_recursive(item, f"{prefix}[{i}]"))

        return keys

    original_keys = get_keys_recursive(original)
    translated_keys = get_keys_recursive(translated)

    missing_keys = original_keys - translated_keys
    extra_keys = translated_keys - original_keys

    if missing_keys:
        raise TranslationError(f"Missing keys in translation: {missing_keys}")

    if extra_keys:
        print(f"⚠️  Extra keys in translation (may be OK): {extra_keys}")

    print(f"✅ Structure validation passed")
    return True


def main():
    """Main execution function"""
    print("=" * 60)
    print("🌐 Cruz Resume Translation Script")
    print("=" * 60)

    try:
        # Load existing data
        data = load_data()

        # Check if zh-TW exists
        if "zh-TW" not in data:
            raise TranslationError("zh-TW source content not found in data.json")

        zh_tw_content = data["zh-TW"]
        print(f"📝 Source language: zh-TW ({len(zh_tw_content)} sections)")

        # Translate to each target language
        for lang in TARGET_LANGUAGES:
            print(f"\n{'=' * 60}")
            print(f"🌍 Processing language: {lang}")
            print(f"{'=' * 60}")

            try:
                # Translate
                translated_content = translate_with_gemini(zh_tw_content, lang)

                # Validate
                validate_translation(zh_tw_content, translated_content)

                # Update data
                data[lang] = translated_content
                print(f"✅ {lang} translation completed and validated")

            except TranslationError as e:
                print(f"❌ Error translating to {lang}: {e}")
                print(f"⏭️  Skipping {lang}, keeping existing content")
                continue

        # Save updated data
        save_data(data, backup=True)

        print(f"\n{'=' * 60}")
        print("✅ Translation completed successfully!")
        print(f"{'=' * 60}")
        print(f"📊 Updated languages: {', '.join(TARGET_LANGUAGES)}")
        print(f"💾 Backup saved to: {BACKUP_DIR}")

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
