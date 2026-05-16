import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django.utils import timezone

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

class MarketItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='market_items')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(_('name'), max_length=255)
    image = models.ImageField(_('image'), upload_to='market_items/', null=True, blank=True)
    price = models.DecimalField(_('price'), max_digits=20, decimal_places=2)
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=2, default=0.0)
    likes_count = models.PositiveIntegerField(_('likes'), default=0)
    location = models.CharField(_('location'), max_length=255)
    condition = models.CharField(_('condition'), max_length=100)
    brand = models.CharField(_('brand'), max_length=100)
    model = models.CharField(_('model'), max_length=100)
    has_delivery = models.BooleanField(_('has delivery'), default=False)
    warranty = models.CharField(_('warranty'), max_length=100, blank=True)
    description = models.TextField(_('description'))
    phone_number = models.CharField(_('contact phone'), max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MarketOrder(models.Model):
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('delivered', _('Delivered')),
        ('canceled', _('Canceled')),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(MarketItem, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='market_orders')
    delivery_location = models.CharField(_('delivery location'), max_length=255)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    delivery_date = models.DateField(_('delivery date'))
    comment = models.TextField(_('comment'), blank=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user} for {self.item.name}"
