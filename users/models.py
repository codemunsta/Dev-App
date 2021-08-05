from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Client(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    auxiliary_phone_number = models.IntegerField(null=True, blank=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='images/client/', default='static/main/images/g3.png')
    header_pic = models.ImageField(blank=True, null=True, upload_to='images/client/header/', default='static/main/images/g3.png')
    house_number = models.IntegerField()
    street_address = models.TextField(max_length=300)
    area = models.TextField(max_length=300)
    city = models.TextField(max_length=150)
    state = models.TextField(max_length=150)
    about = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.client.username + ' | ' + str(self.phone_number)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})


class LaundryMan(models.Model):
    laundry_man = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='images/laundrymen/', default='static/main/images/g3.png')
    header_pic = models.ImageField(blank=True, null=True, upload_to='images/laundrymen/header/', default='static/main/images/g3.png' )
    phone_number = models.IntegerField()
    auxiliary_phone_number = models.IntegerField(null=True, blank=True)
    house_number = models.IntegerField()
    street_address = models.TextField(max_length=300)
    area = models.TextField(max_length=300)
    city = models.TextField(max_length=150)
    state = models.TextField(max_length=150)
    about = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    dry_clean_company = models.BooleanField()
    active = models.BooleanField(default=False)
    rating = models.FloatField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.laundry_man.username + ' | ' + str(self.phone_number)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})


# Create your models here.
