
from django.urls import path
from . import views



urlpatterns = [

    path('posts/<int:user_id>',views.PostAPIView.as_view(),name='post'),
    path('Post_like/<int:user_id>',views.Post_Like_Unlike_APIView.as_view(),name='Postlike'),
    path('comment/',views.Post_Comment.as_view(),name='Comment')

    
 



] 
