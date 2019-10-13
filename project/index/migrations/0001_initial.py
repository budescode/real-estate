# Generated by Django 2.0 on 2019-09-28 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ninety',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id_user', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('unit', models.TextField()),
                ('street_number', models.TextField()),
                ('street_name', models.TextField()),
                ('suburb', models.TextField()),
                ('postcode', models.TextField()),
                ('state', models.TextField()),
                ('land_size', models.CharField(max_length=100)),
                ('longitude', models.CharField(blank=True, max_length=30)),
                ('latitude', models.CharField(blank=True, max_length=30)),
                ('Property_type', models.CharField(choices=[('House', 'House'), ('Apartment & Unit', 'Apartment & Unit'), ('Townhouse', 'Townhouse'), ('Villa', 'Villa'), ('Land', 'Land'), ('Acreage', 'Acreage'), ('Rural', 'Rural'), ('Block Of Units', 'Block Of Units'), ('Retirement Living', 'Retirement Living')], default='House', max_length=100)),
                ('description', models.TextField()),
                ('Price', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('plan', models.ImageField(upload_to='')),
                ('Bedrooms', models.PositiveIntegerField(default=1)),
                ('Bathrooms', models.PositiveIntegerField(default=1)),
                ('Car_spaces', models.PositiveIntegerField(default=1)),
                ('image1', models.ImageField(blank=True, default='', upload_to='')),
                ('image2', models.ImageField(blank=True, default='', upload_to='')),
                ('image3', models.ImageField(blank=True, default='', upload_to='')),
                ('image4', models.ImageField(blank=True, default='', upload_to='')),
                ('image5', models.ImageField(blank=True, default='', upload_to='')),
                ('image6', models.ImageField(blank=True, default='', upload_to='')),
                ('image7', models.ImageField(blank=True, default='', upload_to='')),
                ('image8', models.ImageField(blank=True, default='', upload_to='')),
                ('image9', models.ImageField(blank=True, default='', upload_to='')),
                ('image10', models.ImageField(blank=True, default='', upload_to='')),
                ('image11', models.ImageField(blank=True, default='', upload_to='')),
                ('image12', models.ImageField(blank=True, default='', upload_to='')),
                ('image13', models.ImageField(blank=True, default='', upload_to='')),
                ('image14', models.ImageField(blank=True, default='', upload_to='')),
                ('image15', models.ImageField(blank=True, default='', upload_to='')),
                ('image16', models.ImageField(blank=True, default='', upload_to='')),
                ('image17', models.ImageField(blank=True, default='', upload_to='')),
                ('image18', models.ImageField(blank=True, default='', upload_to='')),
                ('new_or_established', models.CharField(choices=[('New', 'New'), ('Established', 'Established')], default='New', max_length=20)),
                ('Swimming_pool', models.BooleanField(default=False)),
                ('Garage', models.BooleanField(default=False)),
                ('Balcony', models.BooleanField(default=False)),
                ('Outdoor_area', models.BooleanField(default=False)),
                ('Undercover_parking', models.BooleanField(default=False)),
                ('Shed', models.BooleanField(default=False)),
                ('Fully_fenced', models.BooleanField(default=False)),
                ('Outdoor_spa', models.BooleanField(default=False)),
                ('Tennis_court', models.BooleanField(default=False)),
                ('Ensuite', models.BooleanField(default=False)),
                ('DishWasher', models.BooleanField(default=False)),
                ('Study', models.BooleanField(default=False)),
                ('Built_in_robes', models.BooleanField(default=False)),
                ('Alarm_system', models.BooleanField(default=False)),
                ('Broadband', models.BooleanField(default=False)),
                ('Floorboards', models.BooleanField(default=False)),
                ('Gym', models.BooleanField(default=False)),
                ('Rumpus_room', models.BooleanField(default=False)),
                ('Workshop', models.BooleanField(default=False)),
                ('Air_conditioning', models.BooleanField(default=False)),
                ('Solar_panels', models.BooleanField(default=False)),
                ('Heating', models.BooleanField(default=False)),
                ('High_energy_efficiency', models.BooleanField(default=False)),
                ('Water_tank', models.BooleanField(default=False)),
                ('Solar_hot_water', models.BooleanField(default=False)),
                ('saved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userposts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PosterRent',
            fields=[
                ('id_user', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('unit', models.TextField()),
                ('street_number', models.TextField()),
                ('street_name', models.TextField()),
                ('suburb', models.TextField()),
                ('postcode', models.TextField()),
                ('state', models.TextField()),
                ('land_size', models.CharField(max_length=100)),
                ('Property_type', models.CharField(choices=[('House', 'House'), ('Apartment & Unit', 'Apartment & Unit'), ('Townhouse', 'Townhouse'), ('Villa', 'Villa'), ('Land', 'Land'), ('Acreage', 'Acreage'), ('Rural', 'Rural'), ('Block Of Units', 'Block Of Units'), ('Retirement Living', 'Retirement Living')], default='House', max_length=100)),
                ('description', models.TextField()),
                ('Price', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('plan', models.ImageField(upload_to='')),
                ('Bedrooms', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20')], default='1', max_length=20)),
                ('Bathrooms', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20')], default='1', max_length=10)),
                ('Car_spaces', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], default='1', max_length=10)),
                ('image1', models.ImageField(blank=True, default='', upload_to='')),
                ('image2', models.ImageField(blank=True, default='', upload_to='')),
                ('image3', models.ImageField(blank=True, default='', upload_to='')),
                ('image4', models.ImageField(blank=True, default='', upload_to='')),
                ('image5', models.ImageField(blank=True, default='', upload_to='')),
                ('image6', models.ImageField(blank=True, default='', upload_to='')),
                ('image7', models.ImageField(blank=True, default='', upload_to='')),
                ('image8', models.ImageField(blank=True, default='', upload_to='')),
                ('image9', models.ImageField(blank=True, default='', upload_to='')),
                ('image10', models.ImageField(blank=True, default='', upload_to='')),
                ('image11', models.ImageField(blank=True, default='', upload_to='')),
                ('image12', models.ImageField(blank=True, default='', upload_to='')),
                ('image13', models.ImageField(blank=True, default='', upload_to='')),
                ('image14', models.ImageField(blank=True, default='', upload_to='')),
                ('image15', models.ImageField(blank=True, default='', upload_to='')),
                ('image16', models.ImageField(blank=True, default='', upload_to='')),
                ('image17', models.ImageField(blank=True, default='', upload_to='')),
                ('image18', models.ImageField(blank=True, default='', upload_to='')),
                ('new_or_established', models.CharField(choices=[('New', 'New'), ('Established', 'Established')], default='New', max_length=20)),
                ('Swimming_pool', models.BooleanField(default=False)),
                ('Garage', models.BooleanField(default=False)),
                ('Balcony', models.BooleanField(default=False)),
                ('Outdoor_area', models.BooleanField(default=False)),
                ('Undercover_parking', models.BooleanField(default=False)),
                ('Shed', models.BooleanField(default=False)),
                ('Fully_fenced', models.BooleanField(default=False)),
                ('Outdoor_spa', models.BooleanField(default=False)),
                ('Tennis_court', models.BooleanField(default=False)),
                ('Ensuite', models.BooleanField(default=False)),
                ('DishWasher', models.BooleanField(default=False)),
                ('Study', models.BooleanField(default=False)),
                ('Built_in_robes', models.BooleanField(default=False)),
                ('Alarm_system', models.BooleanField(default=False)),
                ('Broadband', models.BooleanField(default=False)),
                ('Floorboards', models.BooleanField(default=False)),
                ('Gym', models.BooleanField(default=False)),
                ('Rumpus_room', models.BooleanField(default=False)),
                ('Workshop', models.BooleanField(default=False)),
                ('Air_conditioning', models.BooleanField(default=False)),
                ('Solar_panels', models.BooleanField(default=False)),
                ('Heating', models.BooleanField(default=False)),
                ('High_energy_efficiency', models.BooleanField(default=False)),
                ('Water_tank', models.BooleanField(default=False)),
                ('Solar_hot_water', models.BooleanField(default=False)),
                ('saved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentuserposts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SavedDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.TextField()),
                ('pricemin', models.TextField()),
                ('pricemax', models.TextField()),
                ('bedmin', models.TextField()),
                ('bedmax', models.TextField()),
                ('notification', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SavedDetail2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.TextField()),
                ('pricemin', models.TextField()),
                ('pricemax', models.TextField()),
                ('bedmin', models.TextField()),
                ('bedmax', models.TextField()),
                ('notification', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SavedHeaders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedHeaders1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ThreeSixty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='saveddetail2',
            name='header',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.SavedHeaders'),
        ),
        migrations.AddField(
            model_name='saveddetail2',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='saveddetail',
            name='header',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.SavedHeaders'),
        ),
        migrations.AddField(
            model_name='saveddetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
