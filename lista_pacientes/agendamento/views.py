import json

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView

from pacientes.models import Paciente
from .models import Agendamento
from .serializers import AgendamentoSerializerBodyResponse, AgendamentoSerializerBodyRequest


# Create your views here.
class AgendamentoList(APIView):
    def get(self, request):
        agendamento_list = Agendamento.objects.all()
        serializate_response = AgendamentoSerializerBodyResponse(agendamento_list, many=True)
        return Response(
            serializate_response.data,
            status=200
        )

    @swagger_auto_schema(
        request_body=AgendamentoSerializerBodyRequest
    )
    def post(self, request):
        body = json.loads(request.body)
        param_paciente_id = body.get('paciente')
        agendado_para = body.get('agendado_para')
        try:
            paciente = Paciente.objects.get(id=int(param_paciente_id))
        except:
            return Response(
                "Error: 'paciente' not found.",
                status=400
            )
        new_agendamento = Agendamento(
            agendado_para=agendado_para,
            criado_em=timezone.now(),
            atualizado_em=timezone.now(),
            paciente=paciente
        )
        new_agendamento.save()
        serializer_response = AgendamentoSerializerBodyResponse(new_agendamento)
        return Response(
            serializer_response.data,
            status=201
        )

    @swagger_auto_schema(
        request_body=AgendamentoSerializerBodyRequest,
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description='Identificador unico do Agendamento.',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def put(self,request):
        body = json.loads(request.body)
        param_agendamento_id = request.query_params.get('id')
        param_paciente_id = body.get('paciente')
        agendado_para = body.get('agendado_para')
        try:
            agendamento = Agendamento.objects.get(id=int(param_agendamento_id))
        except:
            return Response(
                "Error: Param 'id' not found in 'agendameto'.",
                status=404
            )
        try:
            paciente = Paciente.objects.get(id=int(param_paciente_id))
        except:
            return Response(
                "Error: Item 'paciente' not found.",
                status=404
            )
        agendamento.agendado_para = agendado_para
        agendamento.paciente = paciente
        agendamento.atualizado_em = timezone.now()
        agendamento.save()
        serializate_response = AgendamentoSerializerBodyResponse(agendamento)
        return Response(
            serializate_response.data,
            status=200
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def delete(self,request):
        param_id = request.query_params.get('id')
        try:

            try:
                agendamento = Agendamento.objects.get(id=int(param_id))
            except:
                return Response(
                    "Error: Item 'agendamento' not found.",
                    status=404
                )
            agendamento.delete()
            return Response(
                "Item removed from database.",
                status=204
            )
        except:
            return Response(
                "Error: unspecified error.",
                status=500
            )

