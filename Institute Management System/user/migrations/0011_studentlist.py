# Generated by Django 3.2.9 on 2022-02-21 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_user_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(max_length=6, unique=True)),
                ('registration', models.CharField(max_length=15)),
            ],
        ),
    ]
