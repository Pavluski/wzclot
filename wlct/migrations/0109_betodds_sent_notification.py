# Generated by Django 2.1.4 on 2020-04-26 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0108_auto_20200426_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='betodds',
            name='sent_notification',
            field=models.BooleanField(default=False),
        ),
    ]
