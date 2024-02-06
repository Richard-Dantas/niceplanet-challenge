from dataclasses import dataclass
from uuid import UUID
from core.analiseHistorico.application.exceptions import InvalidAnaliseHistoricoData

from core.analiseHistorico.domain.IRepository.analiseHistoricoRepository import AnaliseHistoricoRepository
from core.analiseHistorico.domain.analiseHistorico import AnaliseHistorico


@dataclass
class CreateAnaliseHistoricoRequest:
    nomePropriedade: str
    numeroCar: str

@dataclass
class CreateAnaliseHistoricoResponse:
    idAnaliseHistorico: UUID

class CreateAnaliseHistorico:
    def __init__(self, repository: AnaliseHistoricoRepository):
        self.repository = repository
    
    def execute(self, request: CreateAnaliseHistoricoRequest) -> CreateAnaliseHistoricoResponse:
        try:
            analiseHistorico = AnaliseHistorico(
                nomePropriedade= request.nomePropriedade,
                numeroCar= request.numeroCar,
            )
        except ValueError as err:
            raise InvalidAnaliseHistoricoData(err)
        
        self.repository.save(analiseHistorico)
        return CreateAnaliseHistoricoResponse(idAnaliseHistorico= analiseHistorico.idAnaliseHistorico)