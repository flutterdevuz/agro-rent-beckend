from rest_framework import serializers
from home.models import (
    HomeContent, SiteText, WebsiteSettings, WebsiteService,
    WebsitePartner, WebsiteStep, WebsiteBenefit, WebsiteOrder
)
from agroRent.utils.mixins import TranslatableSerializerMixin

class HomeContentSerializer(TranslatableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = HomeContent
        fields = '__all__'
        read_only_fields = ('content_type',)
        translatable_fields = ['name', 'description']

class SiteTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteText
        fields = '__all__'


# =========================================================================
# WEBSITE SERIALIZERS
# =========================================================================

class WebsiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteSettings
        fields = '__all__'


class WebsiteServiceSerializer(serializers.ModelSerializer):
    image_display_url = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = WebsiteService
        fields = '__all__'

    def get_image_display_url(self, obj):
        return obj.get_image_url()

    def to_internal_value(self, data):
        # Agar image bo'sh kelsa yoki string bo'lsa, uni o'chiramiz
        if hasattr(data, '_mutable'):
            data = data.copy()
        if 'image' in data and not data['image']:
            data.pop('image', None)
        return super().to_internal_value(data)


class WebsitePartnerSerializer(serializers.ModelSerializer):
    photo_display_url = serializers.SerializerMethodField()
    member_type_display = serializers.CharField(source='get_member_type_display', read_only=True)
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = WebsitePartner
        fields = '__all__'

    def get_photo_display_url(self, obj):
        return obj.get_photo_url()

    def to_internal_value(self, data):
        # Agar photo bo'sh kelsa yoki string bo'lsa, uni o'chiramiz
        if hasattr(data, '_mutable'):
            data = data.copy()
        if 'photo' in data and not data['photo']:
            data.pop('photo', None)
        return super().to_internal_value(data)


class WebsiteStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteStep
        fields = '__all__'


class WebsiteBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteBenefit
        fields = '__all__'


class WebsiteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteOrder
        fields = '__all__'
        read_only_fields = ('created_at',)
