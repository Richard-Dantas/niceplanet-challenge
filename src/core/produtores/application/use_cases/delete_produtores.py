from dataclasses import dataclass
from uuid import UUID
from src.core.produtores.application.exceptions import ProdutoresNotFound
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository

@dataclass
class DeleteProdutoresRequest:
    idProdutor: UUID


class DeleteProdutores:
    def __init__(self, repository: ProdutoresRepository):
        self.repository = repository
    
    def execute(self, request: DeleteProdutoresRequest) -> None:
        produtor = self.repository.get_by_id(id = request.idProdutor)

        if produtor is None:
            raise ProdutoresNotFound(f"Produtor com {request.idProdutor} não foi encontrado")

        self.repository.delete(produtor.idProdutor)
    