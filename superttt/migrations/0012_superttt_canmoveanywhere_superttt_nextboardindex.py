# Generated by Django 5.0.3 on 2024-04-21 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superttt', '0011_remove_supertttplayer_haswon_alter_superttt_board_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='superttt',
            name='canMoveAnywhere',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='superttt',
            name='nextBoardIndex',
            field=models.SmallIntegerField(default=0),
        ),
    ]