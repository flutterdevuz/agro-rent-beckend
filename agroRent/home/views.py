from django.db.models import Count, Q
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from home.models import HomeContent
from rest_framework.views import APIView
from rest_framework.response import Response
from agroRent.utils.translator import translate_text
from home.serializers import HomeContentSerializer

class BannerListView(generics.ListCreateAPIView):
    serializer_class = HomeContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HomeContent.objects.filter(content_type='banner').order_by('-id')

    def perform_create(self, serializer):
        serializer.save(content_type='banner')

from django.db.models import Count
from market.models import MarketItem
from market.serializers import MarketItemSerializer

class PopularEquipmentListView(generics.ListAPIView):
    serializer_class = MarketItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MarketItem.objects.annotate(
            order_count=Count('orders')
        ).order_by('-order_count', '-created_at')[:10]

class HomeContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeContent.objects.all()
    serializer_class = HomeContentSerializer
    permission_classes = [IsAuthenticated]

class PublicHomeView(TemplateView):
    template_name = 'public/home.html'

class PublicMarketView(TemplateView):
    template_name = 'public/market.html'

class PublicRentView(TemplateView):
    template_name = 'public/rent.html'

class PublicAboutView(TemplateView):
    template_name = 'public/about.html'

class PublicProfileView(TemplateView):
    template_name = 'public/profile.html'

class PublicRentDetailView(TemplateView):
    template_name = 'public/rent_detail.html'

def handle_404(request, exception):
    from django.shortcuts import render
    return render(request, '404.html', status=404)

class TranslateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        texts = request.data.get('texts', [])
        target_lang = request.LANGUAGE_CODE or 'uz'
        
        translations = {}
        for text in texts:
            translations[text] = translate_text(text, target_lang)
            
        return Response(translations)
