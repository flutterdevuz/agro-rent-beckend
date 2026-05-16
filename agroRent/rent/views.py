from rest_framework import generics, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rent.models import RentItem, RentOrder
from rent.serializers import RentItemSerializer, RentItemCreateSerializer, RentOrderSerializer
from users.permissions import IsRenter, IsOwnerAndRenterOrReadOnly

class RentItemListView(generics.ListCreateAPIView):
    queryset = RentItem.objects.all().order_by('-created_at')
    serializer_class = RentItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'equipment_name': ['icontains'],
        'region': ['icontains'],
        'condition': ['exact'],
        'hp': ['gte', 'lte'],
        'rating': ['gte'],
        'price': ['gte', 'lte'],
    }
    search_fields = ['name', 'equipment_name', 'brand']
    ordering_fields = ['price', 'rating', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RentItemCreateSerializer
        return RentItemSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RentItemCreateView(generics.CreateAPIView):
    queryset = RentItem.objects.all()
    serializer_class = RentItemCreateSerializer
    permission_classes = [IsAuthenticated, IsRenter]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RentItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RentItem.objects.all()
    serializer_class = RentItemSerializer
    permission_classes = [IsOwnerAndRenterOrReadOnly]

class RentItemMeView(generics.ListAPIView):
    serializer_class = RentItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RentItem.objects.filter(owner=self.request.user).order_by('-created_at')

class RentOrderCreateView(generics.CreateAPIView):
    queryset = RentOrder.objects.all()
    serializer_class = RentOrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
