# Generated by Django 5.0.4 on 2024-05-23 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_productos', '0009_remove_producto_dias_producto_dias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
