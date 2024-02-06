from rest_framework import serializers

class VinculosResponseSerializer(serializers.Serializer):
    idVinculo = serializers.UUIDField()
    idPropriedade = serializers.UUIDField()
    idProdutor = serializers.UUIDField()

class CreateVinculosRequestSerializer(serializers.Serializer):
    idPropriedade = serializers.UUIDField()
    idProdutor = serializers.UUIDField()

class CreateVinculosResponseSerializer(serializers.Serializer):
    idVinculo = serializers.UUIDField()