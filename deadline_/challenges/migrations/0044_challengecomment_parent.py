# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-14 19:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0043_submissioncomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengecomment',
            name='parent',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='challenges.ChallengeComment'),
        ),
    ]