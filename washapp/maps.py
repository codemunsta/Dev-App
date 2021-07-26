from django.contrib.auth.models import User
import requests
from users.models import Client, LaundryMan
import pprint


def get_client_location(client):
    user = Client.objects.get(client=client)

    API_KEY = 'AIzaSyBsctqI83IxHI_LgC5EtMI0tKfG-SeKltw'

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

        return(lat, lng)


def get_map_location():
    API_KEY = 'AIzaSyBsctqI83IxHI_LgC5EtMI0tKfG-SeKltw'

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

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

    return(lat, lng, slugs)