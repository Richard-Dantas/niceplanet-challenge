from uuid import UUID
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from core.analiseHistorico.application.exceptions import AnaliseHistoricoNotFound
from core.analiseHistorico.application.use_cases.create_analiseHistorico import CreateAnaliseHistorico, CreateAnaliseHistoricoRequest, CreateAnaliseHistoricoResponse
from core.analiseHistorico.application.use_cases.delete_analiseHistorico import DeleteAnaliseHistorico, DeleteAnaliseHistoricoRequest
from core.analiseHistorico.application.use_cases.get_analiseHistorico import GetAnaliseHistorico, GetAnaliseHistoricoRequest


from core.analiseHistorico.application.use_cases.list_analiseHistorico import ListAnaliseHistorico, ListAnaliseHistoricoRequest
from django_project.analiseHistoricos_app.repository import DjangoORMAnaliseHistoricoRepository
from django_project.analiseHistoricos_app.serializers import CreateAnaliseHistoricoRequestSerializer, CreateAnaliseHistoricoResponseSerializer, DeleteAnaliseHistoricoRequestSerializer, ListAnaliseHistoricoResponseSerializer, RetrieveAnaliseHistoricoRequestSerializer, RetrieveAnaliseHistoricoResponseSerializer

class AnaliseHistoricoViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Esta é uma rota de listagem de casos analisados que faz parte do escopo de teste e retorna informações básicas do caso analisado",
        responses={200: openapi.Response('Success', ListAnaliseHistoricoResponseSerializer)},
        tags=['AnaliseHistorico'],
    )
    def list(self, request: Request):
        input = ListAnaliseHistoricoRequest()

        use_case= ListAnaliseHistorico(repository=DjangoORMAnaliseHistoricoRepository())
        response = use_case.execute(input)

        serializer = ListAnaliseHistoricoResponseSerializer(instance=response)

        return Response(status=HTTP_200_OK, data=serializer.data)
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de busca de casos analisados a partir de seu ID que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        responses={200: openapi.Response('Success', RetrieveAnaliseHistoricoResponseSerializer)},
        tags=['AnaliseHistorico'],
    )
    def retrieve(self, request: Request, pk=None):
        serializer = RetrieveAnaliseHistoricoRequestSerializer(data={"idAnaliseHistorico": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetAnaliseHistorico(repository=DjangoORMAnaliseHistoricoRepository())
        
        try:
            result = use_case.execute(request=GetAnaliseHistoricoRequest(idAnaliseHistorico=serializer.validated_data["idAnaliseHistorico"]))
        except AnaliseHistoricoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        produtor_output = RetrieveAnaliseHistoricoResponseSerializer(instance=result)
        

        return Response(
            status=HTTP_200_OK,
            data= produtor_output.data,
        )
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de criação de casos analisados que NÃO FAZ parte do escopo do teste e não está funcional",
        request_body=CreateAnaliseHistoricoRequestSerializer,
        responses={200: openapi.Response('Success')},
        tags=['AnaliseHistorico'],
    )
    def create(self, request: Request) -> Response:
        serializer = CreateAnaliseHistoricoRequestSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateAnaliseHistoricoRequest(**serializer.validated_data)
        use_case = CreateAnaliseHistorico(repository=DjangoORMAnaliseHistoricoRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateAnaliseHistoricoResponseSerializer(instance=output).data,
        )
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de deleção de casos analisados que faz parte do escopo de teste e retorna um código de sucesso",
        responses={200: openapi.Response('Success')},
        tags=['AnaliseHistorico'],
    )
    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteAnaliseHistoricoRequestSerializer(data={"idAnaliseHistorico": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteAnaliseHistorico(repository = DjangoORMAnaliseHistoricoRepository())
        try:
            use_case.execute(request=DeleteAnaliseHistoricoRequest(idAnaliseHistorico=serializer.validated_data["idAnaliseHistorico"]))
        except AnaliseHistoricoNotFound as e:
            print(e)
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)