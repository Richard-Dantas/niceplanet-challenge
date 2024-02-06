from dataclasses import dataclass
from uuid import UUID
from src.core.produtores.application.exceptions import ProdutoresNotFound
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository
from src.core.produtores.domain.produtores import Produtores

@dataclass
class GetProdutoresRequest:
    idProdutor: UUID

@dataclass
class GetProdutoresResponse:
    idProdutor: UUID 
    nomeProdutor: str
    registroIndividual: str
    status: bool = True

class GetProdutores:
    def __init__(self, repository: ProdutoresRepository):
        self.repository = repository
    
    def execute(self, request: GetProdutoresRequest) -> GetProdutoresResponse:
        produtor = self.repository.get_by_id(id = request.idProdutor)

        if produtor is None:
            raise ProdutoresNotFound(f"Produtor com {request.idProdutor} não foi encontrado")

        return GetProdutoresResponse(
            idProdutor= produtor.idProdutor,
            nomeProdutor= produtor.nomeProdutor,
            registroIndividual= produtor.registroIndividual,
            status= produtor.status,
        )
    

    