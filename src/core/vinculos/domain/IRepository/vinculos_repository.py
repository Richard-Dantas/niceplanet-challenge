from abc import ABC, abstractmethod
from uuid import UUID

from core.vinculos.domain.vinculos import Vinculos


class VinculosRepository(ABC):
    @abstractmethod
    def get_vinculos(self, id_propriedade: UUID) -> list[Vinculos]:
        raise NotImplementedError
    @abstractmethod
    def save(self, vinculo):
        raise NotImplemented