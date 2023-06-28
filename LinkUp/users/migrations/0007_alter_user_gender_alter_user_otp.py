# Generated by Django 4.1.8 on 2023-06-28 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_verified_user_otp_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('Transgenders', 'Transgenders'), ('Male', 'Male'), ('Female', 'Female')], max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
