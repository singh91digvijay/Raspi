# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hosts', models.IntegerField(default=0)),
            ],
        ),
    ]
