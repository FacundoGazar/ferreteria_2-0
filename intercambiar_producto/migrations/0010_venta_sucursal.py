# Generated by Django 5.0.4 on 2024-07-02 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_sucursales', '0003_alter_perfilempleado_sucursal'),
        ('intercambiar_producto', '0009_productoventa_venta_productoventa_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='sucursal',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gestion_de_sucursales.sucursal'),
            preserve_default=False,
        ),
    ]
