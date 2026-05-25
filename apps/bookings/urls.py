from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_page, name='booking'),
    path('modal/', views.booking_modal, name='booking_modal'),
    path('submit/', views.booking_submit, name='booking_submit'),
]
