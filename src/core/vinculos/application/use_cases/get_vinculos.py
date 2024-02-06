from dataclasses import dataclass
from uuid import UUID
from core.vinculos.application.exceptions import VinculosNotFound

from core.vinculos.domain.IRepository.vinculos_repository import VinculosRepository


@dataclass
class GetVinculoByPropriedadeRequest:
    idPropriedade: UUID

@dataclass
class GetVinculoByPropriedadeResponse:
    idVinculo: UUID
    nomeProdutor: UUID
    registroGeral: UUID

class GetVinculos:
    def __init__(self, repository: VinculosRepository):
        self.repository = repository

    def execute(self, request: GetVinculoByPropriedadeRequest) -> GetVinculoByPropriedadeResponse:
        vinculos_data = self.repository.get_vinculos(id_propriedade= request.idPropriedade)

        if vinculos_data is None:
            raise VinculosNotFound(f"Vinculo com propriedade {request.idPropriedade} não foi encontrado")
        
        vinculos = [GetVinculoByPropriedadeResponse(
            idVinculo=vinculo_data['idVinculo'],
            idPropriedade=vinculo_data['idPropriedade'],
            idProdutor=vinculo_data['idProdutor']
        ) for vinculo_data in vinculos_data]

        return vinculos