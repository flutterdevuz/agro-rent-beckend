import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class RentItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rent_items')
    name = models.CharField(_('name'), max_length=255)
    equipment_name = models.CharField(_('equipment name'), max_length=255)
    brand = models.CharField(_('brand'), max_length=255)
    hp = models.PositiveIntegerField(_('horse power'))
    condition = models.CharField(_('condition'), max_length=100)
    price = models.DecimalField(_('price'), max_digits=20, decimal_places=2)
    is_agreement = models.BooleanField(_('agreement'), default=False)
    region = models.CharField(_('region'), max_length=100)
    location_name = models.CharField(_('location name'), max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment_name} - {self.name}"

class RentImage(models.Model):
    rent_item = models.ForeignKey(RentItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rent_images/')

    def __str__(self):
        return f"Image for {self.rent_item.name}"

class RentOrder(models.Model):
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('delivered', _('Delivered')),
        ('canceled', _('Canceled')),
    ]
    rent_item = models.ForeignKey(RentItem, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rent_orders')
    location = models.CharField(_('location'), max_length=255)
    land_area = models.CharField(_('land area'), max_length=100)
    order_date = models.DateTimeField(_('order date'))
    comment = models.TextField(_('comment'), blank=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user} for {self.rent_item.name}"
