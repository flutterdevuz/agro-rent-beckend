from rest_framework import serializers
from rent.models import RentItem, RentImage, RentOrder
from users.serializers import UserSerializer
from agroRent.utils.mixins import TranslatableSerializerMixin

class RentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentImage
        fields = ('id', 'image')

class RentItemSerializer(TranslatableSerializerMixin, serializers.ModelSerializer):
    images = RentImageSerializer(many=True, read_only=True)
    owner_details = UserSerializer(source='owner', read_only=True)
    
    class Meta:
        model = RentItem
        fields = '__all__'
        read_only_fields = ('owner', 'rating', 'created_at')
        translatable_fields = ['name', 'equipment_name', 'brand', 'condition', 'location_name']

class RentItemCreateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = RentItem
        fields = (
            'id', 'name', 'equipment_name', 'brand', 'hp', 'condition', 
            'price', 'is_agreement', 'region', 'location_name', 
            'latitude', 'longitude', 'uploaded_images'
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        rent_item = RentItem.objects.create(**validated_data)
        for image in uploaded_images:
            RentImage.objects.create(rent_item=rent_item, image=image)
        return rent_item

class RentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentOrder
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
