# Generated by Django 2.0 on 2019-06-09 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrydetails',
            name='dc',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='countrydetails',
            name='detail_type',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='countrydetails',
            name='ion',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='countrydetails',
            name='lat',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='countrydetails',
            name='postcode',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='countrydetails',
            name='state',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='countrydetails',
            name='suburb',
            field=models.CharField(default='', max_length=100),
        ),
    ]
