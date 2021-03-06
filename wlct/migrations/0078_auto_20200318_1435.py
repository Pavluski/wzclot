# Generated by Django 2.1.4 on 2020-03-18 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wlct', '0077_auto_20200315_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionalRelegationDivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='promotionalrelegationleagueseason',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='promotionalrelegationleagueseason',
            name='season_number',
        ),
        migrations.AddField(
            model_name='promotionalrelegationleagueseason',
            name='season_template',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pr_season_template', to='wlct.ClanLeagueTemplate'),
        ),
        migrations.AddField(
            model_name='promotionalrelegationdivision',
            name='season',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wlct.PromotionalRelegationLeagueSeason'),
        ),
    ]
