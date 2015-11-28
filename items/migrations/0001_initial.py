# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bids',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bidder', models.CharField(max_length=200)),
                ('bid_amount', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('name', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('date_added', models.DateTimeField(verbose_name=b'date added')),
                ('image', models.ImageField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bids',
            name='item',
            field=models.ForeignKey(to='items.Items'),
            preserve_default=True,
        ),
    ]
