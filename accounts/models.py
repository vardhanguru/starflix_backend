from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    fname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.username