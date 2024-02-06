from src.core.produtores.application.use_cases.update_produtores import UpdateProdutores, UpdateProdutoresRequest
from src.core.produtores.domain.produtores import Produtores
from src.core.produtores.infra.in_memory_produtores_repository import InMemoryProdutoresRepository


class TestUpdateProdutores:
    def test_can_update_produtores_nomeProdutor(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        repository = InMemoryProdutoresRepository()
        repository.save(produtor)

        use_case = UpdateProdutores(repository=repository)
        request = UpdateProdutoresRequest(
            idProdutor= produtor.idProdutor,
            nomeProdutor="Testado",
            registroIndividual= "123.456.789-10",
        )

        use_case.execute(request)

        update_produtores = repository.get_by_id(produtor.idProdutor)
        assert update_produtores.nomeProdutor == produtor.nomeProdutor