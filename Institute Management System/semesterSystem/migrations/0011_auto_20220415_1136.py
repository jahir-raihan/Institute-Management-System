# Generated by Django 3.2.9 on 2022-04-15 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semesterSystem', '0010_auto_20220129_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='midtermfee',
            name='department',
            field=models.CharField(default='Computer Science and Technology(85)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='midtermfee',
            name='session',
            field=models.CharField(default='2019-2020', max_length=50),
            preserve_default=False,
        ),
    ]
