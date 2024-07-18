# Generated by Django 5.0.7 on 2024-07-17 09:32

import base.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_patient_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='availability',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='schedule',
            field=models.DateField(validators=[base.validators.validate_schedule_date]),
        ),
    ]
