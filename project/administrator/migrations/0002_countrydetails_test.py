# Generated by Django 2.0 on 2020-01-05 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrydetails',
            name='test',
            field=models.CharField(default='', max_length=100),
        ),
    ]