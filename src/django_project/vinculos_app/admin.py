from django.contrib import admin

from django_project.vinculos_app.models import Vinculos

class VinculosAdmin(admin.ModelAdmin):
    pass

admin.site.register(Vinculos, VinculosAdmin)
