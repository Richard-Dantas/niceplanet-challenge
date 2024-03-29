from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT


from core.vinculos.application.use_cases.create_vinculo import CreateVinculos, CreateVinculosRequest
from django_project.vinculos_app.repository import DjangoORMVinculosRepository
from django_project.vinculos_app.serializers import CreateVinculosRequestSerializer, CreateVinculosResponseSerializer

class VinculosViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Esta é uma rota de criação de vinculos que apesar de não fazer parte do escopo do teste, está funcional e pode ser utilizada",
        request_body=CreateVinculosRequestSerializer,
        responses={200: openapi.Response('Success', CreateVinculosResponseSerializer)},
        tags=['Vinculos'],
    )
    def create(self, request: Request) -> Response:
        serializer = CreateVinculosRequestSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateVinculosRequest(**serializer.validated_data)
        use_case = CreateVinculos(repository=DjangoORMVinculosRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateVinculosResponseSerializer(instance=output).data,
        )