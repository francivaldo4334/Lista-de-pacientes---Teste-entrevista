from rest_framework.views import APIView
from rest_framework.response import Response
from agendamento.models import Agendamento
from .models import Exame
from .serializers import ExameSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class ExameList(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'agendamento_id',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self,request):
        param_agendamento_id = request.query_params.get('agendamento_id')
        if param_agendamento_id is not None:
            agendamento = Agendamento.objects.get(id=int(param_agendamento_id))
            exaem_list = Exame.objects.filter(agendamento=agendamento)
        else:
            exaem_list = Exame.objects.all()
        serializer_exame_list = ExameSerializer(exaem_list,many=True)
        return Response(
            serializer_exame_list.data,
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
            exame = Exame.objects.get(id=int(param_id))
        except:
            return Response(
                "Error: 'exame' not found.",
                status=404
            )
        exame.delete()
        return Response(
            "Item removed from database.",
            status=204
        )
