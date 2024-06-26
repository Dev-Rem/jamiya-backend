# Generated by Django 4.0.1 on 2023-05-24 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('station', models.CharField(blank=True, choices=[('FRONTDESK1', 'FRONTDESK1'), ('FRONTDESK2', 'FRONTDESK2'), ('FRONTDESK3', 'FRONTDESK3'), ('FRONTDESK4', 'FRONTDESK4'), ('BANK', 'BANK'), ('DRIVER', 'DRIVER'), ('ONLINE', 'ONLINE'), ('MARKETING', 'MARKETING'), ('HEAD OF OPERATIONS', 'HEAD OF OPERATIONS')], max_length=50, null=True, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Date Joined')),
                ('last_login', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date Last log in')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
