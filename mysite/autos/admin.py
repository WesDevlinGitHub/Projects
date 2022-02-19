from django.contrib import admin

# Register your models here.

from .models import Make
from .models import Auto

admin.site.register(Make)
admin.site.register(Auto)