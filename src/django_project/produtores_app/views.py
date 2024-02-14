from uuid import UUID
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from core.produtores.application.exceptions import ProdutoresNotFound
from core.produtores.application.use_cases.create_produtores import CreateProdutores, CreateProdutoresRequest
from core.produtores.application.use_cases.delete_produtores import DeleteProdutores, DeleteProdutoresRequest
from core.produtores.application.use_cases.get_produtores import GetProdutores, GetProdutoresRequest

from core.produtores.application.use_cases.list_produtores import ListProdutores, ListProdutoresRequest,ListProdutoresResponse
from core.produtores.application.use_cases.update_produtores import UpdateProdutores, UpdateProdutoresRequest
from django_project.produtores_app.repository import DjangoORMProdutoresRepository
from django_project.produtores_app.serializers import CreateProdutoresRequestSerializer, CreateProdutoresResponseSerializer, DeleteProdutoresRequestSerializer, ListProdutoresResponseSerializer, RetrieveProdutoresRequestSerializer, RetrieveProdutoresResponseSerializer, UpdateProdutoresRequestSerializer

class ProdutoresViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Esta é uma rota de listagem de produtores que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        responses={200: openapi.Response('Success', ListProdutoresResponseSerializer)},
        tags=['Produtores'],
    )
    def list(self, request: Request):
        input = ListProdutoresRequest()

        use_case= ListProdutores(repository=DjangoORMProdutoresRepository())
        response = use_case.execute(input)

        serializer = ListProdutoresResponseSerializer(instance=response)

        return Response(status=HTTP_200_OK, data=serializer.data)
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de busca de produtores a partir do seu ID que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        responses={200: openapi.Response('Success', RetrieveProdutoresResponseSerializer)},
        tags=['Produtores'],
    )
    def retrieve(self, request: Request, pk=None):
        serializer = RetrieveProdutoresRequestSerializer(data={"idProdutor": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetProdutores(repository=DjangoORMProdutoresRepository())
        
        try:
            result = use_case.execute(request=GetProdutoresRequest(idProdutor=serializer.validated_data["idProdutor"]))
        except ProdutoresNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        produtor_output = RetrieveProdutoresResponseSerializer(instance=result)

        return Response(
            status=HTTP_200_OK,
            data= produtor_output.data,
        )
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de criação de produtores que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        request_body=CreateProdutoresRequestSerializer,
        responses={200: openapi.Response('Success', CreateProdutoresResponseSerializer)},
        tags=['Produtores'],
    )
    def create(self, request: Request) -> Response:
        serializer = CreateProdutoresRequestSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateProdutoresRequest(**serializer.validated_data)
        use_case = CreateProdutores(repository=DjangoORMProdutoresRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateProdutoresResponseSerializer(instance=output).data,
        )
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de edição/atualização de produtores que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        request_body=UpdateProdutoresRequestSerializer,
        responses={200: openapi.Response('Success')},
        tags=['Produtores'],
    )
    def update(self, request: Request, pk:UUID=None) -> Response:
        serializer = UpdateProdutoresRequestSerializer(
            data = {
                **request.data,
                "idProdutor": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateProdutoresRequest(**serializer.validated_data)
        use_case = UpdateProdutores(repository=DjangoORMProdutoresRepository())
        try:
            use_case.execute(request=input)
        except ProdutoresNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status = HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_description="Esta é uma rota de deleção de produtores que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        responses={200: openapi.Response('Success')},
        tags=['Produtores'],
    )
    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteProdutoresRequestSerializer(data={"idProdutor": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteProdutores(repository = DjangoORMProdutoresRepository())
        try:
            use_case.execute(request=DeleteProdutoresRequest(idProdutor=serializer.validated_data["idProdutor"]))
        except ProdutoresNotFound as e:
            print(e)
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)