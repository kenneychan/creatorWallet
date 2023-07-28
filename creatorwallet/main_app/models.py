from django.db import models
# Import the User
from django.contrib.auth.models import User

# # Create your models here.
# class Cat(models.Model):
#   ...
#   # toys = models.ManyToManyField(Toy)
#   # Add the foreign key linking to a user instance
#   user = models.ForeignKey(User, on_delete=models.CASCADE)