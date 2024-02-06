from uuid import UUID
from core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository
from core.produtores.domain.produtores import Produtores
from django_project.produtores_app.models import Produtores as ProdutoresModel


class DjangoORMProdutoresRepository(ProdutoresRepository):
    def __init__(self, produtores_model: ProdutoresModel = ProdutoresModel) -> None:
        self.produtores_model = produtores_model

    def save(self, produtor: Produtores) -> None:
        self.produtores_model.objects.create(
            idProdutor = produtor.idProdutor,
            nomeProdutor = produtor.nomeProdutor,
            registroIndividual = produtor.registroIndividual,
            status = produtor.status
        )

    def get_by_id(self, id: UUID) -> Produtores | None:
        try:
            produtor = self.produtores_model.objects.get(idProdutor = id)
            return Produtores(
                idProdutor = produtor.idProdutor,
                nomeProdutor = produtor.nomeProdutor,
                registroIndividual = produtor.registroIndividual,
                status = produtor.status
            )
        except self.produtores_model.DoesNotExist:
            return None
        
    def update(self, produtor: Produtores) -> None:
        self.produtores_model.objects.filter(pk = produtor.idProdutor).update(
            nomeProdutor= produtor.nomeProdutor,
            status = produtor.status,
        )
        
    def delete(self, id: UUID) -> None:
        self.produtores_model.objects.filter(idProdutor = id).delete()

    def list(self) -> list[Produtores]:
        return [
            Produtores(
                idProdutor = produtor.idProdutor,
                nomeProdutor = produtor.nomeProdutor,
                registroIndividual = produtor.registroIndividual,
                status = produtor.status
            )
            for produtor in self.produtores_model.objects.all()
        ]
