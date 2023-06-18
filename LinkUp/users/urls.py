from django.urls import path
from .import views


urlpatterns = [

    # user authentication
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('login/', views.UserLoginAPIView.as_view(), name='user_login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('auth/<int:id>/', views.AuthCheckAPIView.as_view(), name='auth'),

    # user profile
    path('user_profile/<int:pk>',
         views.UserProfileAPIView.as_view(), name='user_profile'),
    path('user_profile_update/<int:pk>',
         views.UserProfileAPIView.as_view(), name='user_profile'),

    # User suggestionlist
    path('user_suggestion/', views.UserSuggestionView.as_view(),
         name='user_suggestion'),

    # follow unfollow
    path('follow/<int:user_id>', views.UserFollowView.as_view(), name='follow'),


    # user search param
    path('user_search/', views.UserSearchView.as_view(), name='user_search')



]
