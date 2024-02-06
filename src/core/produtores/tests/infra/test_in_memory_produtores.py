from src.core.produtores.domain.produtores import Produtores
from src.core.produtores.infra.in_memory_produtores_repository import InMemoryProdutoresRepository


class TestInMemoryProdutoresRepository:
    def test_can_save_produtores(self):
        repository =  InMemoryProdutoresRepository()
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
        )

        repository.save(produtor)

        assert len(repository.produtores) == 1
        assert repository.produtores[0] == produtor