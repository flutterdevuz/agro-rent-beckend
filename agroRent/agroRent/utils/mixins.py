from rest_framework import serializers

from .translator import translate_many

_QUEUE_ATTR = '_translation_queue'


def _start_queue(request):
    """Navbatni boshlaydi. True qaytarsa, navbat egasi shu chaqiruv."""
    if request is None or getattr(request, _QUEUE_ATTR, None) is not None:
        return False
    setattr(request, _QUEUE_ATTR, [])
    return True


def _flush_queue(request):
    """Yig'ilgan barcha maydonlarni bitta to'plam qilib tarjima qiladi."""
    queue = getattr(request, _QUEUE_ATTR)
    delattr(request, _QUEUE_ATTR)
    if not queue:
        return
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    translations = translate_many([data[field] for data, field in queue], lang)
    for data, field in queue:
        data[field] = translations.get(data[field], data[field])


class TranslatableListSerializer(serializers.ListSerializer):
    """Ro'yxatdagi barcha obyektlar matnlarini bitta to'plamda tarjima qiladi."""
    def to_representation(self, data):
        request = self.context.get('request')
        owner = _start_queue(request)
        try:
            result = super().to_representation(data)
        except Exception:
            if owner:
                delattr(request, _QUEUE_ATTR)
            raise
        if owner:
            _flush_queue(request)
        return result


class TranslatableSerializerMixin:
    """
    Mixin to automatically translate specified fields in a serializer.
    The serializer should define 'translatable_fields' in its Meta class.

    Maydonlar darhol tarjima qilinmaydi: javobdagi barcha matnlar (ichma-ich
    serializerlar ham) yig'iladi va bitta to'plam qilib tarjima qilinadi.
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        meta = getattr(cls, 'Meta', None)
        if meta is not None and not hasattr(meta, 'list_serializer_class'):
            meta.list_serializer_class = TranslatableListSerializer

    def to_representation(self, instance):
        request = self.context.get('request')
        owner = _start_queue(request)
        try:
            data = super().to_representation(instance)
        except Exception:
            if owner:
                delattr(request, _QUEUE_ATTR)
            raise
        if request is None:
            return data

        meta = getattr(self, 'Meta', None)
        queue = getattr(request, _QUEUE_ATTR)
        for field in getattr(meta, 'translatable_fields', []):
            if isinstance(data.get(field), str) and data[field]:
                queue.append((data, field))

        if owner:
            _flush_queue(request)
        return data
