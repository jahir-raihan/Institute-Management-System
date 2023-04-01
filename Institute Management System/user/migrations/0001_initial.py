# Generated by Django 3.2.9 on 2021-12-31 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Email Address')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='Phone Number')),
                ('roll', models.CharField(max_length=6, null=True, unique=True, verbose_name='Roll Number')),
                ('registration', models.CharField(max_length=15, null=True, unique=True, verbose_name='Registration Number')),
                ('semester', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], null=True, verbose_name='Semester')),
                ('department', models.CharField(choices=[('CST', 'CST'), ('AIDT', 'AIDT'), ('CT', 'CT'), ('EET', 'EET')], max_length=20, null=True, verbose_name='Department')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=20, null=True, verbose_name='Gender')),
                ('religion', models.CharField(choices=[('Islam', 'Islam'), ('Hindu', 'Hindu'), ('Buddhist', 'Buddhist'), ('Christan', 'Christan')], max_length=20, null=True, verbose_name='Religion')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('in_hostel', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]