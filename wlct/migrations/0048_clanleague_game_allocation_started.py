# Generated by Django 2.1.4 on 2019-12-31 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0047_clanleaguetournament_clan_league_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='clanleague',
            name='game_allocation_started',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
