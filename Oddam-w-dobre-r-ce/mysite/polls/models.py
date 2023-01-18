import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import dateutil.utils
from enum import Enum

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Institution(models.Model):

    class mType(models.IntegerChoices):
        FUNDACJA = 1
        ORGANIZACJA_POZARZĄDOWA= 2
        ZBIÓRKA_LOKALNA = 3

    type = models.IntegerField(choices=mType.choices)

    name = models.CharField(max_length=128)
    description = models.TextField()

    categories = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    categories = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    institution = models.ForeignKey(to=Institution, on_delete=models.CASCADE)
    address = models.TextField()
    address_home_nr = models.DecimalField(max_digits=6, decimal_places=3)
    phone_number = models.DecimalField(max_digits=9,  decimal_places=0)
    city = models.TextField()
    zip_code = models.DecimalField(max_digits=5, decimal_places=0)
    pick_up_date = models.DateField()
    pick_up_time = models.IntegerField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

