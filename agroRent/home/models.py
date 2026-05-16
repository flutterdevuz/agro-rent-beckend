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
