from django.db import models

class LaboratorioActivo(models.Model):
    """
    Modelo para registrar el estado y actividad de los laboratorios activos.
    """
    lab_id = models.CharField(max_length=100, unique=True)
    execution_id = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        unique=True
    )
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


class ResultadoReto(models.Model):
    semana = models.PositiveIntegerField()
    reto = models.PositiveIntegerField()
    lab_id = models.CharField(max_length=100)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(
        null=True,
        blank=True
    )
    metodo_validacion = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )
    execution_id = models.UUIDField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Resultado de reto"
        verbose_name_plural = "Resultados de retos"

        ordering = ["semana", "reto"]

        constraints = [
            models.UniqueConstraint(
                fields=["semana", "reto"],
                name="unique_resultado_semana_reto"
            )
        ]

    def __str__(self):
        return f"Semana {self.semana} - Reto {self.reto}"
