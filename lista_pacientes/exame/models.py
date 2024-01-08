from django.db import models
from agendamento.models import Agendamento
from django.utils import timezone


# Create your models here.
class Exame(models.Model):
    class TipoExame(models.TextChoices):
        RAIO_X = 'RaioX', "Exame do tipo raio_x.",
        TOMOGRAFIA = 'Tomografia', 'Exame do tipo tomografia.'
    tipo = models.CharField(
        max_length=10,
        choices=TipoExame.choices,
        verbose_name='Tipo de exame.',
        help_text='Expecificação do tipo de exame.'
    )
    criado_em = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de criação.',
        help_text='Data de criação do registro de exame.'
    )
    agendamento = models.ForeignKey(Agendamento,on_delete=models.CASCADE)