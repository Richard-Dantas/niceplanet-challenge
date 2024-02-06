from dataclasses import dataclass
from uuid import UUID
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository

@dataclass
class UpdateProdutoresRequest:
    idProdutor: UUID
    registroIndividual: str
    nomeProdutor: str | None = None
    status: bool | None = None


class UpdateProdutores:
    def __init__(self, repository: ProdutoresRepository):
        self.repository = repository

    def execute(self, request: UpdateProdutoresRequest) -> None:
        print("Request ID Produtor:", request.idProdutor)
        print("Request Nome Produtor:", request.nomeProdutor)
        print("Request Registro Individual:", request.registroIndividual)
        print("Request Status:", request.status)
        produtor =  self.repository.get_by_id(request.idProdutor)

        if request.status is True:
                produtor.activate()

        if request.status is False:
            produtor.deactivate()
            
        if request.nomeProdutor is not None:
                produtor.nomeProdutor = request.nomeProdutor
        
        produtor.update_produtores(nomeProdutor= produtor.nomeProdutor)

        
        self.repository.update(produtor)
