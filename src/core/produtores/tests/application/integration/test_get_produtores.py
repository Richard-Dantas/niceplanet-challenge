from uuid import UUID
import uuid
import pytest
from src.core.produtores.application.use_cases.get_produtores import GetProdutores, GetProdutoresRequest, GetProdutoresResponse
from src.core.produtores.domain.produtores import Produtores
from src.core.produtores.infra.in_memory_produtores_repository import InMemoryProdutoresRepository
from src.core.produtores.application.exceptions import ProdutoresNotFound


class TestGetProdutores:
    def test_get_produtores_by_id(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        repository = InMemoryProdutoresRepository(produtores=[produtor])
        use_case = GetProdutores(repository = repository)
        request = GetProdutoresRequest(
            idProdutor = produtor.idProdutor,
        )

        response = use_case.execute(request)
        
        assert response == GetProdutoresResponse(
            idProdutor = produtor.idProdutor,
            nomeProdutor = "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )

    def test_when_produtores_does_not_exist_then_raise_exception(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )
        repository = InMemoryProdutoresRepository(produtores=[produtor])
        use_case = GetProdutores(repository = repository)
        not_found_id = uuid.uuid4
        request = GetProdutoresRequest(
            idProdutor = not_found_id,
        )
        
        with pytest.raises(ProdutoresNotFound) as exc:
            use_case.execute(request)
