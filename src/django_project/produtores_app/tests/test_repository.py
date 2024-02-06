import pytest
from django_project.produtores_app.models import Produtores
from django_project.produtores_app.repository import DjangoORMProdutoresRepository
from django_project.produtores_app.models import Produtores as ProdutoresModel


@pytest.mark.django_db
class TestSave:
    def test_save_produtores_in_database(self):
        produtor = Produtores(
            nomeProdutor = "Teste Da Silva",
            registroIndividual = "123.456.789-10",
        )
        repository = DjangoORMProdutoresRepository()

        assert ProdutoresModel.objects.count() == 0
        repository.save(produtor)
        assert ProdutoresModel.objects.count() == 1