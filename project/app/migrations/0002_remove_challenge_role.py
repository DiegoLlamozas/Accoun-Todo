# Generated by Django 4.2.4 on 2023-08-10 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='role',
        ),
    ]
