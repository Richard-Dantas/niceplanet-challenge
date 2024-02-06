from abc import ABC, abstractmethod
from uuid import UUID

from core.propriedades.domain.propriedades import Propriedades



class PropriedadesRepository(ABC):
    @abstractmethod
    def get_by_sicar(self, sicar: str) -> Propriedades | None:
        raise NotImplementedError
    @abstractmethod
    def save(self, propriedade):
        raise NotImplemented
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Propriedades | None:
        raise NotImplementedError

    # @abstractmethod
    # def delete(self, id: UUID) -> None:
    #     raise NotImplementedError
    
    @abstractmethod
    def update(self, produtor: Propriedades) -> None:
        raise NotImplementedError
    
    # @abstractmethod
    # def list(self) -> list[Propriedades]:
    #     raise NotImplementedError