# Generated by Django 2.1.4 on 2020-03-24 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0084_tournamentgame_players'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentgame',
            name='players',
            field=models.CharField(max_length=255, null=True),
        ),
    ]