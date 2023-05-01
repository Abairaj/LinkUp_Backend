# Generated by Django 4.1.8 on 2023-04-30 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='facebook_uid',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Transgenders', 'Transgenders'), ('Female', 'Female')], max_length=30),
        ),
    ]
