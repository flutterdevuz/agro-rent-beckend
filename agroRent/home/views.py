from django.db.models import Count, Q
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from home.models import HomeContent
from rest_framework.views import APIView
from rest_framework.response import Response
from agroRent.utils.translator import translate_text, translate_texts_batch
from home.serializers import HomeContentSerializer
from market.models import MarketItem
from market.serializers import MarketItemSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers

class BannerListView(generics.ListCreateAPIView):
    serializer_class = HomeContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HomeContent.objects.filter(content_type='banner').order_by('-id')

    def perform_create(self, serializer):
        serializer.save(content_type='banner')

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

# TemplateView-larni Swagger sxemasidan chiqarib tashlaymiz
@extend_schema(exclude=True)
class PublicHomeView(TemplateView):
    template_name = 'public/home.html'

@extend_schema(exclude=True)
class PublicMarketView(TemplateView):
    template_name = 'public/market.html'

@extend_schema(exclude=True)
class PublicRentView(TemplateView):
    template_name = 'public/rent.html'

@extend_schema(exclude=True)
class PublicAboutView(TemplateView):
    template_name = 'public/about.html'

@extend_schema(exclude=True)
class PublicProfileView(TemplateView):
    template_name = 'public/profile.html'

@extend_schema(exclude=True)
class PublicRentDetailView(TemplateView):
    template_name = 'public/rent_detail.html'

def handle_404(request, exception):
    from django.shortcuts import render
    return render(request, '404.html', status=404)

class TranslateView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=inline_serializer(
            name='TranslateRequest',
            fields={
                'texts': serializers.ListField(child=serializers.CharField(), help_text="Tarjima qilinishi kerak bo'lgan matnlar ro'yxati"),
                'lang': serializers.CharField(required=False, help_text="Maqsadli til kodi, masalan: 'ru', 'en'")
            }
        ),
        responses={
            200: inline_serializer(
                name='TranslateResponse',
                fields={
                    'original_text': serializers.CharField(help_text="Tarjima qilingan matn natijalari")
                }
            )
        },
        description="Matnlarni yuborilgan tilga guruh shaklida (batch) tarjima qilib beruvchi API"
    )
    def post(self, request):
        texts = request.data.get('texts', [])
        target_lang = request.data.get('lang') or request.headers.get('Accept-Language', 'uz').split(',')[0].strip().split('-')[0]

        lang_map = {
            'uz_cyrl': 'uz',
            'uz-cyrl': 'uz',
        }
        target_lang = lang_map.get(target_lang, target_lang)

        if not texts:
            return Response({})

        translations = translate_texts_batch(texts, target_lang)
        return Response(translations)
