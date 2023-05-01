from django.urls import path
from . import views



urlpatterns = [
    path('dj-rest-auth/facebook/' ,views.FacebookLogin.as_view(),name='fb_login')

    
]