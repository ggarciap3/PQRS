# Generated by Django 5.0 on 2024-01-06 14:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_queja'),
    ]

    operations = [
        migrations.AddField(
            model_name='queja',
            name='Qfecha',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
