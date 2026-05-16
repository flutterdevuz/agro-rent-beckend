from rest_framework import serializers
from home.models import HomeContent

class HomeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeContent
        fields = '__all__'
        read_only_fields = ('content_type',)
