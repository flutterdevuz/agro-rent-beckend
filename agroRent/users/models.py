from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('Phone number is required'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    username = None
    phone_number = models.CharField(_('phone number'), max_length=15, unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
   
    country = models.CharField(_('country'), max_length=100, default="O'zbekiston")
    region = models.CharField(_('region'), max_length=50) 
    district = models.CharField(_('district'), max_length=100) # Tuman
    street = models.CharField(_('street'), max_length=150)       # Ko'cha
    house_number = models.CharField(_('house number'), max_length=50) # Uy raqami
    
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=2, default=0.0)
    is_renter = models.BooleanField(_('is renter'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

class ResetPasswordRequest(models.Model):
    phone_number = models.CharField(_('phone number'), max_length=15)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset request: {self.phone_number} at {self.created_at}"
