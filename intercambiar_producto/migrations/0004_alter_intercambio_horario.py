# Generated by Django 5.0.4 on 2024-05-24 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiar_producto', '0003_intercambio_dia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intercambio',
            name='horario',
            field=models.CharField(choices=[(9, '9:00 AM'), (10, '10:00 AM'), (11, '11:00 AM'), (12, '12:00 PM'), (13, '1:00 PM'), (14, '2:00 PM'), (15, '3:00 PM'), (16, '4:00 PM'), (17, '5:00 PM')], default=' ', max_length=5),
        ),
    ]
