from django.db import models

class LaboratorioActivo(models.Model):
    """
    Modelo para registrar el estado y actividad de los laboratorios activos.
    """
    lab_id = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    ultima_actividad = models.DateTimeField(null=True, blank=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['activo', 'ultima_actividad']),
        ]
    
    def __str__(self):
        return self.lab_id