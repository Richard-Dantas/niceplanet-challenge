from django.contrib import admin

from django.contrib import admin

from django_project.analiseHistoricos_app.models import AnaliseHistorico

class AnaliseHistoricoAdmin(admin.ModelAdmin):
    pass

admin.site.register(AnaliseHistorico, AnaliseHistoricoAdmin)
