# Generated by Django 5.0.7 on 2024-07-12 10:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='phone',
            field=models.CharField(help_text='Enter a 10-digit contact number', max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Contact number must be exactly 10 digits.', regex='^\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='emergency',
            name='contact_number',
            field=models.CharField(help_text='Enter a 10-digit contact number', max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Contact number must be exactly 10 digits.', regex='^\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(help_text='Enter a 10-digit contact number', max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Contact number must be exactly 10 digits.', regex='^\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='staff',
            name='phone',
            field=models.CharField(help_text='Enter a 10-digit contact number', max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Contact number must be exactly 10 digits.', regex='^\\d{10}$')]),
        ),
    ]
