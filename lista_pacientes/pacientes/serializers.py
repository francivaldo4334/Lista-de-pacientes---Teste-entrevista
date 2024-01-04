from rest_framework import serializers
from .models import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    criado_em = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    atualizado_em = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Paciente
        fields = ['id','nome','idade','status','sexo','preferencial','criado_em','atualizado_em']