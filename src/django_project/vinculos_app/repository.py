from uuid import UUID
from core.vinculos.domain.IRepository.vinculos_repository import VinculosRepository
from core.vinculos.domain.vinculos import Vinculos
from django_project.vinculos_app.models import Vinculos as VinculosModel


class DjangoORMVinculosRepository(VinculosRepository):
    def __init__(self, vinculos_model: VinculosModel = VinculosModel) -> None:
        self.vinculos_model = vinculos_model

    def save(self, vinculo: Vinculos) -> None:
        self.vinculos_model.objects.create(
            idVinculo = vinculo.idVinculo,
            idProdutor = vinculo.idProdutor,
            idPropriedade = vinculo.idPropriedade
        )

    def get_vinculos(self, id_propriedade: UUID) -> list[Vinculos] | None:
        try:
            vinculos = self.vinculos_model.objects.filter(idPropriedade = id_propriedade)
            return [
                Vinculos(
                    idVinculo=vinculo.idVinculo,
                    idPropriedade=vinculo.idPropriedade,
                    idProdutor=vinculo.idProdutor,
                )
            for vinculo in vinculos
        ]
        except self.vinculos_model.DoesNotExist:
            return []