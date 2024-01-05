from django.urls import path
from .views import AgendamentoList

urlpatterns = [
    path('',AgendamentoList.as_view(),name = 'agendamento_list')
]