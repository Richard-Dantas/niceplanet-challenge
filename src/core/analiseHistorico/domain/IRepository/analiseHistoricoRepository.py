from abc import ABC, abstractmethod
from uuid import UUID

from core.analiseHistorico.domain.analiseHistorico import AnaliseHistorico


class AnaliseHistoricoRepository(ABC):
    @abstractmethod
    def save(self, produtor):
        raise NotImplemented
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> AnaliseHistorico | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[AnaliseHistorico]:
        raise NotImplementedError