# Generated by Django 3.2.9 on 2022-01-25 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeSystem', '0008_auto_20220125_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='storegrade',
            name='subject_credit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subjects',
            name='subject_credit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
