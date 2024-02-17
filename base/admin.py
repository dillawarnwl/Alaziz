from django.contrib import admin
from .models import DonorRegister, OrganizationRegister

# Register your models here.
admin.site.register(DonorRegister)
admin.site.register(OrganizationRegister)
