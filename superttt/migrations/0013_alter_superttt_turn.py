# Generated by Django 5.0.3 on 2024-05-05 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superttt', '0012_superttt_canmoveanywhere_superttt_nextboardindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superttt',
            name='turn',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'Circle'), (2, 'Cross'), (3, 'Nullplayer')]),
        ),
    ]