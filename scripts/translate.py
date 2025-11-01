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
GEMINI_MODEL = "gemini-2.0-flash-exp"
GENERATION_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.95,
    "max_output_tokens": 8192,
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
        "en": """You are a professional translator for a multilingual resume website.
Translate the following Traditional Chinese content to English.

Guidelines:
- Keep technical terms in English (e.g., "Claude Code", "AI-Native")
- Maintain professional tone suitable for enterprise audiences
- Preserve HTML tags and formatting exactly as is
- Use active voice and concise language
- Target audience: International recruiters and enterprise clients

Output format: Valid JSON with the same structure as input
IMPORTANT: Return ONLY the JSON, no markdown code blocks or extra text.""",

        "ja": """あなたは多言語履歴書ウェブサイトの専門翻訳者です。
以下の繁体字中国語コンテンツを日本語に翻訳してください。

ガイドライン:
- 技術用語は英語のまま保持（例：「Claude Code」、「AI-Native」）
- ビジネス文書として適切な敬語を使用
- HTMLタグとフォーマットを正確に保持
- ターゲット読者: 日本企業の採用担当者および意思決定者

出力形式: 入力と同じ構造の有効なJSON
重要: JSONのみを返してください。マークダウンのコードブロックや余分なテキストは不要です。""",

        "ko": """당신은 다국어 이력서 웹사이트의 전문 번역가입니다.
다음 번체 중국어 콘텐츠를 한국어로 번역하세요.

가이드라인:
- 기술 용어는 영어로 유지 (예: "Claude Code", "AI-Native")
- 기업 대상으로 적절한 전문적인 어조 유지
- HTML 태그와 형식을 정확히 보존
- 대상 독자: 한국 기업의 채용 담당자 및 의사 결정권자

출력 형식: 입력과 동일한 구조의 유효한 JSON
중요: JSON만 반환하세요. 마크다운 코드 블록이나 추가 텍스트는 필요하지 않습니다.""",

        "ar": """أنت مترجم محترف لموقع سيرة ذاتية متعدد اللغات.
قم بترجمة المحتوى التالي من الصينية التقليدية إلى العربية.

إرشادات:
- احتفظ بالمصطلحات التقنية بالإنجليزية (مثل "Claude Code", "AI-Native")
- استخدم لغة مهنية مناسبة للعملاء من الشركات
- احتفظ بعلامات HTML والتنسيق بدقة
- القراء المستهدفون: مسؤولو التوظيف وصناع القرار في الشركات

تنسيق الإخراج: JSON صالح بنفس هيكل الإدخال
مهم: أرجع JSON فقط، بدون كتل تعليمات برمجية markdown أو نص إضافي."""
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
