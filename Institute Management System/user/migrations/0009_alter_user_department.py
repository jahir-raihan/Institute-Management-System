# Generated by Django 3.2.9 on 2022-02-10 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_user_is_deafen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(choices=[('Computer Science and Technology', 'Computer Science and Technology'), ('Architecture and Interior Design Technology', 'Architecture and Interior Design Technology'), ('Civil Technology', 'Civil Technology'), ('TextTile Technology', 'TextTile Technology'), ('Electrical Engineering Technology', 'Electrical Engineering Technology')], max_length=100, null=True, verbose_name='Department'),
        ),
    ]