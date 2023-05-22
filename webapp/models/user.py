from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fcm_token = models.TextField()

    def __str__(self):
        return str(self.username)
