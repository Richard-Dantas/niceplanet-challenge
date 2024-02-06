from unittest.mock import create_autospec
import uuid, pytest
from src.core.produtores.application.exceptions import ProdutoresNotFound
from src.core.produtores.application.use_cases.delete_produtores import DeleteProdutores, DeleteProdutoresRequest
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository

from src.core.produtores.domain.produtores import Produtores


class TestDeleteProdutores:
    def test_delete_produtores_from_repository(self):
        produtor = Produtores(
            idProdutor= uuid.uuid4(),
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.get_by_id.return_value = produtor

        use_case = DeleteProdutores(mock_repository)
        use_case.execute(DeleteProdutoresRequest(idProdutor= produtor.idProdutor))
        
        mock_repository.delete.assert_called_once_with(produtor.idProdutor)


    def test_when_produtores_not_found_then_raise_exception(self):
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteProdutores(mock_repository)
        
        with pytest.raises(ProdutoresNotFound):
            use_case.execute(DeleteProdutoresRequest(idProdutor=uuid.uuid4()))

        mock_repository.delete.assert_not_called()