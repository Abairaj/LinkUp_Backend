from django.urls import path
from . import views



urlpatterns = [

    path('message/<rec_id>/<sen_id>',views.MessageAccessView.as_view(), name='message'),

]