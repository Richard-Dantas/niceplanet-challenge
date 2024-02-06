from django.contrib import admin

from django_project.propriedades_app.models import Propriedades

class PropriedadesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Propriedades, PropriedadesAdmin)
