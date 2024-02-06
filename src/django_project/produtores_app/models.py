from uuid import uuid4
from django.db import models

class Produtores(models.Model):
    idProdutor = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nomeProdutor = models.CharField(max_length=255)
    registroIndividual = models.CharField(max_length=14)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "Produtores"

    def __str__(self):
        return self.nomeProdutor
