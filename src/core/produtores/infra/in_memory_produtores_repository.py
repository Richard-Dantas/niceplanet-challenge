from uuid import UUID
from src.core.produtores.domain.produtores import Produtores


class InMemoryProdutoresRepository:
    def __init__(self, produtores=None):
        self.produtores = produtores or []

    def save(self, produtor):
        self.produtores.append(produtor)

    def get_by_id(self, id: UUID) -> Produtores | None:
        return next(
            (produtores for produtores in self.produtores if produtores.idProdutor == id), None
        )
    
    def delete(self, id: UUID) -> None:
        produtor = self.get_by_id(id)
        self.produtores.remove(produtor)

    def update(self, produtor: Produtores) -> None:
        old_produtor = self.get_by_id(produtor.idProdutor)
        if old_produtor:
            self.produtores.remove(old_produtor)
            self.produtores.append(produtor)

    def list(self) -> list[Produtores]:
        return [produtores for produtores in self.produtores]