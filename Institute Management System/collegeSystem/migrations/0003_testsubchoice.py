# Generated by Django 3.2.9 on 2022-01-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeSystem', '0002_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSubChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.CharField(choices=[['Business Organization and Communications(65842)', 'Business Organization and Communications(65842)'], ['Data Structure and Algorithms(65441)', 'Data Structure and Algorithms(65441)'], ['Object Oriented Programming(65443)', 'Object Oriented Programming(65443)']], max_length=50)),
            ],
        ),
    ]
