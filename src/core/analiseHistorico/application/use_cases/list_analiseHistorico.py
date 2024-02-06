from dataclasses import dataclass
import datetime
from uuid import UUID

from core.analiseHistorico.domain.IRepository.analiseHistoricoRepository import AnaliseHistoricoRepository


@dataclass
class ListAnaliseHistoricoRequest:
    pass

@dataclass
class AnaliseHistoricoOutput:
    idAnaliseHistorico: UUID 
    nomePropriedade: str
    numeroCar: str
    dateAnalise: datetime

@dataclass
class ListAnaliseHistoricoResponse:
    data: list[AnaliseHistoricoOutput]

class ListAnaliseHistorico:
    def __init__(self, repository: AnaliseHistoricoRepository):
        self.repository = repository
    
    def execute(self, request: ListAnaliseHistoricoRequest) -> ListAnaliseHistoricoResponse:
        analiseHistoricos = self.repository.list()


        return ListAnaliseHistoricoResponse(
            data=[
                AnaliseHistoricoOutput(
                    idAnaliseHistorico= analiseHistorico.idAnaliseHistorico,
                    nomePropriedade= analiseHistorico.nomePropriedade,
                    numeroCar= analiseHistorico.numeroCar,
                    dateAnalise= analiseHistorico.dateAnalise,
                ) 
                for analiseHistorico in analiseHistoricos
            ]
        )