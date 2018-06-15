# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-06 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='popular_book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('cnt', models.IntegerField(db_column='num_of_borrow')),
            ],
            options={
                'db_table': 'p_book',
                'managed': False,
            },
        ),
    ]
