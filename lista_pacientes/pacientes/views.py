import json

from django.db.models import Q
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paciente
from .serializers import PacienteSerializer


# Create your views here.
class PacienteList(APIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def valid_paciente_params(
            self,
            preferencial,
            sexo,
            status,
            idade,
            nome
    ):
        if idade >= 65 and preferencial != Paciente.CondicaoPreferencial.PESSOA_IDOSA.value:
            return (
                f"Error: elderly patient but was not informed '{Paciente.CondicaoPreferencial.PESSOA_IDOSA.value}' in the param 'preferencial'.",
                400
            )
        elif idade < 65 and preferencial == Paciente.CondicaoPreferencial.PESSOA_IDOSA.value:
            return (
                f"Error: patient is not preferential '{Paciente.CondicaoPreferencial.PESSOA_IDOSA.value}' in the param 'preferencial'.",
                400
            )
        elif not preferencial in Paciente.CondicaoPreferencial.values:
            return (
                f"Error: value 'preferencial' is invalid. valid params {Paciente.CondicaoPreferencial.values}",
                400
            )
        elif not sexo in Paciente.Sexo.values:
            return (
                f"Error: value 'sexo' is invalid. valid params {Paciente.Sexo.values}",
                400
            )
        elif not status in Paciente.StatusAndamento.values:
            return (
                f"Error: value 'status' is invalid. valid params {Paciente.StatusAndamento.values}",
                400
            )
        elif idade <= 0 or idade >= 500:
            return (
                "Error: value 'idade' is invalid.",
                400
            )
        elif not nome:
            return (
                "Error: value 'nome' is invalid."
            )
        else:
            return (
                "successs",
                200
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Parametro de pesquisa por estado de andamento do paciente.",
                type=openapi.TYPE_STRING,
                enum=['Aguardando', 'Cancelado', 'EmAtendimento', 'Concluído']
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description='Data inícial em formato [yyyy-MM-dd]',
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description='Data final em formato [yyyy-MM-dd]',
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'preferencial',
                openapi.IN_QUERY,
                description='Filtar pacientes com preferencia.',
                type=openapi.TYPE_STRING,
                enum=['false', 'true']
            )
        ]
    )
    def get(self, request):
        status = request.query_params.get('status')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        is_preferencial = request.query_params.get('preferencial')
        if start_date and end_date and start_date != end_date:
            pacientes = Paciente.objects.filter(criado_em__range=[start_date, end_date])
        elif start_date:
            pacientes = Paciente.objects.filter(criado_em__gte=start_date)
        elif end_date:
            pacientes = Paciente.objects.filter(
                Q(criado_em__lt=end_date) | Q(criado_em=end_date)
            )
        else:
            pacientes = Paciente.objects.all()
        if status is not None:
            pacientes = pacientes.filter(status=status)
        if is_preferencial == 'true':
            pacientes = pacientes.exclude(preferencial=Paciente.CondicaoPreferencial.NAO_PREFERENCIAL.value)
        order_list = sorted(
            pacientes,
            key=lambda paciente: (
                paciente.criado_em
            ),
            reverse=True
        )
        order_list = sorted(
            order_list,
            key=lambda paciente: (
                    paciente.preferencial != Paciente.CondicaoPreferencial.NAO_PREFERENCIAL.value
            ),
            reverse=True
        )
        serializer_response = PacienteSerializer(order_list, many=True)
        return Response(serializer_response.data)

    @swagger_auto_schema(
        request_body=PacienteSerializer
    )
    def post(self, request):
        body = json.loads(request.body)
        preferencial = body.get('preferencial')
        sexo = body.get('sexo')
        status = body.get('status')
        idade = int(body.get('idade'))
        nome = body.get('nome')
        criado_em = timezone.now()
        (text_response, status_response) = self.valid_paciente_params(
            preferencial,
            sexo,
            status,
            idade,
            nome
        )
        if status_response != 200:
            return Response(
                text_response,
                status_response
            )
        new_paciente = Paciente(
            preferencial=preferencial,
            sexo=sexo,
            status=status,
            idade=idade,
            nome=nome,
            criado_em=criado_em,
        )
        new_paciente.save()
        response_serializer = PacienteSerializer(new_paciente)
        return Response(
            response_serializer.data,
            status=201
        )

    @swagger_auto_schema(
        request_body=PacienteSerializer,
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description='identificador unico do paciente.',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def put(self, request):
        body = json.loads(request.body)
        preferencial = body.get('preferencial')
        sexo = body.get('sexo')
        status = body.get('status')
        idade = int(body.get('idade'))
        nome = body.get('nome')
        param_id = request.query_params.get('id')
        if param_id is None:
            return Response(
                "Error: param id is invalid.",
                status=400
            )
        try:
            paciente = Paciente.objects.get(id=int(param_id))
        except:
            return Response(
                "Error: item does not exist.",
                status=404
            )
        (text_response, status_response) = self.valid_paciente_params(
            preferencial,
            sexo,
            status,
            idade,
            nome
        )
        if status_response != 200:
            return Response(
                text_response,
                status_response
            )
        paciente.preferencial = preferencial
        paciente.sexo = sexo
        paciente.status = status
        paciente.idade = idade
        paciente.nome = nome
        paciente.atualizado_em = timezone.now()
        paciente.save()
        response_serializer = PacienteSerializer(paciente)
        return Response(
            response_serializer.data,
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
    def delete(self, request):
        param_id = request.query_params.get('id')
        if param_id is None:
            return Response(
                "Error: param id is invalid.",
                status=400
            )
        try:
            try:
                paciente = Paciente.objects.get(id=int(param_id))
            except:
                return Response(
                    "Error: Item not found.",
                    status=400
                )
            paciente.delete()
            return Response(
                "Item removed from database.",
                status=204
            )
        except:
            return Response(
                "Error: unspecified error.",
                status=500
            )
