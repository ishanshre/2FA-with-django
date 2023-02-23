from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    otp_enabled = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    otp_base32 = models.CharField(max_length=255, null=True)
    otp_auth_url = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


