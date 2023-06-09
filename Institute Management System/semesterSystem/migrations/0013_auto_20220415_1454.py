# Generated by Django 3.2.9 on 2022-04-15 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semesterSystem', '0012_auto_20220415_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='semestersysteminfo',
            name='department',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='semestersysteminfo',
            name='semester',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semestersysteminfo',
            name='session',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='semestersysteminfo',
            name='amount_to_pay',
            field=models.IntegerField(default=0),
        ),
    ]
