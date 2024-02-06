from uuid import UUID
from core.propriedades.domain.IRepository.propriedades_repository import PropriedadesRepository
from core.propriedades.domain.propriedades import Propriedades
from django_project.propriedades_app.models import Propriedades as PropriedadesModel

class DjangoORMPropriedadesRepository(PropriedadesRepository):
    def __init__(self, propriedades_model: PropriedadesModel = PropriedadesModel) -> None:
        self.propriedades_model = propriedades_model

    def save(self, propriedade: Propriedades) -> None:
        self.propriedades_model.objects.create(
            idPropriedade= propriedade.idPropriedade,
            nomePropriedade= propriedade.nomePropriedade,
            numeroCar= propriedade.numeroCar,
            uf= propriedade.uf,
            municipio= propriedade.municipio,
            pais= propriedade.pais,
            liberado= propriedade.liberado,
            status= propriedade.status
        )

    def get_by_sicar(self, sicar: str) -> Propriedades | None:
        try:
            propriedade = self.propriedades_model.objects.get(numeroCar = sicar)
            return Propriedades(
                idPropriedade= propriedade.idPropriedade,
                nomePropriedade= propriedade.nomePropriedade,
                numeroCar= propriedade.numeroCar,
                uf= propriedade.uf,
                municipio= propriedade.municipio,
                pais= propriedade.pais,
                liberado= propriedade.liberado,
                status= propriedade.status
            )
        except self.propriedades_model.DoesNotExist:
            return None
        
    def get_by_id(self, id: UUID) -> Propriedades | None:
        try:
            propriedade = self.propriedades_model.objects.get(idPropriedade = id)
            return Propriedades(
                idPropriedade= propriedade.idPropriedade,
                nomePropriedade= propriedade.nomePropriedade,
                numeroCar= propriedade.numeroCar,
                uf= propriedade.uf,
                municipio= propriedade.municipio,
                pais= propriedade.pais,
                liberado= propriedade.liberado,
                status= propriedade.status
            )
        except self.propriedades_model.DoesNotExist:
            return None
        
    def update(self, propriedade: Propriedades) -> None:
        self.propriedades_model.objects.filter(pk = propriedade.idPropriedade).update(
            liberado = propriedade.liberado
        )