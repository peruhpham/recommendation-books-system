import langid
from deep_translator import GoogleTranslator

def detect_language(text):
    detected_lang, confidence = langid.classify(text)
    return detected_lang

def translate_vi_to_en(text):
    detected_lang = detect_language(text)
    if detected_lang == "vi":
        return GoogleTranslator(source='vi', target='en').translate(text)
    return text

def translate_en_to_vi(text):
    detected_lang = detect_language(text)
    if detected_lang == "en":
        return GoogleTranslator(source='en', target='vi').translate(text)
    else:
        return text