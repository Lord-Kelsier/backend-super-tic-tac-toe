# Generated by Django 5.0.3 on 2024-04-20 07:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superttt', '0007_superttt_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superttt',
            name='board',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), size=10), size=9),
        ),
    ]
