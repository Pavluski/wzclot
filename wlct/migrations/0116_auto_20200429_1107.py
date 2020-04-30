# Generated by Django 2.2.4 on 2020-04-29 18:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0115_auto_20200428_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentgame',
            name='game_finished_time',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='tournamentgame',
            name='game_log_sent',
            field=models.BooleanField(blank=True, db_index=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='tournamentgame',
            name='game_start_time',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]