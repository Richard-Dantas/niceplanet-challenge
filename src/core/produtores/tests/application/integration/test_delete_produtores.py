from unittest.mock import create_autospec
from src.core.produtores.application.use_cases.delete_produtores import DeleteProdutores, DeleteProdutoresRequest
from src.core.produtores.domain.produtores import Produtores
from src.core.produtores.infra.in_memory_produtores_repository import InMemoryProdutoresRepository


class TestDeleteProdutores:
    def test_delete_produtores_from_repository(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        repository = InMemoryProdutoresRepository(produtores=[produtor])
        use_case = DeleteProdutores(repository = repository)
        request = DeleteProdutoresRequest(
            idProdutor = produtor.idProdutor,
        )

        response = use_case.execute(request)
        
        assert repository.get_by_id(produtor.idProdutor) is None
        assert response is None