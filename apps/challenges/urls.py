from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('<int:challenge_id>/', views.detail, name='detail'),
]