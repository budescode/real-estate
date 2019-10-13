from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid



# class CreateProfile(models.Model):
# 	username = models.CharField(max_length=50, unique=True)
# 	email = models.EmailField()
# 	password = models.CharField(max_length=1000)
# 	def __str__(self):
# 		return self.username

class PasswordResetEmail(models.Model):
	email = models.EmailField()
class ChangePasswordCode(models.Model):
	user_email = models.EmailField(max_length=50)
	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
class ChangePassword(models.Model):
	new_password = models.CharField(max_length=50, blank = False, null = False)
	confirm_new_password = models.CharField(max_length=50, blank = False, null = False)


class Profile(models.Model):
	choices = (('Buyer', 'Buyer'),('Seller', 'Seller'))
	select_choices = (('Individual', 'Individual'),('Agency', 'Agency'))

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_category')
	category = models.CharField(max_length=30, choices=choices)
	brand = models.CharField(max_length=30, choices=select_choices, blank=True, help_text='Select Your brand')

class Profile(models.Model):
	choices = (('Buyer', 'Buyer'),('Seller', 'Seller'))
	select_choices = (('Individual', 'Individual'),('Agency', 'Agency'))

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_category')
	category = models.CharField(max_length=30, choices=choices)
	brand = models.CharField(max_length=30, choices=select_choices, blank=True, help_text='Select Your brand')


class UserRegister(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=13, help_text='Starts with +910')
	email = models.EmailField()
	password = models.CharField(max_length=100)


