from django.urls import path
from . import views

urlpatterns = [
    path('', views.product, name='index'),
    path('<slug:slug>/', views.detail, name='detail')
]