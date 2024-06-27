# Generated by Django 5.0.6 on 2024-06-26 09:56

import base.models
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor_Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Emergency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unnamed Emergency', max_length=300)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('contact_number', models.CharField(max_length=300)),
                ('date', models.DateTimeField(default=base.models.nepal_time_default)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('solved', 'Solved')], default='pending', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], max_length=100)),
                ('address', models.CharField(max_length=300)),
                ('phone', models.CharField(max_length=300, unique=True)),
                ('medical_history', models.TextField(blank=True)),
                ('schedule', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=300)),
                ('password', models.CharField(max_length=300)),
                ('groups', models.ManyToManyField(to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], max_length=100)),
                ('address', models.CharField(max_length=300)),
                ('phone', models.CharField(max_length=300, unique=True)),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.doctor_speciality')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('diagnosis', models.TextField()),
                ('treatments', models.TextField()),
                ('prescriptions', models.TextField(blank=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='medical_record/pdf/')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('canceled', 'Canceled'), ('completed', 'Completed')], default='scheduled', max_length=100)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], max_length=100)),
                ('address', models.CharField(max_length=300)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]
