# Generated by Django 5.0.7 on 2024-07-17 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IMSapp', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='IMSapp.department'),
        ),
    ]
