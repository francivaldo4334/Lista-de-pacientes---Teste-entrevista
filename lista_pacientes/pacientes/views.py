from .models import Paciente
from .serializers import PacienteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.utils import timezone
import json
# Create your views here.
class PacienteList(APIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Parametro de pesquisa por estado de andamento do paciente.",
                type=openapi.TYPE_STRING,
                enum=['Aguardando','Cancelado','EmAtendimento','Concluído']
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
                enum=['True','False']
            )
        ]
    )
    def get(self,request):
        status = request.query_params.get('status')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        preferencial = request.query_params.get('preferencial')
        if start_date and end_date:
            pacientes = Paciente.objects.filter(criado_em__range=[start_date,end_date])
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
        if preferencial == 'True':
            pacientes = pacientes.exclude(preferencial=Paciente.CondicaoPreferencial.NAO_PREFERENCIAL[0])
        order_list = sorted(
            pacientes,
            key=lambda paciente:(
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
        serializer_response = PacienteSerializer(order_list,many=True)
        return Response(serializer_response.data)
    @swagger_auto_schema(
        request_body= PacienteSerializer
    )
    def post(self,request):
        body = json.loads(request.body)
        preferencial = body.get('preferencial')
        sexo = body.get('sexo')
        status = body.get('status')
        idade = int(body.get('idade'))
        nome = body.get('nome')
        criado_em = timezone.now()

        if idade > 65:
            preferencial = Paciente.CondicaoPreferencial.PESSOA_IDOSA.value
        if not preferencial in Paciente.CondicaoPreferencial.values:
            return Response(
                f"Error: value 'preferencial' is invalid. valid params {Paciente.CondicaoPreferencial.values}",
                status=400
            )
        if not sexo in Paciente.Sexo.values:
            return Response(
                f"Error: value 'sexo' is invalid. valid params {Paciente.Sexo.values}",
                status=400
            )
        if not status in Paciente.StatusAndamento.values:
            return Response(
                f"Error: value 'status' is invalid. valid params {Paciente.StatusAndamento.values}",
                status=400
            )
        if idade <= 0 or idade >= 500:
            return Response(
                "Error: value 'idade' is invalid."
            )
        new_paciente = Paciente(
            preferencial =preferencial,
            sexo =sexo,
            status =status,
            idade =idade,
            nome =nome,
            criado_em =criado_em,
        )
        new_paciente.save()
        return Response()