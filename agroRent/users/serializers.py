from rest_framework import serializers
from users.models import User, ResetPasswordRequest
from rent.models import RentItem, RentOrder
from market.models import MarketItem, MarketOrder

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'region', 'district', 'mfy', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            region=validated_data['region'],
            district=validated_data['district'],
            mfy=validated_data['mfy']
        )
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordRequest
        fields = ('phone_number', 'description')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'region', 'district', 'mfy', 'rating')

class ProfileSerializer(serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()
    equipment_count = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'order_count', 'rating', 'equipment_count', 'location')

    def get_order_count(self, obj):
        return RentOrder.objects.filter(user=obj).count() + MarketOrder.objects.filter(user=obj).count()

    def get_equipment_count(self, obj):
        return RentItem.objects.filter(owner=obj).count() + MarketItem.objects.filter(seller=obj).count()

    def get_location(self, obj):
        return f"{obj.region}, {obj.district}, {obj.mfy}"

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

class UnifiedOrderSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    type = serializers.CharField() # 'rent' or 'market'
    name = serializers.CharField()
    image = serializers.ImageField()
    size = serializers.CharField(required=False)
    date_time = serializers.DateTimeField()
    status = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
