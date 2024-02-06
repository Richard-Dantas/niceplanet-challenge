from unittest.mock import create_autospec
from src.core.produtores.application.use_cases.list_produtores import ListProdutores, ListProdutoresRequest, ListProdutoresResponse, ProdutoresOutput
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository
from src.core.produtores.domain.produtores import Produtores
from src.core.produtores.infra.in_memory_produtores_repository import InMemoryProdutoresRepository


class TestListProdutores:
    def test_return_empty_list(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        repository = InMemoryProdutoresRepository(produtores=[])

        use_case = ListProdutores(repository = repository)
        request = ListProdutoresRequest(
        )

        response = use_case.execute(request)
        
        assert response == ListProdutoresResponse(
            data = []
        )

    def test_return_existing_produtores(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        repository = InMemoryProdutoresRepository()
        repository.save(produtor)

        use_case = ListProdutores(repository = repository)
        request = ListProdutoresRequest(
        )

        response = use_case.execute(request)
        
        assert response == ListProdutoresResponse(
            data = [
                ProdutoresOutput(
                    idProdutor = produtor.idProdutor,
                    nomeProdutor = produtor.nomeProdutor,
                    registroIndividual = produtor.registroIndividual,
                    status = produtor.status,
                ),
            ]
        )