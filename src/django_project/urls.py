"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter
from django_project.analiseHistoricos_app.views import AnaliseHistoricoViewSet

from django_project.produtores_app.views import ProdutoresViewSet
from django_project.propriedades_app.views import PropriedadesViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django_project.propriedades_app.views import PropriedadesViewSet

router = DefaultRouter()
router.register(r"api/produtores", ProdutoresViewSet, basename="produtores")
router.register(r"api/propriedades", PropriedadesViewSet, basename="propriedades")
router.register(r"api/vinculos", PropriedadesViewSet, basename="vinculos")
router.register(r"api/analiseHistoricos", AnaliseHistoricoViewSet, basename="analiseHistoricos")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
