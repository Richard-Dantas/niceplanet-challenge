from rest_framework import serializers
from django_project.produtores_app.serializers import ProdutoresResponseSerializer

from django_project.propriedades_app.models import Propriedades

class PropriedadesResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propriedades
        fields = ['idPropriedade', 'nomePropriedade', 'numeroCar', 'uf', 'municipio', 'pais', 'status']

class RetrievePropriedadesRequestSerializer(serializers.Serializer):
    numeroCar = serializers.CharField()

class RetrievePropriedadesResponseSerializer(serializers.ModelSerializer):
    produtores_vinculados = ProdutoresResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Propriedades
        fields = ['idPropriedade', 'nomePropriedade', 'numeroCar', 'uf', 'municipio', 'pais', 'status', 'liberado', 'produtores_vinculados']

class CreatePropriedadesRequestSerializer(serializers.Serializer):
    nomePropriedade = serializers.CharField(max_length=255)
    numeroCar = serializers.CharField(max_length=255)
    uf = serializers.CharField(max_length=2)
    municipio = serializers.CharField(max_length=255)
    pais = serializers.CharField(max_length=255)
    liberado = serializers.ChoiceField(choices=Propriedades.StatusLiberado.choices, default=Propriedades.StatusLiberado.BLOQUEADO)
    status = serializers.BooleanField(default=True)

class CreatePropriedadesResponseSerializer(serializers.Serializer):
    idPropriedade = serializers.UUIDField()

class PatchPropriedadesRequestSerializer(serializers.Serializer):
    idPropriedade = serializers.UUIDField()
    liberado = serializers.ChoiceField(choices=Propriedades.StatusLiberado.choices)