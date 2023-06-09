# Generated by Django 3.2.9 on 2022-02-05 03:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('collegeSystem', '0014_auto_20220204_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadresult',
            name='ended',
            field=models.DateField(default=datetime.datetime(2022, 2, 5, 3, 8, 52, 788313, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadresult',
            name='exam_year',
            field=models.DateField(default=datetime.datetime(2022, 2, 5, 3, 9, 2, 60084, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadresult',
            name='started',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
