from django.db import models
from django.contrib.auth.models import User

class DonorRegister(models.Model):
    fname = models.CharField(max_length=50, blank=False, null=False)
    lname = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=11, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    bgroup = models.CharField(max_length=3, blank=False, null=False)
    donorid = models.CharField(max_length=15, unique=True)    
    more = models.TextField(null=True, blank=True)
    dob = models.DateField(null=False, blank=False)
    ldonation = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, blank=True)

    def __str__(self):
        return self.donorid  # Returning a relevant field for the object representation
