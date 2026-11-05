from django.urls import path
from . import views

app_name = 'weeks'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:week_number>/', views.detail, name='detail'),
]