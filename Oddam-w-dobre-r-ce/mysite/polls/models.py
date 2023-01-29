import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
import dateutil.utils
from enum import Enum
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = ('Kategorie')

class Institution(models.Model):

    class InstitutionType(models.TextChoices):
        FOUNDATION = 'FUND', 'Fundacja',
        NON_GOV = 'NGOV', 'Organizacja pozarządowa',
        CHARITY = 'CHAR', 'Zbiórka lokalna',

    institution_type = models.CharField(max_length=4,
                                        choices=InstitutionType.choices,
                                        default=InstitutionType.FOUNDATION)

    name = models.CharField(max_length=128)
    description = models.TextField()

    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = ('Instytucje')

#class CustomUser(AbstractUser):
#    email = models.EmailField(('Email address'), unique=True)

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
        return self.institution.name

    class Meta:
        ordering = ('pick_up_date', 'pick_up_time')
        verbose_name_plural = ('Donacje')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

