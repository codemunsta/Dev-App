import os
from django.contrib.auth.models import User
import requests
from users.models import Client, LaundryMan
from .models import LaundryBasket
import pprint


def get_client_location(client):
    user = Client.objects.get(client=client)
    API_KEY = os.environ['Map_key']

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    name = user.client.username
    address = f'{user.house_number} {user.street_address}, {user.area}, {user.state}'

    params = {
            'key': API_KEY,
            'address': address
        }

    response = requests.get(base_url, params=params).json()
    print(response['status'])

    if response['status'] == 'OK':
        lat = response['results'][0]['geometry']['location']['lat']
        lng = response['results'][0]['geometry']['location']['lng']
        print(lat, lng)

        return lat, lng


def get_map_location(client):
    API_KEY = os.environ['Map_key']

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    laundry_basket = LaundryBasket.objects.get(user=client, ordered=False)

    if laundry_basket.clothing_description == 'dry clean':
        laundry_men = LaundryMan.objects.filter(verified=True, dry_clean_company=True)
    else:
        laundry_men = LaundryMan.objects.all()
    pprint.pprint(laundry_men)
    lat = []
    lng = []
    slugs = []

    for laundry_man in laundry_men:
        name = laundry_man.laundry_man.username
        print(name)
        address = f'{laundry_man.house_number} {laundry_man.street_address}, {laundry_man.area}, {laundry_man.state}'
        slug = laundry_man.slug
        slugs.append(slug)

        params = {
            'key': API_KEY,
            'address': address
        }

        response = requests.get(base_url, params=params).json()

        if response['status'] == 'OK':
            lat.append(response['results'][0]['geometry']['location']['lat'])
            lng.append(response['results'][0]['geometry']['location']['lng'])

    return lat, lng, slugs


def distance_matrix(client, laundry_man):
    user = Client.objects.get(client=client)
    laundryman = laundry_man
    address = f'{user.house_number} {user.street_address}, {user.area}, {user.state}'
    laundry_address = f'{laundryman.house_number} {laundryman.street_address}, {laundryman.area}, {laundryman.state}'
    API_KEY = os.environ['Map_Key']
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    params = {
        'key': API_KEY,
        'origins': address,
        'destinations': laundry_address,
        'mode': 'car'
    }

    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        result = response['rows']
        for element in result:
            for distance in element['elements']:
                distance_m = distance['distance']['value']
                return distance_m
    else:
        print('An error occurred')
        return
