from django.urls import path

from .views import PacienteList

urlpatterns = [
    path('', PacienteList.as_view(), name='paciente-list')
]
