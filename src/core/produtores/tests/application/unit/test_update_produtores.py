from unittest.mock import create_autospec
from src.core.produtores.application.use_cases.update_produtores import UpdateProdutores, UpdateProdutoresRequest
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository
from src.core.produtores.domain.produtores import Produtores


class TestUpdateProdutores:
    def test_update_produtores_nomeProdutor(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.get_by_id.return_value = produtor
        use_case = UpdateProdutores(repository = mock_repository)
        request = UpdateProdutoresRequest(
            idProdutor = produtor.idProdutor,
            nomeProdutor = "Testado",
            registroIndividual= "123.456.789-10",
            )
        
        use_case.execute(request)

        assert produtor.nomeProdutor == "Testado"
        mock_repository.update.assert_called_once_with(produtor)

    def test_can_deactivate_produtores(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.get_by_id.return_value = produtor
        use_case = UpdateProdutores(repository = mock_repository)
        request = UpdateProdutoresRequest(
            idProdutor = produtor.idProdutor,
            registroIndividual= "123.456.789-10",
            status = False,
            )
        
        use_case.execute(request)

        assert produtor.status is False
        mock_repository.update.assert_called_once_with(produtor)

    def test_can_activate_produtores(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= False,
        )
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.get_by_id.return_value = produtor
        use_case = UpdateProdutores(repository = mock_repository)
        request = UpdateProdutoresRequest(
            idProdutor = produtor.idProdutor,
            registroIndividual= "123.456.789-10",
            status = True,
            )
        
        use_case.execute(request)

        assert produtor.status is True
        mock_repository.update.assert_called_once_with(produtor)