# Generated by Django 3.2.9 on 2022-01-06 19:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('semesterSystem', '0004_alter_semestersystem_last_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semestersystem',
            name='last_payment',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last payment'),
        ),
    ]