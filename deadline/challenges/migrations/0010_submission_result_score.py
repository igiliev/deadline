# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0009_testcase_error_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='result_score',
            field=models.IntegerField(default=0, verbose_name='The points from the challenge'),
        ),
    ]
