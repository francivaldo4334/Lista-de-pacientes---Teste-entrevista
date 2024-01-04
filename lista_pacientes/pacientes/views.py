from .models import Paciente
from .serializers import PacienteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
            )
        ]
    )
    def get(self,request):
        status = request.query_params.get('status')
        if status is not None:
            pacientes = Paciente.objects.filter(status=status)
        else:
            pacientes = Paciente.objects.all()
        serializerResponse = PacienteSerializer(pacientes,many=True)
        return Response(serializerResponse.data)
    @swagger_auto_schema(
        request_body= PacienteSerializer
    )
    def post(self,request):
        ...