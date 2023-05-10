
from django.urls import path
from . import views



urlpatterns = [

    path('create_post/<int:user_id>',views.PostAPIView.as_view(),name='post')

    
 



] 
