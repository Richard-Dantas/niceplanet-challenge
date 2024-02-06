from uuid import uuid4
from django.db import models


class Vinculos(models.Model):
    idVinculo = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    idProdutor = models.UUIDField()
    idPropriedade = models.UUIDField()

    class Meta:
        db_table = "Vinculos"

    def __str__(self):
        return self.idVinculo