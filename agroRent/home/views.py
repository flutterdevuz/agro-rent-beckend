from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from home.models import HomeContent
from home.serializers import HomeContentSerializer

class BannerListView(generics.ListCreateAPIView):
    serializer_class = HomeContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HomeContent.objects.filter(content_type='banner')

    def perform_create(self, serializer):
        serializer.save(content_type='banner')

class PopularEquipmentListView(generics.ListAPIView):
    serializer_class = HomeContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HomeContent.objects.filter(content_type='popular_equipment')

class HomeContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeContent.objects.all()
    serializer_class = HomeContentSerializer
    permission_classes = [IsAuthenticated]
