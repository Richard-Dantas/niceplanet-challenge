from uuid import UUID
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