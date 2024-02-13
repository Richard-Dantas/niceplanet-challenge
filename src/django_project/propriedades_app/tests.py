from django.test import TestCase
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from core.produtores.domain.produtores import Produtores
from core.propriedades.domain.propriedades import Propriedades
from core.vinculos.domain.vinculos import Vinculos
from django_project.produtores_app.repository import DjangoORMProdutoresRepository
from django_project.propriedades_app.repository import DjangoORMPropriedadesRepository
from django.contrib.auth.models import User

from django_project.vinculos_app.repository import DjangoORMVinculosRepository

@pytest.fixture
def produtor_test():
    return Produtores(
        nomeProdutor="Teste da Silva",
        registroIndividual="123.456.789-10",
        status=True,
    )

@pytest.fixture
def propriedade_test():
    return Propriedades(
        nomePropriedade="Propriedade da Silva",
        numeroCar="TO-15235304-5381E1396BB4E6TFBA16CA5AE14745212",
        uf="TO",
        municipio="Palmas",
        pais="Brasil",
        liberado=1,
        status=True,
    )

@pytest.fixture
def produtores_repository() -> DjangoORMProdutoresRepository:
    return DjangoORMProdutoresRepository()

@pytest.fixture
def propriedade_repository() -> DjangoORMPropriedadesRepository:
    return DjangoORMPropriedadesRepository()

@pytest.fixture
def vinculos_repository() -> DjangoORMVinculosRepository:
    return DjangoORMVinculosRepository()

@pytest.fixture
def create_superuser():
    user = User.objects.create_superuser(username='root', password='root')
    return user

def get_access_token(client: APIClient, username: str, password: str) -> str:
    response = client.post('/api/token/', {'username': username, 'password': password}, format='json')
    return response.json().get('access', '')

@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid_return_400(self, create_superuser) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        url = '/api/propriedades/123123123123/'
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_return_propriedades_when_exists(
        self,
        propriedade_test: Propriedades,
        produtor_test: Produtores,
        propriedade_repository: DjangoORMPropriedadesRepository,
        produtores_repository: DjangoORMProdutoresRepository,
        vinculos_repository: DjangoORMVinculosRepository,
        create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')

        produtores_repository.save(produtor_test)
        propriedade_repository.save(propriedade_test)

        vinculo = Vinculos(
            idProdutor=produtor_test.idProdutor,
            idPropriedade=propriedade_test.idPropriedade
        )

        vinculos_repository.save(vinculo)

        url = f'/api/propriedades/{propriedade_test.numeroCar}/'
        response = APIClient().get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        expected_data = {
            "idPropriedade": str(propriedade_test.idPropriedade),
            "nomePropriedade": "Propriedade da Silva",
            "numeroCar": "TO-15235304-5381E1396BB4E6TFBA16CA5AE14745212",
            "uf": "TO",
            "municipio": "Palmas",
            "pais": "Brasil",
            "liberado": 1,
            "status": True,
            "produtores_vinculados": [
                {
                    "idProdutor": str(produtor_test.idProdutor),
                    "nomeProdutor": "Teste da Silva",
                    "registroIndividual": "123.456.789-10",
                    "status": True,
                }
            ]
        }
        
        assert response.data == expected_data
        assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self, create_superuser) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        url = '/api/propriedades/123123123123/'
        response = client.put(
            url,
            data={
                "liberado": "2",
            },
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_return_204(
            self,
            propriedade_test: Propriedades,
            propriedade_repository: DjangoORMPropriedadesRepository,
            create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        propriedade_repository.save(propriedade_test)

        url = f'/api/propriedades/{propriedade_test.idPropriedade}/'
        response = client.put(
            url,
            data={
                "idPropriedade": propriedade_test.idPropriedade,
                "liberado": 2,
            },
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )
