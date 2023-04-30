from django.urls import path
from . import views



urlpatterns = [

    path('',views.AdminLoginAPIView.as_view(), name='admin'),


]