from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='customers/', null=True, blank=True, default='default.jpg')
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
