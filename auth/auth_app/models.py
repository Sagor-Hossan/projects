from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class customUser(AbstractUser):
    def __str__(self) -> str:
        return self.username