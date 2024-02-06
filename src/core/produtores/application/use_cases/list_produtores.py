from dataclasses import dataclass
from uuid import UUID
from src.core.produtores.application.exceptions import ProdutoresNotFound

from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository


@dataclass
class ListProdutoresRequest:
    pass

@dataclass
class ProdutoresOutput:
    idProdutor: UUID 
    nomeProdutor: str
    registroIndividual: str
    status: bool = True


@dataclass
class ListProdutoresResponse:
    data: list[ProdutoresOutput]
    

class ListProdutores:
    def __init__(self, repository: ProdutoresRepository):
        self.repository = repository
    
    def execute(self, request: ListProdutoresRequest) -> ListProdutoresResponse:
        produtores = self.repository.list()


        return ListProdutoresResponse(
            data=[
                ProdutoresOutput(
                    idProdutor= produtor.idProdutor,
                    nomeProdutor= produtor.nomeProdutor,
                    registroIndividual= produtor.registroIndividual,
                    status= produtor.status,
                ) 
                for produtor in produtores
            ]
        )