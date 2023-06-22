
from django.urls import path
from . import views


urlpatterns = [
    # user posts
    path('posts/<user_id>', views.PostAPIView.as_view(), name='post'),
    path('create_post/<int:user_id>',
         views.Create_Post_API_VIEW.as_view(), name='create_post'),

    path('getpost/<int:user_id>', views.PostByIdApiView.as_view(), name='post_by_id'),





    path('Post_like/<int:user_id>',
         views.Post_Like_Unlike_APIView.as_view(), name='Postlike'),
    path('add_comment/', views.Post_Comment.as_view(), name='Comment'),
    path('get_comment/<int:post_id>',
         views.Post_Comment.as_view(), name='Comment'),




]
