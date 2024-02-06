from django.contrib import admin

from django_project.produtores_app.models import Produtores

class ProdutoresAdmin(admin.ModelAdmin):
    pass

admin.site.register(Produtores, ProdutoresAdmin)
