from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Exame
from .serializers import ExameSerializer

# Create your views here.
class ExameList(APIView):
    def get(self,request):
        exaem_list = Exame.objects.all()
        serializer_exame_list = ExameSerializer(exaem_list,many=True)
        return Response(
            serializer_exame_list.data,
            status=200
        )