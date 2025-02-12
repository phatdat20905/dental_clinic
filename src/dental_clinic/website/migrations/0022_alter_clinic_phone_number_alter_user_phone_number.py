# Generated by Django 5.0.10 on 2024-12-31 05:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be 10 digits only.', regex='^\\d{10}')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be 10 digits only.', regex='^\\d{10}')]),
        ),
    ]
