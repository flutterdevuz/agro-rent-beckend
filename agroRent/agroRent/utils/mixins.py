from .translator import translate_text

class TranslatableSerializerMixin:
    """
    Mixin to automatically translate specified fields in a serializer.
    The serializer should define 'translatable_fields' in its Meta class.
    """
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Get target language from request
        request = self.context.get('request')
        if not request:
            return data
            
        target_lang = getattr(request, 'LANGUAGE_CODE', 'uz')
        
        # Get fields to translate from Meta
        meta = getattr(self, 'Meta', None)
        translatable_fields = getattr(meta, 'translatable_fields', [])
        
        if not translatable_fields:
            return data

        for field in translatable_fields:
            if field in data and data[field]:
                data[field] = translate_text(data[field], target_lang)
                
        return data
