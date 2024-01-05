from rest_framework import serializers
from .models import Agendamento
class AgendamentoSerializerBodyResponse(serializers.ModelSerializer):
    paciente = serializers.IntegerField(source='paciente.id', read_only=True)
    status = serializers.CharField(source='paciente.status',read_only=True)
    class Meta:
        model = Agendamento
        fields = ['id','agendado_para','criado_em','atualizado_em','paciente','status']
class AgendamentoSerializerBodyRequest(serializers.ModelSerializer):
    paciente = 0
    class Meta:
        model = Agendamento
        fields = ['id','agendado_para','paciente']