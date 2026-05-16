from rest_framework import serializers
from users.models import User, ResetPasswordRequest
from rent.models import RentItem, RentOrder
from market.models import MarketItem, MarketOrder
from agroRent.utils.mixins import TranslatableSerializerMixin

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    isRenter = serializers.BooleanField(source='is_renter', default=False)

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'region', 'district', 'mfy', 'password', 'isRenter')

    def validate_phone_number(self, value):
        # Remove spaces and common separators
        return value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

    def create(self, validated_data):
        is_renter = validated_data.pop('is_renter', False)
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            region=validated_data['region'],
            district=validated_data['district'],
            mfy=validated_data['mfy'],
            is_renter=is_renter
        )
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, value):
        # Remove spaces and common separators
        return value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordRequest
        fields = ('phone_number', 'description')

class UserSerializer(TranslatableSerializerMixin, serializers.ModelSerializer):
    isRenter = serializers.BooleanField(source='is_renter', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'region', 'district', 'mfy', 'rating', 'isRenter', 'is_staff', 'is_superuser')
        translatable_fields = ['district', 'mfy']

class ProfileSerializer(TranslatableSerializerMixin, serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()
    equipment_count = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'order_count', 'rating', 'equipment_count', 'location')
        translatable_fields = ['location']

    def get_order_count(self, obj) -> int:
        return RentOrder.objects.filter(user=obj).count() + MarketOrder.objects.filter(user=obj).count()

    def get_equipment_count(self, obj) -> int:
        return RentItem.objects.filter(owner=obj).count() + MarketItem.objects.filter(seller=obj).count()

    def get_location(self, obj) -> str:
        # Note: translate_text will be called on the final string by the mixin
        return f"{obj.get_region_display()}, {obj.district}, {obj.mfy}"

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'region', 'district', 'mfy', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class UnifiedOrderSerializer(TranslatableSerializerMixin, serializers.Serializer):
    id = serializers.UUIDField()
    type = serializers.CharField() # 'rent' or 'market'
    name = serializers.CharField()
    image = serializers.ImageField()
    size = serializers.CharField(required=False)
    date_time = serializers.DateTimeField()
    status = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    
    class Meta:
        translatable_fields = ['name', 'status']
