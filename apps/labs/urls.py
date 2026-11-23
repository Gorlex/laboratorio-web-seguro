from django.urls import path
from . import views

app_name = 'labs'

urlpatterns = [
    path('xss-stored/iniciar/', views.iniciar_laboratorio_view, {'lab_id': 'xss-stored'}, name='iniciar'),
    path('<slug:lab_id>/finalizar/', views.finalizar_laboratorio_view, name='finalizar'),
]