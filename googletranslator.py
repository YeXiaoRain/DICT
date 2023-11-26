# write by chatgpt3.5
import argparse
from googletrans import Translator

def google_translator(original_text):
    def detect_language(text):
        translator = Translator()
        result = translator.detect(text)
        return result.lang

    def translate_text(text, target_language='en'):
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    # Detect source language
    source_language = detect_language(original_text)
    print(f"Source Language: {source_language}")

    # Translate text
    if source_language == 'zh-CN':
        target_language = 'en'
    else:
        target_language = 'zh-CN'

    translated_text = translate_text(original_text, target_language)
    print(f"Google Translation: {translated_text}")

def main():
    parser = argparse.ArgumentParser(description='Translate text between Chinese and English.')
    parser.add_argument('text', nargs='+', help='The text to translate, multiple words are accepted.')

    args = parser.parse_args()
    original_text = ' '.join(args.text)
    google_translator(original_text)


if __name__ == "__main__":
    main()
