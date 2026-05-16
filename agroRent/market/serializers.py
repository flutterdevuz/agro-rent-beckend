from rest_framework import serializers
from market.models import Category, MarketItem, MarketOrder
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at')

class MarketItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_details = UserSerializer(source='seller', read_only=True)

    class Meta:
        model = MarketItem
        fields = '__all__'
        read_only_fields = ('seller', 'rating', 'likes_count', 'created_at')

class MarketOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
