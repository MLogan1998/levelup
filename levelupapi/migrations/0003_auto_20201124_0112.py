# Generated by Django 3.1.3 on 2020-11-24 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_auto_20201124_0018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='datetime',
            new_name='date',
        ),
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]
