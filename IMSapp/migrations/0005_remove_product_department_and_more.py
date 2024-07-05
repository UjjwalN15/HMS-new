# Generated by Django 5.0.6 on 2024-07-04 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IMSapp', '0004_remove_department_floor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='department',
        ),
        migrations.RemoveField(
            model_name='purchase_products',
            name='department',
        ),
        migrations.AddField(
            model_name='product',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='IMSapp.department'),
        ),
        migrations.AddField(
            model_name='purchase_products',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='IMSapp.department'),
        ),
    ]
