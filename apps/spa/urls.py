from django.urls import path
from . import views

urlpatterns = [
    path('', views.spa_index, name='spa'),
]
