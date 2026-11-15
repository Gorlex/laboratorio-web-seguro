from django.urls import path
from . import views

app_name = "labs"

urlpatterns = [
    path(
        "<slug:lab_id>/iniciar/",
        views.iniciar_laboratorio_view,
        name="iniciar",
    ),
]