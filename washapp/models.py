from django.db import models
from users.models import Client, LaundryMan
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Iron(models.Model):
    shirt = models.IntegerField(blank=True, null=True)
    trousers = models.IntegerField(blank=True, null=True)
    suits_and_jackets = models.IntegerField(blank=True, null=True)

    def get_iron_cost(self):
        shirt_rate = 100
        trouser_rate = 150
        jacket_rate = 300
        shirt_cost = 0
        trouser_cost = 0
        jacket_cost = 0
        if self.shirt:
            shirt_cost = self.shirt * shirt_rate
        if self.trousers:
            trouser_cost = self.trousers * trouser_rate
        if self.suits_and_jackets:
            jacket_cost = self.suits_and_jackets * jacket_rate
        cost = shirt_cost + trouser_cost + jacket_cost
        return cost


class LaundryBasket(models.Model):

    class Description(models.TextChoices):
        WEIGHT = 'Weight', _('weight')
        Quantity = 'quantity', _('quantity')
        Dry_Clean = 'dry clean', _('dry clean')

    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    laundry_man = models.ForeignKey(LaundryMan, null=True, on_delete=models.SET_NULL)
    clothing_description = models.CharField(choices=Description.choices, max_length=10)
    weight = models.FloatField(blank=True, null=True)
    shirt = models.IntegerField(blank=True, null=True)
    trousers = models.IntegerField(blank=True, null=True)
    suits_and_jackets = models.IntegerField(blank=True, null=True)
    natives = models.IntegerField(blank=True, null=True)
    underwear = models.IntegerField(blank=True, null=True)
    bedsheets = models.IntegerField(blank=True, null=True)
    blankets_and_duvets = models.IntegerField(blank=True, null=True)
    iron = models.OneToOneField(Iron, null=True, blank=True, on_delete=models.SET_NULL)
    ordered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_required = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    rating = models.IntegerField(choices=RATING, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f'{self.user.client.username} basket, attended to by'

    def get_absolute_url(self):
        slug = str(self.user.slug)
        return reverse('dashboard', kwargs={'slug': slug})

    def get_weight_cost(self):
        rate = 1500
        cost = self.weight * rate
        return cost

    def get_quantity_cost(self):
        shirt_rate = 200
        trouser_rate = 300
        jacket_rate = 500
        shirt_cost = 0
        trouser_cost = 0
        jacket_cost = 0
        if self.shirt:
            shirt_cost = shirt_rate * self.shirt
        if self.trousers:
            trouser_cost = self.trousers * trouser_rate
        if self.suits_and_jackets:
            jacket_cost = self.suits_and_jackets * jacket_rate
        cost = shirt_cost + trouser_cost + jacket_cost
        return cost

    def get_dry_clean_cost(self):
        shirt_rate = 300
        trouser_rate = 450
        jacket_rate = 700
        shirt_cost = 0
        trouser_cost = 0
        jacket_cost = 0
        if self.shirt:
            shirt_cost = shirt_rate * self.shirt
        if self.trousers:
            trouser_cost = self.trousers * trouser_rate
        if self.suits_and_jackets:
            jacket_cost = self.suits_and_jackets * jacket_rate
        cost = shirt_cost + trouser_cost + jacket_cost
        return cost

    def get_total_cost(self):
        wash_cost = 0
        iron_cost = 0
        if self.clothing_description == 'Weight':
            wash_cost = self.get_weight_cost()

            if self.iron:
                iron_cost = self.iron.get_iron_cost()
            else:
                iron_cost = 0
        elif self.clothing_description == 'quantity':
            wash_cost = self.get_quantity_cost()

            if self.iron:
                iron_cost = self.iron.get_iron_cost()
            else:
                iron_cost = 0

        elif self.clean_fields == 'dry clean':
            wash_cost = self.get_dry_clean_cost()

        total_cost = wash_cost + iron_cost
        return total_cost


class Payment(models.Model):
    user = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    laundry_basket = models.OneToOneField(LaundryBasket, null=True, on_delete=models.SET_NULL)
    amount = models.FloatField()
    transaction_id = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class Request(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    laundry_man = models.ForeignKey(LaundryMan, on_delete=models.CASCADE)
    laundry_basket = models.ForeignKey(LaundryBasket, on_delete=models.CASCADE)
    accepted = models.BooleanField(null=True)
    viewed = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_accepted = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.client.client.username} request to {self.laundry_man.laundry_man.username}'

    def get_absolute_url(self):
        slug = str(self.client.slug)
        return reverse('dashboard', kwargs={'slug': slug})

# Create your models here.


