# Generated by Django 5.0.1 on 2024-01-04 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0003_paciente_nome_alter_paciente_preferencial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='preferencial',
            field=models.CharField(choices=[('NaoPreferencial', 'pessoa sem condicao preferencial.'), ('Deficiente', 'pessoa com deficiência física.'), ('PessoaIdosa', 'idosos com idade igual ou superior a sessenta e cinco anos.'), ('Gestante', 'mães em periodo de gestação.'), ('Lactante', 'mães com filho(a) recém nascido.'), ('CriancaDeColo', 'pessoas acompanhadas por crianças de colo.')], default='NaoPreferencial', help_text='Condição preferencial de atendimento.', max_length=15, verbose_name='Condição preferencial'),
        ),
    ]
