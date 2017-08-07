# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
                ('password', models.CharField(max_length=256)),
                ('confirm_email', models.CharField(blank=True, max_length=100)),
                ('score', models.IntegerField()),
                ('auth_token', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
