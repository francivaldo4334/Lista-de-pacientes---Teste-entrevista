from django.db import models
from django.utils import timezone
from pacientes.models import Paciente

# Create your models here.
class Agendamento(models.Model):
    agendado_para = models.DateTimeField(
        verbose_name='data marcada para o atendimento.',
        help_text='data marcada para o atendimento.'
    )
    criado_em = models.DateTimeField(
        default=timezone.now(),
        verbose_name='data de criação.',
        help_text='data de criação do registro de agendamento.'
    )
    atualizado_em = models.DateTimeField(
        default=timezone.now(),
        verbose_name='data de atualização.',
        help_text='data da ultima atualizacao do registro de agendamento.'
    )
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)