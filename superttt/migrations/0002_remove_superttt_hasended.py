# Generated by Django 5.0.3 on 2024-04-20 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superttt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='superttt',
            name='hasEnded',
        ),
    ]
