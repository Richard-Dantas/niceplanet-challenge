from dataclasses import dataclass
from uuid import UUID
from core.propriedades.application.exceptions import InvalidPropriedadesData
from core.propriedades.domain.IRepository.propriedades_repository import PropriedadesRepository
from core.propriedades.domain.propriedades import Propriedades


@dataclass
class CreatePropriedadesRequest:
    nomePropriedade: str
    numeroCar: str
    uf: str
    municipio: str
    pais: str
    liberado: int
    status: bool = True

@dataclass
class CreatePropriedadesResponse:
    idPropriedade: UUID

class CreatePropriedades:
    def __init__(self, repository: PropriedadesRepository):
        self.repository = repository
    
    def execute(self, request: CreatePropriedadesRequest) -> CreatePropriedadesResponse:
        try:
            propriedade = Propriedades(
                nomePropriedade= request.nomePropriedade,
                numeroCar= request.numeroCar,
                uf= request.uf,
                municipio= request.municipio,
                pais= request.pais,
                liberado= request.liberado,
                status= request.status
            )
        except ValueError as err:
            raise InvalidPropriedadesData(err)
        
        self.repository.save(propriedade)
        return CreatePropriedadesResponse(idPropriedade= propriedade.idPropriedade)