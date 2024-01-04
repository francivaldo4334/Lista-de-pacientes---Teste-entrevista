import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Paciente(models.Model):
    class Meta:
        db_table = 'paciente'
        verbose_name = 'paciente'
        verbose_name_plural: str = "pacientes"
    class Sexo(models.TextChoices):
        H = 'H', 'Homen'
        M = 'M', 'Mulher'
    class StatusAndamento(models.TextChoices):
        AGUARDANDO = 'Aguardando', 'Paciente aguardando atendimento.',
        CANCELADO = 'Cancelado', 'Consulta cancelada pelo paciente ou pelo sistema.',
        EM_ATENDIMENTO = 'EmAtendimento', 'Paciente em atendimento médico.',
        CONCLUIDO = 'Concluído', 'Consulta concluída.'
    class CondicaoPreferencial(models.TextChoices):
        NAO_PREFERENCIAL = 'NaoPreferencial', 'pessoa sem condicao preferencial.',
        DEFICIENTE = 'Deficiente', 'pessoa com deficiência física.',
        PESSOA_IDOSA = 'PessoaIdosa', 'idosos com idade igual ou superior a sessenta e cinco anos.',
        GESTANTE = 'Gestante', 'mães em periodo de gestação.'
        LACTANTE = 'Lactante', 'mães com filho(a) recém nascido.',
        CRIANCA_DE_COLO = 'CriancaDeColo','pessoas acompanhadas por crianças de colo.',

    preferencial = models.CharField(
        max_length = 15,
        choices = CondicaoPreferencial.choices,
        default = CondicaoPreferencial.NAO_PREFERENCIAL,
        verbose_name = 'Condição preferencial',
        help_text = 'Condição preferencial de atendimento.'
    )
    sexo = models.CharField(
        max_length = 1,
        choices = Sexo.choices,
        default = Sexo.H,
        verbose_name = 'genero sexual',
        help_text = 'genero sexual'
    )
    status = models.CharField(
        max_length = 15,
        choices = StatusAndamento.choices,
        default = StatusAndamento.AGUARDANDO,
        verbose_name = 'status do atendimento.',
        help_text = 'gerencia status de atendimento.'
    )
    idade = models.IntegerField(
        verbose_name = 'Idade do paciente',
        help_text = 'Idade do paciente'
    )
    criado_em = models.DateField(
        default = timezone.now,
        verbose_name = 'data de entrada do paciente.',
        help_text = 'data de criação/inicio do paciente no sistema.'
    )
    nome = models.TextField(
        default = '',
        verbose_name = 'nome do paciente.',
        help_text = 'nome do paciente.'
    )
