from rest_framework import serializers
from home.models import HomeContent
from agroRent.utils.mixins import TranslatableSerializerMixin

class HomeContentSerializer(TranslatableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = HomeContent
        fields = '__all__'
        read_only_fields = ('content_type',)
        translatable_fields = ['name', 'description']
