from django.db import models
from django.contrib.auth.models import User
import uuid





class PropertyType(models.Model):
	name = models.CharField(max_length=200, default='')
	def __str__(self):
		return self.name

class Price(models.Model):
	price = models.DecimalField(max_length=50, decimal_places=2, max_digits=15, default=0.00)
	def __str__(self):
		return str(self.price)









class Poster(models.Model):


	PropertyTypeChoice = (
		('House', 'House'),
		('Apartment & Unit', 'Apartment & Unit'),
		('Townhouse', 'Townhouse'),
		('Villa', 'Villa'),
		('Land', 'Land'),
		('Acreage', 'Acreage'),
		('Rural', 'Rural'),
		('Block Of Units', 'Block Of Units'),
		('Retirement Living', 'Retirement Living'),

		)
	bathrooms = (

		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
		('11', '11'),
		('12', '12'),
		('13', '13'),
		('14', '14'),
		('15', '15'),
		('16', '16'),
		('17', '17'),
		('18', '18'),
		('19', '19'),
		('20', '20'),

		)

	bedrooms = (

			('1', '1'),
			('2', '2'),
			('3', '3'),
			('4', '4'),
			('5', '5'),
			('6', '6'),
			('7', '7'),
			('8', '8'),
			('9', '9'),
			('10', '10'),
			('11', '11'),
			('12', '12'),
			('13', '13'),
			('14', '14'),
			('15', '15'),
			('16', '16'),
			('17', '17'),
			('18', '18'),
			('19', '19'),
			('20', '20'),

			)


	car_spaces = (

		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		)

	new_or_established = (
			('New', 'New'),
			('Established', 'Established')
		)
	id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	created = models.DateTimeField(auto_now_add=True)
	Updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'userposts')
	# days_left = models.PositiveIntegerField()

	# address = models.CharField(max_length=1000)
	unit = models.TextField()
	street_number = models.TextField()
	street_name = models.TextField()
	suburb = models.TextField()
	postcode = models.TextField()
	state = models.TextField()
	land_size = models.CharField(max_length=100)
	longitude = models.CharField(max_length=30, blank=True)
	latitude = models.CharField(max_length=30, blank=True)


	Property_type = models.CharField(max_length=100, choices=PropertyTypeChoice, default='House')
	description = models.TextField()
	Price = models.PositiveIntegerField()
	image = models.ImageField()
	plan = models.ImageField()
	Bedrooms = models.PositiveIntegerField(default=1)
	Bathrooms =models.PositiveIntegerField(default=1)
	Car_spaces = models.PositiveIntegerField(default=1)

	image1 = models.ImageField(default='', blank=True)
	image2 = models.ImageField(default='', blank=True)
	image3 = models.ImageField(default='', blank=True)
	image4 = models.ImageField(default='', blank=True)
	image5 = models.ImageField(default='', blank=True)
	image6 = models.ImageField(default='', blank=True)
	image7 = models.ImageField(default='', blank=True)
	image8 = models.ImageField(default='', blank=True)
	image9 = models.ImageField(default='', blank=True)
	image10 = models.ImageField(default='', blank=True)
	image11 = models.ImageField(default='', blank=True)
	image12 = models.ImageField(default='', blank=True)
	image13 = models.ImageField(default='', blank=True)
	image14 = models.ImageField(default='', blank=True)
	image15 = models.ImageField(default='', blank=True)
	image16 = models.ImageField(default='', blank=True)
	image17 = models.ImageField(default='', blank=True)
	image18 = models.ImageField(default='', blank=True)


	new_or_established = models.CharField(max_length=20, choices=new_or_established, default='New')
	Swimming_pool = models.BooleanField(default=False)
	Garage = models.BooleanField(default=False)
	Balcony = models.BooleanField(default=False)
	Outdoor_area = models.BooleanField(default=False)
	Undercover_parking = models.BooleanField(default=False)
	Shed = models.BooleanField(default=False)
	Fully_fenced = models.BooleanField(default=False)
	Outdoor_spa = models.BooleanField(default=False)
	Tennis_court = models.BooleanField(default=False)
	Ensuite = models.BooleanField(default=False)
	DishWasher = models.BooleanField(default=False)
	Study = models.BooleanField(default=False)
	Built_in_robes = models.BooleanField(default=False)
	Alarm_system = models.BooleanField(default=False)
	Broadband = models.BooleanField(default=False)
	Floorboards = models.BooleanField(default=False)
	Gym = models.BooleanField(default=False)
	Rumpus_room = models.BooleanField(default=False)
	Workshop = models.BooleanField(default=False)
	Air_conditioning = models.BooleanField(default=False)
	Solar_panels = models.BooleanField(default=False)
	Heating = models.BooleanField(default=False)
	High_energy_efficiency = models.BooleanField(default=False)
	Water_tank = models.BooleanField(default=False)
	Solar_hot_water = models.BooleanField(default=False)
	saved = models.BooleanField(default=False)
	#this saved field is used to change the color of the star when a user has saved a search

	def __str__(self):
		return str(self.id_user)
	# Keywords = models.CharField(max_length=1000, default='')
	# Include_surrounding_suburbs = models.BooleanField(default=False)
	# Exclude_under = models.BooleanField(default=False)


class PosterRent(models.Model):


	PropertyTypeChoice = (
		('House', 'House'),
		('Apartment & Unit', 'Apartment & Unit'),
		('Townhouse', 'Townhouse'),
		('Villa', 'Villa'),
		('Land', 'Land'),
		('Acreage', 'Acreage'),
		('Rural', 'Rural'),
		('Block Of Units', 'Block Of Units'),
		('Retirement Living', 'Retirement Living'),

		)
	bathrooms = (

		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
		('11', '11'),
		('12', '12'),
		('13', '13'),
		('14', '14'),
		('15', '15'),
		('16', '16'),
		('17', '17'),
		('18', '18'),
		('19', '19'),
		('20', '20'),

		)

	bedrooms = (

			('1', '1'),
			('2', '2'),
			('3', '3'),
			('4', '4'),
			('5', '5'),
			('6', '6'),
			('7', '7'),
			('8', '8'),
			('9', '9'),
			('10', '10'),
			('11', '11'),
			('12', '12'),
			('13', '13'),
			('14', '14'),
			('15', '15'),
			('16', '16'),
			('17', '17'),
			('18', '18'),
			('19', '19'),
			('20', '20'),

			)


	car_spaces = (

		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		)

	new_or_established = (
			('New', 'New'),
			('Established', 'Established')
		)
	id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	created = models.DateTimeField(auto_now_add=True)
	Updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'rentuserposts')
	# days_left = models.PositiveIntegerField()

	# address = models.CharField(max_length=1000)
	unit = models.TextField()
	street_number = models.TextField()
	street_name = models.TextField()
	suburb = models.TextField()
	postcode = models.TextField()
	state = models.TextField()
	land_size = models.CharField(max_length=100)

	Property_type = models.CharField(max_length=100, choices=PropertyTypeChoice, default='House')
	description = models.TextField()
	Price = models.PositiveIntegerField()
	image = models.ImageField()
	plan = models.ImageField()
	Bedrooms = models.CharField(max_length=20, choices=bedrooms, default='1')
	Bathrooms = models.CharField(max_length=10, choices = bathrooms, default='1')
	Car_spaces = models.CharField(max_length=10, choices = car_spaces, default='1')

	image1 = models.ImageField(default='', blank=True)
	image2 = models.ImageField(default='', blank=True)
	image3 = models.ImageField(default='', blank=True)
	image4 = models.ImageField(default='', blank=True)
	image5 = models.ImageField(default='', blank=True)
	image6 = models.ImageField(default='', blank=True)
	image7 = models.ImageField(default='', blank=True)
	image8 = models.ImageField(default='', blank=True)
	image9 = models.ImageField(default='', blank=True)
	image10 = models.ImageField(default='', blank=True)
	image11 = models.ImageField(default='', blank=True)
	image12 = models.ImageField(default='', blank=True)
	image13 = models.ImageField(default='', blank=True)
	image14 = models.ImageField(default='', blank=True)
	image15 = models.ImageField(default='', blank=True)
	image16 = models.ImageField(default='', blank=True)
	image17 = models.ImageField(default='', blank=True)
	image18 = models.ImageField(default='', blank=True)


	new_or_established = models.CharField(max_length=20, choices=new_or_established, default='New')
	Swimming_pool = models.BooleanField(default=False)
	Garage = models.BooleanField(default=False)
	Balcony = models.BooleanField(default=False)
	Outdoor_area = models.BooleanField(default=False)
	Undercover_parking = models.BooleanField(default=False)
	Shed = models.BooleanField(default=False)
	Fully_fenced = models.BooleanField(default=False)
	Outdoor_spa = models.BooleanField(default=False)
	Tennis_court = models.BooleanField(default=False)
	Ensuite = models.BooleanField(default=False)
	DishWasher = models.BooleanField(default=False)
	Study = models.BooleanField(default=False)
	Built_in_robes = models.BooleanField(default=False)
	Alarm_system = models.BooleanField(default=False)
	Broadband = models.BooleanField(default=False)
	Floorboards = models.BooleanField(default=False)
	Gym = models.BooleanField(default=False)
	Rumpus_room = models.BooleanField(default=False)
	Workshop = models.BooleanField(default=False)
	Air_conditioning = models.BooleanField(default=False)
	Solar_panels = models.BooleanField(default=False)
	Heating = models.BooleanField(default=False)
	High_energy_efficiency = models.BooleanField(default=False)
	Water_tank = models.BooleanField(default=False)
	Solar_hot_water = models.BooleanField(default=False)
	saved = models.BooleanField(default=False)
	#this saved field is used to change the color of the star when a user has saved a search

	def __str__(self):
		return str(self.id_user)
	# Keywords = models.CharField(max_length=1000, default='')
	# Include_surrounding_suburbs = models.BooleanField(default=False)
	# Exclude_under = models.BooleanField(default=False)



# 	def __str__(self):
# 		return str(self.id)
	# Keywords = models.CharField(max_length=1000, default='')
	# Include_surrounding_suburbs = models.BooleanField(default=False)
	# Exclude_under = models.BooleanField(default=False)



class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.TextField()
    def __str__(self):
        return self.user.username


class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	active = models.BooleanField(default=False)
	created = models.DateField(auto_now=True)

class Ninety(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	active = models.BooleanField(default=False)
	created = models.DateField(auto_now=True)

class ThreeSixty(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	active = models.BooleanField(default=False)
	created = models.DateField(auto_now=True)