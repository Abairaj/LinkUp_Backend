from django.urls import path
from .import views


urlpatterns = [

    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('login/', views.UserLoginAPIView.as_view(), name='user_login'),
    path('user_profile/<int:pk>',views.UserProfileAPIView.as_view(), name='user_profile')






]
