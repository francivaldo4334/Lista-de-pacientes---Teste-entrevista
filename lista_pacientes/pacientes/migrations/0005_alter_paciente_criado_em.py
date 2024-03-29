# Generated by Django 5.0.1 on 2024-01-04 19:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0004_alter_paciente_preferencial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='criado_em',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='data de criação/inicio do paciente no sistema.', verbose_name='data de entrada do paciente.'),
        ),
    ]
