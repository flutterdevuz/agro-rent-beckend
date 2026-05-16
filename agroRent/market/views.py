from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from market.models import Category, MarketItem, MarketOrder
from market.serializers import CategorySerializer, MarketItemSerializer, MarketOrderSerializer
from users.permissions import IsRenter, IsOwnerAndRenterOrReadOnly

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class MarketItemCreateView(generics.CreateAPIView):
    queryset = MarketItem.objects.all()
    serializer_class = MarketItemSerializer
    permission_classes = [IsAuthenticated, IsRenter]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class MarketItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarketItem.objects.all()
    serializer_class = MarketItemSerializer
    permission_classes = [IsOwnerAndRenterOrReadOnly]

class MarketItemMeView(generics.ListAPIView):
    serializer_class = MarketItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MarketItem.objects.filter(seller=self.request.user).order_by('-created_at')

class MarketOrderCreateView(generics.CreateAPIView):
    queryset = MarketOrder.objects.all()
    serializer_class = MarketOrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
