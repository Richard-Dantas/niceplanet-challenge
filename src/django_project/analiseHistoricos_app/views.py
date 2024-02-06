from uuid import UUID
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
    def list(self, request: Request):
        input = ListAnaliseHistoricoRequest()

        use_case= ListAnaliseHistorico(repository=DjangoORMAnaliseHistoricoRepository())
        response = use_case.execute(input)

        serializer = ListAnaliseHistoricoResponseSerializer(instance=response)

        return Response(status=HTTP_200_OK, data=serializer.data)
    
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