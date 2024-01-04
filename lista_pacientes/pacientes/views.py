from .models import Paciente
from .serializers import PacienteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
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
            pacientes = pacientes.exclude(preferencial="NaoPreferencial")
        serializerResponse = PacienteSerializer(pacientes,many=True)
        return Response(serializerResponse.data)
    @swagger_auto_schema(
        request_body= PacienteSerializer
    )
    def post(self,request):
        ...