from rest_framework import serializers
from .models import Exame

class ExameSerializer(serializers.ModelSerializer):
    agendamento = serializers.IntegerField(source='agendamento.id',read_only=True)
    class Meta:
        model = Exame
        fields = ['tipo','criado_em','agendamento']