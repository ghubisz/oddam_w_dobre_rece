import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import dateutil.utils

class Category(models.Model):
    name= models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Institution(models.Model):
    name=models.CharField(max_length=128)
    description = models.TextField()
    #type=
    categories= models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity= models.DecimalField(max_digits=6, decimal_places=2)
    categories=models.ForeignKey(to=Category, on_delete=models.CASCADE)
    institution
    address = models.TextField()
    phone_number = models.DecimalField(max_digits=9)
    city = models.TextField()
    zip_code = models.DecimalField(max_digits=5)
    pick_up_date = models.DateField()
    pick_up_time
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
