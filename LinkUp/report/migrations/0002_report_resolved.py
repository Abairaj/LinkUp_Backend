# Generated by Django 4.1.8 on 2023-06-09 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
