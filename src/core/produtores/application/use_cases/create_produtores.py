from dataclasses import dataclass
from uuid import UUID
from src.core.produtores.application.exceptions import InvalidProdutoresData
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository
from src.core.produtores.domain.produtores import Produtores

@dataclass
class CreateProdutoresRequest:
    nomeProdutor: str
    registroIndividual: str
    status: bool = True

@dataclass
class CreateProdutoresResponse:
    idProdutor: UUID

class CreateProdutores:
    def __init__(self, repository: ProdutoresRepository):
        self.repository = repository
    
    def execute(self, request: CreateProdutoresRequest) -> CreateProdutoresResponse:
        try:
            produtor = Produtores(
                nomeProdutor= request.nomeProdutor,
                registroIndividual= request.registroIndividual,
                status= request.status,
            )
        except ValueError as err:
            raise InvalidProdutoresData(err)
        
        self.repository.save(produtor)
        return CreateProdutoresResponse(idProdutor= produtor.idProdutor)
    