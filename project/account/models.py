from django.db import models
from django.contrib.auth.models import User

import uuid



class CreateProfile(models.Model):
	choices = (('Buyer', 'Buyer'),('Seller', 'Seller'))
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField()
	password = models.CharField(max_length=1000)
	category = models.CharField(max_length=30, choices=choices)
	def __str__(self):
		return self.username

# models.CharField(max_length=50, unique=True)