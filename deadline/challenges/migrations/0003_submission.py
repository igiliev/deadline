# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 15:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenges', '0002_challenge_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.Challenge')),
            ],
        ),
    ]
