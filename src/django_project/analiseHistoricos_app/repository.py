from core.analiseHistorico.domain.IRepository.analiseHistoricoRepository import AnaliseHistoricoRepository
from uuid import UUID
from django_project.analiseHistoricos_app.models import AnaliseHistorico as AnaliseHistoricoModel
from core.analiseHistorico.domain.analiseHistorico import AnaliseHistorico


class DjangoORMAnaliseHistoricoRepository(AnaliseHistoricoRepository):
    def __init__(self, AnaliseHistorico_model: AnaliseHistoricoModel = AnaliseHistoricoModel) -> None:
        self.AnaliseHistorico_model = AnaliseHistorico_model

    def save(self, analiseHistorico: AnaliseHistorico) -> None:
        self.AnaliseHistorico_model.objects.create(
            idAnaliseHistorico = analiseHistorico.idAnaliseHistorico,
            nomePropriedade = analiseHistorico.nomePropriedade,
            numeroCar = analiseHistorico.numeroCar,
            dateAnalise = analiseHistorico.dateAnalise
        )

    def get_by_id(self, id: UUID) -> AnaliseHistorico | None:
        try:
            analiseHistorico = self.AnaliseHistorico_model.objects.get(idAnaliseHistorico = id)
            return AnaliseHistorico(
                idAnaliseHistorico = analiseHistorico.idAnaliseHistorico,
                nomePropriedade = analiseHistorico.nomePropriedade,
                numeroCar = analiseHistorico.numeroCar,
                dateAnalise = analiseHistorico.dateAnalise
            )
        except self.AnaliseHistorico_model.DoesNotExist:
            return None
        
    def delete(self, id: UUID) -> None:
        self.AnaliseHistorico_model.objects.filter(idAnaliseHistorico = id).delete()

    def list(self) -> list[AnaliseHistorico]:
        return [
            AnaliseHistorico(
                idAnaliseHistorico = analiseHistorico.idAnaliseHistorico,
                nomePropriedade = analiseHistorico.nomePropriedade,
                numeroCar = analiseHistorico.numeroCar,
                dateAnalise = analiseHistorico.dateAnalise
            )
            for analiseHistorico in self.AnaliseHistorico_model.objects.all()
        ]
