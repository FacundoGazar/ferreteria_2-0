# Generated by Django 5.0.4 on 2024-07-03 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_servicios', '0012_configuracionservicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado'), ('publicado', 'Publicado'), ('eliminado', 'Eliminado')], default='pendiente', max_length=10),
        ),
    ]
