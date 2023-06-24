from django.urls import path
from . import views


urlpatterns = [

    path('', views.ReportAPIVIEW.as_view(), name="report"),
    path('delete_post/<int:post_id>',
         views.DeletePost_Action.as_view(), name='delete_post'),
    path('search_report/',
         views.SearchReportApiView.as_view(), name='searchreport'),



]
