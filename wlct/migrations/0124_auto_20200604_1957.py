# Generated by Django 2.2.4 on 2020-06-05 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0123_auto_20200604_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentgame',
            name='templateid',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
