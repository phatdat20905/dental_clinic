# Generated by Django 5.0.10 on 2024-12-29 03:37

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_alter_medicalrecord_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', tinymce.models.HTMLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='website/img/service')),
            ],
        ),
        migrations.AlterField(
            model_name='clinic',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ServiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100)),
                ('unit', models.CharField(blank=True, max_length=20, null=True)),
                ('price', models.CharField(blank=True, max_length=30, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.category')),
            ],
        ),
    ]