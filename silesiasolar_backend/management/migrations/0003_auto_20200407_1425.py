# Generated by Django 3.0.5 on 2020-04-07 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20200407_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meter',
            name='host',
            field=models.CharField(max_length=32),
        ),
    ]