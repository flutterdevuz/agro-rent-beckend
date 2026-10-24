import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from market.models import MarketItem

class HomeContent(models.Model):
    TYPE_CHOICES = [
        ('banner', 'Banner'),
        ('popular_equipment', 'Ommabop texnika'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'))
    image = models.ImageField(_('image'), upload_to='home_content/')
    price = models.DecimalField(_('price'), max_digits=20, decimal_places=2, null=True, blank=True)
    market_item = models.ForeignKey(MarketItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='featured_at_home')

    class Meta:
        verbose_name = _('Home Content')
        verbose_name_plural = _('Home Contents')

    def __str__(self):
        return f"{self.get_content_type_display()}: {self.name}"

class SiteText(models.Model):
    key = models.TextField(unique=True, verbose_name=_("Key/Original Text"))
    uz = models.TextField(blank=True, null=True, verbose_name=_("Uzbek (Latin)"))
    uz_cyrl = models.TextField(blank=True, null=True, verbose_name=_("Uzbek (Cyrillic)"))
    ru = models.TextField(blank=True, null=True, verbose_name=_("Russian"))
    en = models.TextField(blank=True, null=True, verbose_name=_("English"))
    tr = models.TextField(blank=True, null=True, verbose_name=_("Turkish"))

    class Meta:
        verbose_name = _("Site Text")
        verbose_name_plural = _("Site Texts")

    def __str__(self):
        return self.key[:50]


# =========================================================================
# WEBSITE / LANDING PAGE MODELLARI (Admin paneldan to'liq boshqariladigan)
# =========================================================================

class WebsiteSettings(models.Model):
    """
    Landing page boshqaruv sozlamalari, havolalari, statistikasi va kontaktlari.
    """
    # Hero Bo'limi
    hero_badge = models.CharField(max_length=255, default="QIShLOQ XO'JALIGI UChUN ZAMONAVIY YECHIM")
    hero_title = models.CharField(max_length=500, default="Qishloq xo'jaligi texnikalari va agroxizmatlarni bir platformada toping.")
    hero_description = models.TextField(default="Traktor, kombayn, seyalka, purkagich, suv nasoslari va boshqa texnikalarni ijaraga oling, shuningdek agroxizmatlarga buyurtma bering. Dehqonlar uchun tez, qulay va ishonchli platforma.")
    hero_primary_cta_text = models.CharField(max_length=100, default="Xizmatni boshlash")
    hero_primary_cta_link = models.CharField(max_length=255, default="#boglanish")
    hero_secondary_cta_text = models.CharField(max_length=100, default="Qanday ishlaydi?")
    hero_secondary_cta_link = models.CharField(max_length=255, default="#qanday-ishlaydi")

    # Mobil Ilova Havolalari (Google Play & App Store)
    google_play_url = models.CharField(max_length=500, blank=True, default="https://play.google.com/store/apps/details?id=uz.agrorent")
    app_store_url = models.CharField(max_length=500, blank=True, default="https://apps.apple.com/app/agrorent/id123456789")

    # Aloqa va Ijtimoiy Tarmoqlar
    phone_number = models.CharField(max_length=50, default="+998 90 123 45 67")
    email = models.CharField(max_length=100, default="info@agrorent.uz")
    address = models.CharField(max_length=255, default="Andijon viloyati, Andijon shahri")
    telegram_url = models.CharField(max_length=500, blank=True, default="https://t.me/agrorent_uz")
    instagram_url = models.CharField(max_length=500, blank=True, default="https://instagram.com/agrorent_uz")
    facebook_url = models.CharField(max_length=500, blank=True, default="https://facebook.com/agrorent.uz")
    youtube_url = models.CharField(max_length=500, blank=True, default="https://youtube.com/@agrorent")

    # Tezkor Statistika (Floating Banner)
    stats_users = models.CharField(max_length=50, default="600+")
    stats_services = models.CharField(max_length=50, default="8 ta")
    stats_region = models.CharField(max_length=100, default="Andijon")
    stats_orders_support = models.CharField(max_length=50, default="24/7")

    # Katta Natijalar (Big Stats)
    stat_total_orders = models.CharField(max_length=50, default="10 000+")
    stat_total_farmers = models.CharField(max_length=50, default="1 200+")
    stat_total_companies = models.CharField(max_length=50, default="150+")
    stat_rating = models.CharField(max_length=50, default="4.9")

    # Pastki Banner (CTA)
    cta_title = models.CharField(max_length=500, default="Bugun AgroRent bilan yangi imkoniyatlarga qadam qo'ying!")
    cta_subtitle = models.TextField(default="Zamonaviy qishloq xo'jaligi uchun ishonchli raqamli hamkor.")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Website Sozlamasi')
        verbose_name_plural = _('Website Sozlamalari')

    def __str__(self):
        return "AgroRent Website Sozlamalari"

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class WebsiteService(models.Model):
    """
    Landing page 'Bizning xizmatlar' bo'limi (8 ta asosiy xizmat va qo'shimcha xizmatlar)
    """
    slug = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_estimate = models.CharField(max_length=255, default="", blank=True)
    features = models.TextField(blank=True, default="", help_text="Har bir qatorda bitta afzallik")
    image = models.ImageField(upload_to='website/services/', blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, default="")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Website Xizmati')
        verbose_name_plural = _('Website Xizmatlari')
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return f"/api/static/images/service-{self.slug}-hd.png"


class WebsitePartner(models.Model):
    """
    Landing page 'Bizning hamkorlar' va 'Jamoa' bo'limi
    """
    TYPE_CHOICES = [
        ('partner', 'Hamkor kompaniya / fermer'),
        ('team', 'Jamoa a\'zosi / mutaxassis'),
    ]
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='website/partners/', blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, default="")
    member_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='partner')
    contact_or_link = models.CharField(max_length=255, blank=True, default="")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Website Hamkor / Jamoa')
        verbose_name_plural = _('Website Hamkorlar va Jamoa')
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.get_member_type_display()})"

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        if self.photo_url:
            return self.photo_url
        return f"/api/static/images/partner-{self.id or 1}-hd.png"


class WebsiteStep(models.Model):
    """
    Qanday ishlaydi - 4 qadam
    """
    step_number = models.CharField(max_length=10) # 01, 02, 03, 04
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Website Qadami')
        verbose_name_plural = _('Website Qadamlari (Qanday ishlaydi)')
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.step_number} - {self.title}"


class WebsiteBenefit(models.Model):
    """
    Nima uchun AgroRent - 4 afzallik
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="zap") # zap, shield-check, receipt, sprout
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Website Afzalligi')
        verbose_name_plural = _('Website Afzalliklari')
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class WebsiteOrder(models.Model):
    """
    Landing page orqali qoldirilgan buyurtma arizalari (Leadlar)
    """
    name = models.CharField(max_length=255, verbose_name="Foydalanuvchi ismi")
    phone = models.CharField(max_length=50, verbose_name="Telefon raqami")
    service = models.CharField(max_length=255, verbose_name="Xizmat turi")
    message = models.TextField(blank=True, default="", verbose_name="Xabar yoki izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    is_contacted = models.BooleanField(default=False, verbose_name="Bog'lanildi")
    admin_notes = models.TextField(blank=True, default="", verbose_name="Admin qaydlari")

    class Meta:
        verbose_name = _('Sayt Arizasi (Lead)')
        verbose_name_plural = _('Sayt Arizalari (Leadlar)')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.service} ({self.phone})"
