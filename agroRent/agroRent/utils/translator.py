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

def translate_texts_batch(texts, target_lang='uz'):
    """
    Translates a list of texts to the target language efficiently.
    Uses caching and batching to avoid API limits.
    """
    if not texts:
        return {}

    target_lang = target_lang.split('-')[0].lower()
    
    results = {}
    uncached_texts = []
    text_to_cache_key = {}

    for text in texts:
        if not text or not isinstance(text, str):
            results[text] = text
            continue
            
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        cache_key = f"trans_{text_hash}_{target_lang}"
        text_to_cache_key[text] = cache_key
        
        cached_val = cache.get(cache_key)
        if cached_val:
            results[text] = cached_val
        else:
            uncached_texts.append(text)

    if uncached_texts:
        try:
            # Barcha so'zlarni 1 ta requestga birlashtiramiz (Google limitiga tushmaslik uchun)
            # Google Translate HTML taglarni olib tashlashi mumkin, shuning uchun \n (yangi qator) ishlatamiz
            separator = " \n "
            combined_text = separator.join(uncached_texts)
            
            # Faqat 1 ta API call ketadi!
            translated_combined = GoogleTranslator(source='auto', target=target_lang).translate(combined_text)
            
            # Qaytib ajratib olamiz
            translated_batch = [t.strip() for t in translated_combined.split('\n')]
            
            # Uzunligi to'g'riligini tekshirib keshga yozamiz
            if len(translated_batch) == len(uncached_texts):
                for original, translated in zip(uncached_texts, translated_batch):
                    results[original] = translated
                    cache.set(text_to_cache_key[original], translated, 60 * 60 * 24)
            else:
                # Agar Google qatorlarni buzib yuborsa (kamdan-kam hollarda), sekin tarjimaga qaytamiz
                print(f"Translation mismatch: expected {len(uncached_texts)} but got {len(translated_batch)}")
                for original in uncached_texts:
                    results[original] = original
                    
        except Exception as e:
            print(f"Batch Translation error: {e}")
            for text in uncached_texts:
                results[text] = text

    return results
