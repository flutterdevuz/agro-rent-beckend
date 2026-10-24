from django.conf import settings
from django.db.models import Count, Q
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from home.models import (
    HomeContent, SiteText, WebsiteSettings, WebsiteService,
    WebsitePartner, WebsiteStep, WebsiteBenefit, WebsiteOrder
)
from home.seed_website import seed_website_data
from home.serializers import (
    HomeContentSerializer, SiteTextSerializer,
    WebsiteSettingsSerializer, WebsiteServiceSerializer,
    WebsitePartnerSerializer, WebsiteStepSerializer,
    WebsiteBenefitSerializer, WebsiteOrderSerializer
)

from users.permissions import IsStaffOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from agroRent.utils.translator import translate_text, translate_texts_batch

from market.models import MarketItem
from market.serializers import MarketItemSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers

class BannerListView(generics.ListCreateAPIView):
    serializer_class = HomeContentSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def get_queryset(self):
        return HomeContent.objects.filter(content_type='banner').order_by('-id')

    def perform_create(self, serializer):
        serializer.save(content_type='banner')

class PopularEquipmentListView(generics.ListAPIView):
    serializer_class = MarketItemSerializer
    # Ochiq bosh sahifada ko'rsatiladi
    permission_classes = [AllowAny]

    def get_queryset(self):
        return MarketItem.objects.annotate(
            order_count=Count('orders')
        ).order_by('-order_count', '-created_at')[:10]

class HomeContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeContent.objects.all()
    serializer_class = HomeContentSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

# TemplateView-larni Swagger sxemasidan chiqarib tashlaymiz
@extend_schema(exclude=True)
class PublicHomeView(TemplateView):
    template_name = 'public/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            seed_website_data()
            context['site_settings'] = WebsiteSettings.get_settings()
            context['services'] = WebsiteService.objects.filter(is_active=True)
            context['partners'] = WebsitePartner.objects.filter(is_active=True)
            context['steps'] = WebsiteStep.objects.all()
            context['benefits'] = WebsiteBenefit.objects.all()
        except Exception as e:
            context['site_settings'] = None
        return context

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

class SiteTextListView(generics.ListCreateAPIView):
    queryset = SiteText.objects.all().order_by('-id')
    serializer_class = SiteTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return SiteText.objects.none()
        queryset = SiteText.objects.all().order_by('-id')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(key__icontains=search) |
                Q(uz__icontains=search) |
                Q(uz_cyrl__icontains=search) |
                Q(ru__icontains=search) |
                Q(en__icontains=search) |
                Q(tr__icontains=search)
            )
        return queryset

class SiteTextDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SiteText.objects.all()
    serializer_class = SiteTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return SiteText.objects.none()
        return super().get_queryset()

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
        description="Matnlarni yuborilgan tilga guruh shaklida (batch) tarjima qilib beruvchi API (Baza orqali)"
    )
    def post(self, request):
        texts = request.data.get('texts', [])
        if not isinstance(texts, list):
            return Response({})
        # Ochiq endpoint: hajmni cheklaymiz
        texts = [t for t in texts if isinstance(t, str) and 0 < len(t) <= 1000][:300]
        target_lang = request.data.get('lang') or request.headers.get('Accept-Language', 'uz').split(',')[0].strip().split('-')[0]

        if not texts:
            return Response({})

        lang_field_map = {
            'uz': 'uz',
            'uz_cyrl': 'uz_cyrl',
            'uz-cyrl': 'uz_cyrl',
            'ru': 'ru',
            'en': 'en',
            'tr': 'tr'
        }
        db_field = lang_field_map.get(target_lang, 'uz')

        existing_texts = {st.key: st for st in SiteText.objects.filter(key__in=texts)}

        texts_to_translate = []
        for text in texts:
            st = existing_texts.get(text)
            if not st:
                texts_to_translate.append(text)
            else:
                val = getattr(st, db_field, None)
                if not val:
                    texts_to_translate.append(text)

        if not settings.AUTO_TRANSLATE:
            # Avtomatik tarjima o'chiq: yangi matnlar admin "Site Texts" bo'limida
            # to'ldirishi uchun bazaga qo'shiladi, javobda esa asl matn qaytadi
            for text in texts_to_translate:
                if text not in existing_texts:
                    SiteText.objects.get_or_create(key=text, defaults={'uz': text} if db_field != 'uz' else {})
            texts_to_translate = []

        translations = {}
        if texts_to_translate:
            translations = translate_texts_batch(texts_to_translate, target_lang)

        for text in texts_to_translate:
            translated_val = translations.get(text, text)
            st = existing_texts.get(text)
            if not st:
                create_data = {
                    'key': text,
                    db_field: translated_val
                }
                if db_field != 'uz':
                    create_data['uz'] = text
                try:
                    st = SiteText.objects.create(**create_data)
                    existing_texts[text] = st
                except Exception as e:
                    # Raund-trip handling if key was created concurrently
                    try:
                        st = SiteText.objects.get(key=text)
                        setattr(st, db_field, translated_val)
                        st.save(update_fields=[db_field])
                        existing_texts[text] = st
                    except:
                        pass
            else:
                setattr(st, db_field, translated_val)
                st.save(update_fields=[db_field])

        response_data = {}
        for text in texts:
            st = existing_texts.get(text)
            val = getattr(st, db_field, None) if st else text
            response_data[text] = val or text

        return Response(response_data)



# =========================================================================
# WEBSITE & LANDING PAGE APIS
# =========================================================================

class WebsiteContentAPIView(APIView):
    """
    Landing page uchun barcha ma'lumotlarni qaytaruvchi ochiq API
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            seed_website_data()
            settings_obj = WebsiteSettings.get_settings()
            services = WebsiteService.objects.filter(is_active=True)
            partners = WebsitePartner.objects.filter(is_active=True)
            steps = WebsiteStep.objects.all()
            benefits = WebsiteBenefit.objects.all()

            return Response({
                'settings': WebsiteSettingsSerializer(settings_obj).data,
                'services': WebsiteServiceSerializer(services, many=True).data,
                'partners': WebsitePartnerSerializer(partners, many=True).data,
                'steps': WebsiteStepSerializer(steps, many=True).data,
                'benefits': WebsiteBenefitSerializer(benefits, many=True).data,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WebsiteOrderCreateView(generics.CreateAPIView):
    """
    Landing page orqali ariza va buyurtmalarni qabul qilish API
    """
    serializer_class = WebsiteOrderSerializer
    permission_classes = [AllowAny]


# Admin Website Management APIs
class AdminWebsiteSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = WebsiteSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        seed_website_data()
        return WebsiteSettings.get_settings()


class AdminWebsiteServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = WebsiteServiceSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsiteService.objects.all().order_by('order', 'id')


class AdminWebsiteServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WebsiteServiceSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsiteService.objects.all()


class AdminWebsitePartnerListCreateView(generics.ListCreateAPIView):
    serializer_class = WebsitePartnerSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsitePartner.objects.all().order_by('order', 'id')


class AdminWebsitePartnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WebsitePartnerSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsitePartner.objects.all()


class AdminWebsiteOrderListView(generics.ListAPIView):
    serializer_class = WebsiteOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsiteOrder.objects.all().order_by('-created_at')


class AdminWebsiteOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WebsiteOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsiteOrder.objects.all()


class AdminWebsiteStepListCreateView(generics.ListCreateAPIView):
    serializer_class = WebsiteStepSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsiteStep.objects.all().order_by('order', 'id')


class AdminWebsiteStepDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WebsiteStepSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsiteStep.objects.all()


class AdminWebsiteBenefitListCreateView(generics.ListCreateAPIView):
    serializer_class = WebsiteBenefitSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsiteBenefit.objects.all().order_by('order', 'id')


class AdminWebsiteBenefitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WebsiteBenefitSerializer
    permission_classes = [IsAuthenticated]
    queryset = WebsiteBenefit.objects.all()
