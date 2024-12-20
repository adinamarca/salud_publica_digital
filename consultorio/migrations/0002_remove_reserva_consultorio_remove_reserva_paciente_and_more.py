# Generated by Django 5.1 on 2024-12-13 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultorio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='consultorio',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='paciente',
        ),
        migrations.AddField(
            model_name='profesional',
            name='rut_profesional',
            field=models.CharField(max_length=12, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='profesional',
            name='titulo_profesional',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.EmailField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Atencion',
        ),
        migrations.DeleteModel(
            name='Consultorio',
        ),
        migrations.DeleteModel(
            name='Reserva',
        ),
    ]
