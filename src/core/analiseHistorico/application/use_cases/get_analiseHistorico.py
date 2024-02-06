
from dataclasses import dataclass
import datetime
from uuid import UUID
from core.analiseHistorico.application.exceptions import AnaliseHistoricoNotFound

from core.analiseHistorico.domain.IRepository.analiseHistoricoRepository import AnaliseHistoricoRepository

@dataclass
class GetAnaliseHistoricoRequest:
    idAnaliseHistorico: UUID

@dataclass
class GetAnaliseHistoricoResponse:
    idAnaliseHistorico: UUID 
    nomePropriedade: str
    numeroCar: str
    dateAnalise: datetime

class GetAnaliseHistorico:
    def __init__(self, repository: AnaliseHistoricoRepository):
        self.repository = repository
    
    def execute(self, request: GetAnaliseHistoricoRequest) -> GetAnaliseHistoricoResponse:
        analiseHistorico = self.repository.get_by_id(id = request.idAnaliseHistorico)

        if analiseHistorico is None:
            raise AnaliseHistoricoNotFound(f"Histórico de Análise com {request.idAnaliseHistorico} não foi encontrado")

        return GetAnaliseHistoricoResponse(
            idAnaliseHistorico= analiseHistorico.idAnaliseHistorico,
            nomePropriedade= analiseHistorico.nomePropriedade,
            numeroCar= analiseHistorico.numeroCar,
            dateAnalise= analiseHistorico.dateAnalise,
        )