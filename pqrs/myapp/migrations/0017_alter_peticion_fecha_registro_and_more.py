# Generated by Django 5.0 on 2024-01-28 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_peticion_fecha_registro_queja_fecha_registro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peticion',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='queja',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reclamo',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sugerencia',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
