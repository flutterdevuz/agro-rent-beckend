from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from market.models import Category, MarketItem, MarketOrder
from market.serializers import CategorySerializer, MarketItemSerializer, MarketOrderSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MarketItemListView(generics.ListCreateAPIView):
    queryset = MarketItem.objects.all().order_by('-created_at')
    serializer_class = MarketItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'location': ['icontains'],
        'price': ['gte', 'lte'],
        'condition': ['exact'],
        'rating': ['gte'],
        'has_delivery': ['exact'],
        'category': ['exact'],
    }
    search_fields = ['name', 'brand', 'model', 'description']
    ordering_fields = ['price', 'rating', 'created_at', 'likes_count']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class MarketItemCreateView(generics.CreateAPIView):
    queryset = MarketItem.objects.all()
    serializer_class = MarketItemSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class MarketItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarketItem.objects.all()
    serializer_class = MarketItemSerializer

class MarketOrderCreateView(generics.CreateAPIView):
    queryset = MarketOrder.objects.all()
    serializer_class = MarketOrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
