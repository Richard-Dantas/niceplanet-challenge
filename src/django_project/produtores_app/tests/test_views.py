import uuid
from django.test import TestCase
from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from core.produtores.domain.produtores import Produtores
from django_project.produtores_app.repository import DjangoORMProdutoresRepository


@pytest.fixture
def produtor_test():
    return Produtores(
        nomeProdutor="Teste da Silva",
        registroIndividual="123.456.789-10",
        status=True,
    )
    
@pytest.fixture
def produtores_repository() -> DjangoORMProdutoresRepository:
    return DjangoORMProdutoresRepository()

@pytest.fixture
def create_superuser():
    user = User.objects.create_superuser(username='root', password='root')
    return user

def get_access_token(client: APIClient, username: str, password: str) -> str:
    response = client.post('/api/token/', {'username': username, 'password': password}, format='json')
    return response.json().get('access', '')

@pytest.mark.django_db
class TestListAPI:
    def test_list_produtores(
        self,
        produtor_test: Produtores,
        produtores_repository: DjangoORMProdutoresRepository,
        create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        produtores_repository.save(produtor_test)

        url = "/api/produtores/"
        response = APIClient().get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        expected_data = {
            "data": [
                {
                    "idProdutor": str(produtor_test.idProdutor),
                    "nomeProdutor": "Teste da Silva",
                    "registroIndividual": "123.456.789-10",
                    "status": True,
                },
            ],
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid_return_400(self, create_superuser) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        url = '/api/produtores/123123123123/'
        response = APIClient().get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_produtores_when_exists(
        self,
        produtor_test: Produtores,
        produtores_repository: DjangoORMProdutoresRepository,
        create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        produtores_repository.save(produtor_test)

        url = f'/api/produtores/{produtor_test.idProdutor}/'
        response = APIClient().get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        expected_data = {
            "data": {
                "idProdutor": str(produtor_test.idProdutor),
                "nomeProdutor": "Teste da Silva",
                "registroIndividual": "123.456.789-10",
                "status": True,
            }
        }
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self, create_superuser) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        url = '/api/produtores/'
        response = APIClient().post(
            url,
            data={
                "nomeProdutor": "",
                "registroIndividual": "",
            },
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_when_payload_is_valid_then_return_201(
            self,
            produtores_repository: DjangoORMProdutoresRepository,
            create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        url = '/api/produtores/'
        response = APIClient().post(
            url,
            data={
                "nomeProdutor": "Teste",
                "registroIndividual": "123.456.789-10",
            }
            , HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        assert response.status_code == status.HTTP_201_CREATED
        created_produtor_id = uuid.UUID(response.data["idProdutor"])
        assert produtores_repository.get_by_id(created_produtor_id) == Produtores(
            idProdutor=created_produtor_id,
            nomeProdutor="Teste",
            registroIndividual="123.456.789-10",
        )

        assert produtores_repository.list() == [
            Produtores(
                idProdutor=uuid.UUID(response.data["idProdutor"]),
                nomeProdutor="Teste",
                registroIndividual="123.456.789-10",
            )
        ]

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self, create_superuser) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        url = '/api/produtores/123123123123/'
        response = APIClient().put(
            url,
            data={
                "nomeProdutor": "",
                "registroIndividual": "123.456.789-10",
            }
            , HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_return_204(
            self,
            produtor_test: Produtores,
            produtores_repository: DjangoORMProdutoresRepository,
            create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        produtores_repository.save(produtor_test)

        url = f'/api/produtores/{produtor_test.idProdutor}/'
        response = APIClient().put(
            url,
            data={
                "idProdutor": produtor_test.idProdutor,
                "nomeProdutor": "Testando",
                "registroIndividual": "123.456.789-10",
                "status": True
            }
            , HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )



@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_idProdutor_is_invalid_then_return_400(self, create_superuser) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        url = '/api/produtores/123123123123/'
        response = APIClient().delete(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_produtores_does_exist_then_delete_and_return_204(
            self,
            produtor_test: Produtores,
            produtores_repository: DjangoORMProdutoresRepository,
            create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        produtores_repository.save(produtor_test)

        url = f'/api/produtores/{produtor_test.idProdutor}/'
        response = APIClient().delete(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert produtores_repository.list() == []