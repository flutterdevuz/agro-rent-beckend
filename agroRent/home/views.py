from django.db.models import Count, Q
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from home.models import HomeContent
from rest_framework.views import APIView
from rest_framework.response import Response
from agroRent.utils.translator import translate_text, translate_texts_batch
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
    permission_classes = [AllowAny]

    def post(self, request):
        texts = request.data.get('texts', [])
        # Tilni request body'dan ol, keyin header'dan, default uz
        target_lang = request.data.get('lang') or request.headers.get('Accept-Language', 'uz').split(',')[0].strip().split('-')[0]

        # uz_cyrl uchun maxsus handling
        lang_map = {
            'uz_cyrl': 'uz',  # Google Translate uz ni ishlatadi
            'uz-cyrl': 'uz',
        }
        target_lang = lang_map.get(target_lang, target_lang)

        # Agar texts bo'sh bo'lsa
        if not texts:
            return Response({})

        translations = translate_texts_batch(texts, target_lang)

        return Response(translations)
