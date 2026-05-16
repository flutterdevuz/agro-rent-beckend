import hashlib
from django.core.cache import cache
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

def translate_text(text, target_lang='uz'):
    """
    Translates text to the target language.
    Uses caching to avoid redundant API calls.
    """
    if not text or not isinstance(text, str):
        return text

    # Handle language codes like 'en-US' or 'uz-UZ'
    target_lang = target_lang.split('-')[0].lower()

    # Create a cache key based on text and target language
    text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    cache_key = f"trans_{text_hash}_{target_lang}"
    
    cached_val = cache.get(cache_key)
    if cached_val:
        return cached_val

    try:
        # Detect source language
        try:
            source_lang = detect(text)
        except:
            source_lang = 'auto'

        if source_lang == target_lang:
            return text

        # Translate
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        
        # Cache the result for 24 hours
        cache.set(cache_key, translated, 60 * 60 * 24)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text
