# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 17:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0010_submission_result_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='pending',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
