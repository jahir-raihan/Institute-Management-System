# Generated by Django 3.2.9 on 2022-01-28 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_transaction_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(default='cash_in', max_length=50),
            preserve_default=False,
        ),
    ]
