# Generated by Django 2.1.4 on 2020-02-17 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0070_auto_20200217_1219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discorduser',
            old_name='discord_id',
            new_name='memberid',
        ),
    ]
