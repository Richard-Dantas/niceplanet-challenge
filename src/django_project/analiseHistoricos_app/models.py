from uuid import uuid4
from django.db import models

class AnaliseHistorico(models.Model):
    dateAnalise = models.DateField()
    idAnaliseHistorico = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nomePropriedade = models.CharField(max_length=255)
    numeroCar = models.CharField(max_length=14)

    class Meta:
        db_table = "AnaliseHistorico"

    def __str__(self):
        return self.numeroCar
