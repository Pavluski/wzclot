# Generated by Django 2.1.4 on 2020-04-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0103_roundrobinrandomteams'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentplayer',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tournamentplayer',
            name='rating',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='tournamentplayer',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
