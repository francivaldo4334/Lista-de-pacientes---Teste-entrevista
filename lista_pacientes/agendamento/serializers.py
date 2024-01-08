from rest_framework import serializers

from exame.models import Exame
from exame.serializers import ExameSerializer, ExameSerializerBodyRequest
from .models import Agendamento


class AgendamentoSerializerBodyResponse(serializers.ModelSerializer):
    paciente = serializers.IntegerField(source='paciente.id', read_only=True)
    status = serializers.CharField(source='paciente.status', read_only=True)
    exames = ExameSerializer(many=True, read_only=True)

    class Meta:
        model = Agendamento
        fields = ['id', 'agendado_para', 'criado_em', 'atualizado_em', 'paciente', 'status', 'exames']

    def to_representation(self, instance):
        query_exames = Exame.objects.filter(agendamento=instance)
        serializer_exames = ExameSerializer(query_exames, many=True).data
        instance.exames = serializer_exames
        return super().to_representation(instance)


class AgendamentoSerializerBodyRequest(serializers.ModelSerializer):
    paciente = 0
    exames = ExameSerializerBodyRequest(many=True)

    class Meta:
        model = Agendamento
        fields = ['id', 'agendado_para', 'paciente', 'exames']
