# Generated by Django 4.0 on 2021-12-12 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='body',
            field=models.TextField(max_length=400, null=True, verbose_name='詳細/内容'),
        ),
    ]
