# Generated by Django 5.0.4 on 2024-06-19 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiar_producto', '0007_alter_intercambio_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercambio',
            name='venta_realizada',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]