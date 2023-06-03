from django.urls import path
from . import views



urlpatterns = [

path('',views.ReportAPIVIEW.as_view(),name="report")



]
