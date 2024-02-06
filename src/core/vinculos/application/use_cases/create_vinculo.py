from dataclasses import dataclass
from uuid import UUID
from core.vinculos.application.exceptions import InvalidVinculosData

from core.vinculos.domain.IRepository.vinculos_repository import VinculosRepository
from core.vinculos.domain.vinculos import Vinculos


@dataclass
class CreateVinculosRequest:
    idPropriedade: UUID
    idProdutor: UUID

@dataclass
class CreateVinculosResponse:
    idvinculo: UUID


class CreateVinculos:
    def __init__(self, repository: VinculosRepository):
        self.repository = repository
    
    def execute(self, request: CreateVinculosRequest) -> CreateVinculosResponse:
        try:
            vinculo = Vinculos(
                idProdutor= request.idProdutor,
                idPropriedade= request.idPropriedade,
            )
        except ValueError as err:
            raise InvalidVinculosData(err)
        
        self.repository.save(vinculo)
        return CreateVinculosResponse(idVinculo= vinculo.idVinculo)