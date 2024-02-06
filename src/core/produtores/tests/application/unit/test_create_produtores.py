from unittest.mock import MagicMock
from uuid import UUID
import pytest

from src.core.produtores.application.use_cases.create_produtores import CreateProdutores, CreateProdutoresRequest
from src.core.produtores.application.exceptions import InvalidProdutoresData
from src.core.produtores.domain.IRepository.produtores_repository import ProdutoresRepository


class TestCreateProdutores:
    def test_create_produtores_with_valid_data(self):
        mock_repository = MagicMock(ProdutoresRepository)
        use_case = CreateProdutores(repository = mock_repository)
        request = CreateProdutoresRequest(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )

        response = use_case.execute(request)
        
        assert response.idProdutor is not None
        assert isinstance(response.idProdutor, UUID)
        assert mock_repository.save.called

    def test_create_produtores_with_invalid_data(self):
        use_case = CreateProdutores(MagicMock(ProdutoresRepository))
        
        with pytest.raises(InvalidProdutoresData, match="Registro Individual não pode ser vazio"):
            produtor_id = use_case.execute(CreateProdutoresRequest(
                nomeProdutor= "",
                registroIndividual= "",
                ))