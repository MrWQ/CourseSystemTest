# -*- coding: utf-8 -*-  
# from django.contrib import admin
from django.conf.urls import handler404
from django.urls import path

from course import views

urlpatterns = [

    path('json/',views.testjson),

    path('',views.index),
    path('base/',views.base),
    path('index/', views.index),
    path('upload/', views.upload2),
    path('files/', views.uploadfiles),
    path('data/', views.data),
    path('data2/', views.data2),
    path('data3/',views.data3),

    # path('tip/',views.tip),
]

handler404 = 'views.index'