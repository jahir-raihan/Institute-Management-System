# Generated by Django 3.2.9 on 2022-02-04 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeSystem', '0011_alter_result_grade_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='storegrade',
            name='subject_mark',
            field=models.CharField(default=0, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storegrade',
            name='subject_name',
            field=models.CharField(default='hello', max_length=100),
            preserve_default=False,
        ),
    ]
