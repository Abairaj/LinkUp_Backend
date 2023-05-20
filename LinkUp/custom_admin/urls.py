from django.urls import path
from . import views



urlpatterns = [

    path('',views.AdminLoginAPIView.as_view(), name='admin'),
    path('get_userlist/',views.AdminUsersAPIView.as_view(),name='user'),
    path('block_unblock_user/<int:user_id>',views.AdminUsersAPIView.as_view(),name='userban')


]