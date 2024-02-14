from uuid import UUID
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.request import Request
from core.analiseHistorico.application.use_cases.create_analiseHistorico import CreateAnaliseHistorico, CreateAnaliseHistoricoRequest
from core.analiseHistorico.domain.IRepository.analiseHistoricoRepository import AnaliseHistoricoRepository
from core.propriedades.application.exceptions import PropriedadesNotFound
from core.propriedades.application.use_cases.create_propriedades import CreatePropriedades, CreatePropriedadesRequest

from core.propriedades.application.use_cases.get_propriedades import GetPropriedades, GetPropriedadesRequest
from core.propriedades.application.use_cases.patch_propriedades import PatchPropriedades, PatchPropriedadesRequest
from django_project.analiseHistoricos_app.repository import DjangoORMAnaliseHistoricoRepository
from django_project.produtores_app.repository import DjangoORMProdutoresRepository
from django_project.propriedades_app.repository import DjangoORMPropriedadesRepository
from django_project.propriedades_app.serializers import CreatePropriedadesRequestSerializer, CreatePropriedadesResponseSerializer, PatchPropriedadesRequestSerializer, RetrievePropriedadesRequestSerializer, RetrievePropriedadesResponseSerializer
from django_project.vinculos_app.repository import DjangoORMVinculosRepository

class PropriedadesViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Esta é a rota de busca de propriedades a partir de seu numeroCar que faz parte do escopo do teste, retornando os atributos de propriedade que foram solicitados bem como atributos dos produtores vinculados. Você pode testar buscar por exemplo: MA-2102804-2PNU380GY64UHORJNIPM9J84Y5UHTRJFK",
        responses={200: openapi.Response('Success', RetrievePropriedadesResponseSerializer)},
        tags=['Propriedades'],
    )
    def retrieve(self, request: Request, pk=None):
        serializer = RetrievePropriedadesRequestSerializer(data={"numeroCar": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetPropriedades(
            propriedade_repository=DjangoORMPropriedadesRepository(),
            produtor_repository= DjangoORMProdutoresRepository(),
            vinculo_repository= DjangoORMVinculosRepository(),
        )
        
        try:
            result = use_case.execute(request=GetPropriedadesRequest(numeroCar=serializer.validated_data["numeroCar"]))
        except PropriedadesNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        use_case_historico = CreateAnaliseHistorico(repository= DjangoORMAnaliseHistoricoRepository())
        use_case_historico.execute(request=CreateAnaliseHistoricoRequest(
            nomePropriedade=result.nomePropriedade, 
            numeroCar=result.numeroCar))

        propriedade_output = RetrievePropriedadesResponseSerializer(instance=result)

        return Response(
            status=HTTP_200_OK,
            data= propriedade_output.data,
        )
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de criação de propriedades que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        request_body=CreatePropriedadesRequestSerializer,
        responses={200: openapi.Response('Success', CreatePropriedadesResponseSerializer)},
        tags=['Propriedades'],
    )
    def create(self, request: Request) -> Response:
        serializer = CreatePropriedadesRequestSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        input = CreatePropriedadesRequest(**serializer.validated_data)
        use_case = CreatePropriedades(repository=DjangoORMPropriedadesRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreatePropriedadesResponseSerializer(instance=output).data,
        )
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de edição/atualização de propriedades que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        request_body=PatchPropriedadesRequestSerializer,
        responses={200: openapi.Response('Success')},
        tags=['Propriedades'],
    )
    def update(self, request: Request, pk:UUID=None) -> Response:
        serializer = PatchPropriedadesRequestSerializer(
            data = {
                **request.data,
                "idPropriedade": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = PatchPropriedadesRequest(**serializer.validated_data)
        use_case = PatchPropriedades(repository=DjangoORMPropriedadesRepository())
        try:
            use_case.execute(request=input)
        except PropriedadesNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status = HTTP_204_NO_CONTENT)