# Generated by Django 5.0.4 on 2024-07-02 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_servicios', '0011_servicio_fechafin_servicio_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('costo_publicacion', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('duracion_publicacion_dias', models.IntegerField(default=30)),
            ],
        ),
    ]
