# Generated by Django 5.0.3 on 2024-04-21 06:41

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superttt', '0008_alter_superttt_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superttt',
            name='board',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(0, 'None'), (1, 'Circle'), (2, 'Cross')]), size=10), size=9),
        ),
    ]
