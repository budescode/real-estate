# Generated by Django 2.0 on 2019-05-20 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20190520_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sellercategory',
            old_name='category',
            new_name='select_category',
        ),
    ]
