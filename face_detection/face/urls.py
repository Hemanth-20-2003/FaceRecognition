from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hm,name='home'),path('webcam',views.face,name='webcam'),path('cam',views.cam,name='cam'),path('add1',views.add1,name='add1'),path('add',views.add,name='add'),path('pic1',views.pic1,name='pic1'),path('pic3',views.pic3,name='pic3'),path('pic',views.pic,name='pic'),
]