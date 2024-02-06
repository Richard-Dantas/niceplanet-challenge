from rest_framework import serializers

class AnaliseHistoricoResponseSerializer(serializers.Serializer):
    idAnaliseHistorico = serializers.UUIDField()
    nomePropriedade = serializers.CharField(max_length=255, allow_blank=False)
    numeroCar = serializers.CharField(max_length=255, allow_blank=False)
    dateAnalise = serializers.SerializerMethodField()

    def get_dateAnalise(self, obj):
            # Formate a data antes de ser serializada
            return obj.dateAnalise.strftime('%Y-%m-%d')

class ListAnaliseHistoricoResponseSerializer(serializers.Serializer):
    data  = AnaliseHistoricoResponseSerializer(many=True)


class RetrieveAnaliseHistoricoRequestSerializer(serializers.Serializer):
    idAnaliseHistorico = serializers.UUIDField()


class RetrieveAnaliseHistoricoResponseSerializer(serializers.Serializer):
    data = AnaliseHistoricoResponseSerializer(source="*")

class CreateAnaliseHistoricoRequestSerializer(serializers.Serializer):
    dateAnalise = serializers.DateField()
    nomePropriedade = serializers.CharField(max_length=255, allow_blank=False)
    numeroCar = serializers.CharField(max_length=255, allow_blank=False)

class CreateAnaliseHistoricoResponseSerializer(serializers.Serializer):
    idAnaliseHistorico = serializers.UUIDField()


class DeleteAnaliseHistoricoRequestSerializer(serializers.Serializer):
    idAnaliseHistorico = serializers.UUIDField()
