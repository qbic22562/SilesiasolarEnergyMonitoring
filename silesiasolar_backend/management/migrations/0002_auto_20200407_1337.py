# Generated by Django 3.0.5 on 2020-04-07 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meter',
            old_name='meter_id',
            new_name='meter_type',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='meter_id',
            new_name='meter_type',
        ),
    ]