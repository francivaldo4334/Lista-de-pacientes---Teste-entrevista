"""
URL configuration for lista_pacientes project.

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
from django.urls import path, URLResolver, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_shemas_veiew

schema_view = swagger_get_shemas_veiew(
    openapi.Info(
        title='Consultas API',
        default_version='1.0.0',
        description='Gerencia lista de pacientes'
    ),
    public=True
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pacientes/', include('pacientes.urls')),
    path('agendamentos/', include('agendamento.urls')),
    path('exames/', include('exame.urls')),
    path('swagger_ui/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-shema')
]
