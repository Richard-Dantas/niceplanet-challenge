from unittest.mock import MagicMock, create_autospec
from uuid import UUID
import uuid
import pytest

from src.core.produtores.application.use_cases.create_produtores import CreateProdutores, CreateProdutoresRequest
from src.core.produtores.application.exceptions import InvalidProdutoresData, ProdutoresNotFound
from src.core.produtores.application.use_cases.get_produtores import GetProdutores, GetProdutoresRequest, GetProdutoresResponse
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository
from src.core.produtores.domain.produtores import Produtores


class TestGetProdutores:
    def test_get_return_found_produtores(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.get_by_id.return_value = produtor
        use_case = GetProdutores(repository = mock_repository)
        request = GetProdutoresRequest(
            idProdutor= produtor.idProdutor
        )

        response = use_case.execute(request)
        
        assert response == GetProdutoresResponse(
            idProdutor = produtor.idProdutor,
            nomeProdutor = "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )

    def test_get_when_produtores_not_found_then_raise_exception(self):
        mock_repository = create_autospec(ProdutoresRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetProdutores(repository=mock_repository)
        request = GetProdutoresRequest(idProdutor=uuid.uuid4())

        with pytest.raises(ProdutoresNotFound):
            use_case.execute(request)