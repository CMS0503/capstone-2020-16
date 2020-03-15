# Generated by Django 2.2.10 on 2020-03-15 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onepanman_api', '0009_problem_rule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False, verbose_name='ID')),
                ('ruleClass', models.CharField(db_column='RULECLASS', default='착수', max_length=50, verbose_name='CLASS')),
                ('ruleType', models.CharField(db_column='TYPE', default='이동', max_length=50, verbose_name='TYPE')),
                ('number', models.IntegerField(db_column='OBJECTNUM', default=1, verbose_name='OBJECT NUMBER')),
                ('description', models.CharField(db_column='DESCRIPTION', default='규칙 설명', max_length=200, verbose_name='DESCRIPTION')),
            ],
            options={
                'verbose_name': '규칙',
                'verbose_name_plural': '규칙 정보',
                'db_table': 'RULE',
                'ordering': ['id', 'ruleClass', 'ruleType', 'number'],
            },
        ),
        migrations.AddField(
            model_name='game',
            name='error_msg',
            field=models.TextField(db_column='ERROR_MSG', default='no error', verbose_name='에러메세지'),
        ),
        migrations.AddField(
            model_name='game',
            name='result',
            field=models.CharField(db_column='RESULT', default='playing', max_length=50, verbose_name='결과'),
        ),
        migrations.AddField(
            model_name='userinformationinproblem',
            name='available_game',
            field=models.BooleanField(db_column='AVAILABLE_GAME', default='True', verbose_name='게임 가능 유저'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='rule',
            field=models.TextField(db_column='RULE', default='{ "placement" : , "action" : , "ending": ,}', verbose_name='문제 규칙'),
        ),
    ]
