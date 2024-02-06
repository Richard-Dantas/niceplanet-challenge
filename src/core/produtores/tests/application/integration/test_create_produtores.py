from uuid import UUID
from src.core.produtores.application.use_cases.create_produtores import CreateProdutores, CreateProdutoresRequest
from src.core.produtores.infra.in_memory_produtores_repository import InMemoryProdutoresRepository


class TestCreateProdutores:
    def test_create_produtores_with_valid_data(self):
        repository = InMemoryProdutoresRepository()
        use_case = CreateProdutores(repository = repository)
        request = CreateProdutoresRequest(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )

        response = use_case.execute(request)
        
        assert response is not None
        assert isinstance(response.idProdutor, UUID)
        assert len(repository.produtores) == 1
        assert repository.produtores[0].idProdutor == response.idProdutor
