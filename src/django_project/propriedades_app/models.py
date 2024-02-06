from django.db import models
from uuid import uuid4

class Propriedades(models.Model):
    class StatusLiberado(models.IntegerChoices):
        BLOQUEADO = 0, 'Bloqueado'
        LIBERADO = 1, 'Liberado'
        ALERTA = 2, 'Alerta'
    idPropriedade= models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nomePropriedade= models.CharField(max_length=255)
    numeroCar= models.CharField(max_length=255)
    uf= models.CharField(max_length=255)
    municipio= models.CharField(max_length=255)
    pais= models.CharField(max_length=255)
    status= models.BooleanField(default=True)
    liberado= models.IntegerField(choices = StatusLiberado.choices, default = StatusLiberado.BLOQUEADO, verbose_name = "liberado")
    

    class Meta:
        db_table = "Propriedades"

    def __str__(self):
        return f"{self.get_status_display()} - {self.nomePropriedade} ({self.uf}, {self.municipio}, {self.pais})"
