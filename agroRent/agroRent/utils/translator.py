import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

from django.core.cache import cache
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)

CACHE_TTL = 60 * 60 * 24 * 30      # Tarjimalar 30 kun saqlanadi
BLOCK_KEY = 'translate_blocked'
BLOCK_TTL = 120                     # Google xato bersa, 2 daqiqa tarjimasiz ishlaymiz
REQUEST_TIMEOUT = 5                 # Bitta Google so'rovi uchun maksimal kutish (soniya)
CHUNK_CHARS = 1500                  # Bir so'rovga yig'iladigan matn hajmi (URL uzunligi cheklovi)
MAX_TEXT_CHARS = 4500               # Bundan uzun matnlar tarjima qilinmaydi (Google limiti 5000)

# deep_translator so'rovlarga timeout qo'ymaydi, shuning uchun alohida oqimda chaqiramiz
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix='translate')


class _TranslationUnavailable(Exception):
    pass


def _normalize_lang(lang):
    return (lang or 'uz').split('-')[0].lower()


def _cache_key(text, lang):
    return f"trans_{hashlib.md5(text.encode('utf-8')).hexdigest()}_{lang}"


def _google(translator, text):
    future = _executor.submit(translator.translate, text)
    try:
        return future.result(timeout=REQUEST_TIMEOUT)
    except FutureTimeout:
        raise _TranslationUnavailable('timeout')
    except Exception as e:
        raise _TranslationUnavailable(str(e))


def _is_same_language(text, lang):
    try:
        return detect(text) == lang
    except Exception:
        return False


def translate_many(texts, target_lang='uz'):
    """
    Matnlar ro'yxatini tarjima qiladi va {asl_matn: tarjima} lug'atini qaytaradi.

    - Natijalar umumiy keshda saqlanadi, shuning uchun bir matn faqat bir marta tarjima qilinadi.
    - Bir qatorli matnlar bitta so'rovga yig'ib yuboriladi (Google limitiga tushmaslik uchun).
    - Google xato bersa yoki javob bermasa, 2 daqiqa davomida tarjimasiz ishlaymiz,
      shunda sahifa sekinlashmaydi.
    """
    lang = _normalize_lang(target_lang)
    results = {}
    unique = []
    for text in texts:
        if not text or not isinstance(text, str):
            results[text] = text
        elif text not in results:
            results[text] = text  # Standart qiymat: tarjima bo'lmasa asl matn
            unique.append(text)

    if not unique:
        return results

    keys = {text: _cache_key(text, lang) for text in unique}
    cached = cache.get_many(list(keys.values()))
    pending = []
    for text in unique:
        if keys[text] in cached:
            results[text] = cached[keys[text]]
        else:
            pending.append(text)

    if not pending or cache.get(BLOCK_KEY):
        return results

    to_cache = {}
    to_translate = []
    for text in pending:
        if len(text) > MAX_TEXT_CHARS or _is_same_language(text, lang):
            to_cache[keys[text]] = text
        else:
            to_translate.append(text)

    try:
        translator = GoogleTranslator(source='auto', target=lang)
    except Exception:
        # Qo'llab-quvvatlanmaydigan til: asl matnni qaytaramiz va qayta urinmaymiz
        to_cache.update({keys[t]: t for t in to_translate})
        cache.set_many(to_cache, CACHE_TTL)
        return results

    single_line = [t for t in to_translate if '\n' not in t]
    multi_line = [t for t in to_translate if '\n' in t]

    # Bir qatorli matnlarni guruhlab, har bir guruh uchun bitta so'rov
    chunks, chunk, size = [], [], 0
    for text in single_line:
        if chunk and size + len(text) > CHUNK_CHARS:
            chunks.append(chunk)
            chunk, size = [], 0
        chunk.append(text)
        size += len(text) + 1
    if chunk:
        chunks.append(chunk)

    try:
        for chunk in chunks:
            translated = _google(translator, '\n'.join(chunk))
            lines = [line.strip() for line in (translated or '').split('\n')]
            if len(lines) == len(chunk):
                for original, value in zip(chunk, lines):
                    to_cache[keys[original]] = value or original
            else:
                # Google qatorlarni birlashtirib yuborsa, bittalab tarjima qilamiz
                multi_line.extend(chunk)

        for text in multi_line:
            to_cache[keys[text]] = _google(translator, text) or text
    except _TranslationUnavailable as e:
        logger.warning("Translation unavailable, pausing for %ss: %s", BLOCK_TTL, e)
        cache.set(BLOCK_KEY, True, BLOCK_TTL)

    if to_cache:
        cache.set_many(to_cache, CACHE_TTL)
        for text in pending:
            if keys[text] in to_cache:
                results[text] = to_cache[keys[text]]

    return results


def translate_text(text, target_lang='uz'):
    """Bitta matnni tarjima qiladi (kesh bilan)."""
    if not text or not isinstance(text, str):
        return text
    return translate_many([text], target_lang)[text]


def translate_texts_batch(texts, target_lang='uz'):
    """TranslateView uchun: {asl_matn: tarjima} lug'ati."""
    return translate_many(texts, target_lang)
