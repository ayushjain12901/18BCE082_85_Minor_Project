from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('ag_data/', views.ag_data, name="ag_data"),
    path('analytics/', views.analytics, name="analytics"),
    path('stats/', views.stats, name="stats"),
    path('commodity_grade/',views.commodity_grade,name='commodity_grade'),
    path('commodity_variety/',views.commodity_variety,name='commodity_variety'),
    path('commodity_modal/',views.commodity_modal,name='commodity_modal'),
    path('commodity_modal1/',views.commodity_modal1,name='commodity_modal1')
]
