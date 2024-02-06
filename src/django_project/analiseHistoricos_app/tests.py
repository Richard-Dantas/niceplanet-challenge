from datetime import datetime
from django.test import TestCase
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django_project.analiseHistoricos_app.repository import DjangoORMAnaliseHistoricoRepository
from django.contrib.auth.models import User
from django_project.propriedades_app.models import Propriedades
from django_project.analiseHistoricos_app.models import AnaliseHistorico
from django_project.propriedades_app.repository import DjangoORMPropriedadesRepository

@pytest.fixture
def propriedade_test():
    return Propriedades(
        nomePropriedade="Propriedade da Silva",
        numeroCar="TO-15235304-5381E1396BB4E6TFBA16CA5AE14745213",
        uf="TO",
        municipio="Palmas",
        pais="Brasil",
        liberado=1,
        status=True,
    )

@pytest.fixture
def propriedade_repository() -> DjangoORMPropriedadesRepository:
    return DjangoORMPropriedadesRepository()

@pytest.fixture
def analiseHistorico_repository() -> DjangoORMAnaliseHistoricoRepository:
    return DjangoORMAnaliseHistoricoRepository()

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
        print(access_token)
        url = '/api/analiseHistoricos/123123123123/'
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_analiseHistorico_when_exists(
        self,
        propriedade_test: Propriedades,
        analiseHistorico_repository: DjangoORMAnaliseHistoricoRepository,
        propriedade_repository: DjangoORMPropriedadesRepository,
        create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')

        propriedade_repository.save(propriedade_test)

        analiseHistorico = AnaliseHistorico(
            nomePropriedade = propriedade_test.nomePropriedade,
            numeroCar = propriedade_test.numeroCar,
            dateAnalise = datetime.now()
        )
        analiseHistorico_repository.save(analiseHistorico)

        url = f'/api/analiseHistoricos/{analiseHistorico.idAnaliseHistorico}/'
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        expected_data = {
            "data": {
                "idAnaliseHistorico": str(analiseHistorico.idAnaliseHistorico),
                "nomePropriedade": propriedade_test.nomePropriedade,
                "numeroCar": propriedade_test.numeroCar,
                "dateAnalise": analiseHistorico.dateAnalise.strftime('%Y-%m-%d'),
            }
        }
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

@pytest.mark.django_db
class TestListAPI:
    def test_list_analiseHistorico(
        self,
        propriedade_test: Propriedades,
        analiseHistorico_repository: DjangoORMAnaliseHistoricoRepository,
        propriedade_repository: DjangoORMPropriedadesRepository,
        create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')

        propriedade_repository.save(propriedade_test)

        analiseHistorico = AnaliseHistorico(
            nomePropriedade = propriedade_test.nomePropriedade,
            numeroCar = propriedade_test.numeroCar,
            dateAnalise = datetime.now()
        )
        analiseHistorico_repository.save(analiseHistorico)

        url = "/api/analiseHistoricos/"
        response = APIClient().get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        expected_data = {
            "data": [
                {
                    "idAnaliseHistorico": str(analiseHistorico.idAnaliseHistorico),
                    "nomePropriedade": propriedade_test.nomePropriedade,
                    "numeroCar": propriedade_test.numeroCar,
                    "dateAnalise": analiseHistorico.dateAnalise.strftime('%Y-%m-%d'),
                },
            ],
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_idAnaliseHistorico_is_invalid_then_return_400(self, create_superuser) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')
        url = '/api/analiseHistoricos/123123123123/'
        response = APIClient().delete(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_analiseHistorico_does_exist_then_delete_and_return_204(
        self,
        propriedade_test: Propriedades,
        analiseHistorico_repository: DjangoORMAnaliseHistoricoRepository,
        propriedade_repository: DjangoORMPropriedadesRepository,
        create_superuser
    ) -> None:
        client = APIClient()
        access_token = get_access_token(client, 'root', 'root')

        propriedade_repository.save(propriedade_test)

        analiseHistorico = AnaliseHistorico(
            nomePropriedade = propriedade_test.nomePropriedade,
            numeroCar = propriedade_test.numeroCar,
            dateAnalise = datetime.now()
        )
        analiseHistorico_repository.save(analiseHistorico)

        url = f'/api/analiseHistoricos/{analiseHistorico.idAnaliseHistorico}/'
        response = APIClient().delete(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert analiseHistorico_repository.list() == []