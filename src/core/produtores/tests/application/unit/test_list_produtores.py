from unittest.mock import create_autospec
from src.core.produtores.application.use_cases.list_produtores import ListProdutores, ListProdutoresRequest, ListProdutoresResponse, ProdutoresOutput
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository
from src.core.produtores.domain.produtores import Produtores


class TestListProdutores:
    def test_when_no_produtores_in_repository_then_return_empty_list(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.list.return_value = []

        use_case = ListProdutores(repository = mock_repository)
        request = ListProdutoresRequest(
        )

        response = use_case.execute(request)
        
        assert response == ListProdutoresResponse(
            data = []
        )

    def test_when_produtores_in_repository_then_return_list(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.list.return_value = [produtor]

        use_case = ListProdutores(repository = mock_repository)
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