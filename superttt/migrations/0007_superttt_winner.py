# Generated by Django 5.0.3 on 2024-04-20 07:28

import superttt.types
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superttt', '0006_alter_superttt_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='superttt',
            name='winner',
            field=models.IntegerField(default=0, verbose_name=superttt.types.SuperTTTPlayerSymbol),
        ),
    ]
