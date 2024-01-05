from django.urls import path
from .views import ExameList

urlpatterns = [
    path('',ExameList.as_view(),name='exame_list')
]