# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-15 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SICS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.IntegerField(),
        ),
    ]
