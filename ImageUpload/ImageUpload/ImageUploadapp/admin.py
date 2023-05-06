from django.contrib import admin

# Register your models here.

from .models import Image

class imageAdmin(admin.ModelAdmin):
    list_display = ["title", "image_file", "description"]

admin.site.register(Image, imageAdmin)