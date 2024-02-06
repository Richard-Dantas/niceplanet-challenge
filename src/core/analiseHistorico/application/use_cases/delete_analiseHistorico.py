
from dataclasses import dataclass
from uuid import UUID
from core.analiseHistorico.application.exceptions import AnaliseHistoricoNotFound

from core.analiseHistorico.domain.IRepository.analiseHistoricoRepository import AnaliseHistoricoRepository


@dataclass
class DeleteAnaliseHistoricoRequest:
    idAnaliseHistorico: UUID

class DeleteAnaliseHistorico:
    def __init__(self, repository: AnaliseHistoricoRepository):
        self.repository = repository
    
    def execute(self, request: DeleteAnaliseHistoricoRequest) -> None:
        analiseHistorico = self.repository.get_by_id(id = request.idAnaliseHistorico)

        if analiseHistorico is None:
            raise AnaliseHistoricoNotFound(f"Histórico de Análise com {request.idAnaliseHistorico} não foi encontrado")

        self.repository.delete(analiseHistorico.idAnaliseHistorico)