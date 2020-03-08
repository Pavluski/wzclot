# Generated by Django 2.1.4 on 2020-03-05 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0075_logger_bot_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordChannelTournamentLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channelid', models.BigIntegerField(blank=True, db_index=True, default=0, null=True)),
                ('discord_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wlct.DiscordUser')),
                ('tournament', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wlct.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='tournamentgame',
            name='game_log_sent',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]