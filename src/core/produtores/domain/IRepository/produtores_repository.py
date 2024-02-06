from abc import ABC, abstractmethod
from uuid import UUID

from src.core.produtores.domain.produtores import Produtores


class ProdutoresRepository(ABC):
    @abstractmethod
    def save(self, produtor):
        raise NotImplemented
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Produtores | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, produtor: Produtores) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[Produtores]:
        raise NotImplementedError