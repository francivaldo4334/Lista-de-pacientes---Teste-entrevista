from rest_framework.views import APIView
from .models import Exame

# Create your views here.
class ExameList(APIView):
    def get(self,request):
        pass