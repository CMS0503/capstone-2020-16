# Generated by Django 2.2.10 on 2020-04-18 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onepanman_api', '0021_userinformationinproblem_playing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='available_game',
            field=models.BooleanField(db_column='AVAILABLE_GAME', default=True, verbose_name='게임가능코드'),
        ),
    ]
