from dataclasses import dataclass
from uuid import UUID
from core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository
from core.propriedades.application.exceptions import PropriedadesNotFound
from typing import List

from core.propriedades.domain.IRepository.propriedades_repository import PropriedadesRepository
from core.vinculos.domain.IRepository.vinculos_repository import VinculosRepository


@dataclass
class GetPropriedadesRequest:
    numeroCar: str

@dataclass
class ProdutorVinculado:
    idProdutor: UUID
    nomeProdutor: str
    registroIndividual: str
    status: bool

@dataclass
class GetPropriedadesResponse:
    idPropriedade: UUID
    nomePropriedade: str
    numeroCar: str
    uf: str
    municipio: str
    pais: str
    liberado: int
    status: bool = True
    produtores_vinculados: List[ProdutorVinculado] = None

class GetPropriedades:
    def __init__(
            self, 
            propriedade_repository: PropriedadesRepository, 
            vinculo_repository: VinculosRepository,
            produtor_repository: ProdutoresRepository
        ):
        self.propriedade_repository = propriedade_repository
        self.vinculo_repository = vinculo_repository
        self.produtor_repository = produtor_repository
    
    def execute(self, request: GetPropriedadesRequest) -> GetPropriedadesResponse:
        propriedade = self.propriedade_repository.get_by_sicar(sicar= request.numeroCar)

        if propriedade is None:
            raise PropriedadesNotFound(f"Propriedade com {request.numeroCar} não foi encontrada")
        
        vinculos = self.vinculo_repository.get_vinculos(id_propriedade=propriedade.idPropriedade)

        produtores_vinculados = []
        for vinculo in vinculos:
            produtor = self.produtor_repository.get_by_id(vinculo.idProdutor)
            if produtor:
                produtores_vinculados.append(ProdutorVinculado(
                    idProdutor=produtor.idProdutor,
                    nomeProdutor=produtor.nomeProdutor,
                    registroIndividual=produtor.registroIndividual,
                    status=produtor.status
                ))

        return GetPropriedadesResponse(
            idPropriedade= propriedade.idPropriedade,
            nomePropriedade= propriedade.nomePropriedade,
            numeroCar= propriedade.numeroCar,
            produtores_vinculados=produtores_vinculados,
            uf=propriedade.uf,
            municipio=propriedade.municipio,
            pais= propriedade.pais,
            liberado=propriedade.liberado,
            status= propriedade.status,
        )
    

    