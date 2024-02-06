from rest_framework import serializers

class ProdutoresResponseSerializer(serializers.Serializer):
    idProdutor = serializers.UUIDField()
    nomeProdutor = serializers.CharField(max_length=255, allow_blank=False)
    registroIndividual = serializers.CharField(max_length=14, allow_blank=False)
    status = serializers.BooleanField()


class ListProdutoresResponseSerializer(serializers.Serializer):
    data  = ProdutoresResponseSerializer(many=True)


class RetrieveProdutoresRequestSerializer(serializers.Serializer):
    idProdutor = serializers.UUIDField()


class RetrieveProdutoresResponseSerializer(serializers.Serializer):
    data = ProdutoresResponseSerializer(source="*")

class CreateProdutoresRequestSerializer(serializers.Serializer):
    nomeProdutor = serializers.CharField(max_length=255, allow_blank=False)
    registroIndividual = serializers.CharField(max_length=14, allow_blank=False)
    status = serializers.BooleanField(default=True)

class CreateProdutoresResponseSerializer(serializers.Serializer):
    idProdutor = serializers.UUIDField()

class UpdateProdutoresRequestSerializer(serializers.Serializer):
    idProdutor = serializers.UUIDField()
    nomeProdutor = serializers.CharField(max_length=255, allow_blank=False)
    registroIndividual = serializers.CharField(max_length=14, allow_blank=False)
    status = serializers.BooleanField()

class DeleteProdutoresRequestSerializer(serializers.Serializer):
    idProdutor = serializers.UUIDField()