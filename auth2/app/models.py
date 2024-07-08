from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class customUser(AbstractUser):
    
    name = models.CharField(max_length=50,null=True)
    gender = models.CharField(max_length=50, null=True, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    dob = models.DateField(null=True)
    about = models.TextField(null=True)

    def __str__(self):
        return self.username