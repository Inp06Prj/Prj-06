from django.contrib import admin
from .models import UserProfile, Reserve

admin.site.register(UserProfile)

admin.site.register(Reserve)