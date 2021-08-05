from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View, CreateView, DetailView, UpdateView
from .models import LaundryBasket, Iron, Request, Payment
from django.contrib.auth.models import User
from users.models import Client, LaundryMan
from .forms import NewLaundryForm, RequestForm, IroningForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from . import maps, sms
import random


def index(request):
    context = {}
    return render(request, 'index.html', context)


class Dashboard(DetailView):
    model = Client
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        client = Client.objects.get(client=self.request.user)
        if LaundryBasket.objects.filter(user=client, completed=False):
            active_laundry = LaundryBasket.objects.get(user=client, completed=False)
            context['Active_laundry_basket'] = LaundryBasket.objects.get(user=client, completed=False)
            if Request.objects.filter(laundry_basket=active_laundry, viewed=False):
                context['requests'] = Request.objects.get(laundry_basket=active_laundry, viewed=False)
            elif Request.objects.filter(laundry_basket=active_laundry):
                context['requests'] = Request.objects.get(laundry_basket=active_laundry)
        laundry_baskets = LaundryBasket.objects.filter(user=client, completed=True).order_by('-date_created')
        n = 3
        laundry_baskets_group = [laundry_baskets[i:i+n] for i in range(0, len(laundry_baskets), 3)]
        context['laundry_baskets_group'] = laundry_baskets_group
        context['payments'] = Payment.objects.filter(user=client)
        laundry_basket = LaundryBasket.objects.filter(user=client, completed=True)
        shirts = 0 
        trousers = 0
        weight = 0
        for laundry in laundry_basket:
            if laundry.shirt:
                shirts += laundry.shirt
            if laundry.trousers:
                trousers += laundry.trousers
            if laundry.weight:
                weight += laundry.weight
        context['shirts'] = shirts
        context['trousers'] = trousers
        context['weight'] = weight
        return context


class ProfileView(DetailView):
    model = Client
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        client = Client.objects.get(client=self.request.user)
        if LaundryBasket.objects.filter(user=client, completed=False):            
            context['Active_laundry_basket'] = LaundryBasket.objects.get(user=client, completed=False)
        laundry_basket = LaundryBasket.objects.filter(user=client, completed=True)
        shirts = 0 
        trousers = 0
        weight = 0
        for laundry in laundry_basket:
            if laundry.shirt:
                shirts += laundry.shirt
            if laundry.trousers:
                trousers += laundry.trousers
            if laundry.weight:
                weight += laundry.weight
        context['shirts'] = shirts
        context['trousers'] = trousers
        context['weight'] = weight
        return context


class LaundryOffice(DetailView):
    model = LaundryMan
    template_name = 'office.html'

    def get_context_data(self, **kwargs):
        context = super(LaundryOffice, self).get_context_data(**kwargs)
        laundry_man = LaundryMan.objects.get(laundry_man=self.request.user)
        if LaundryBasket.objects.filter(laundry_man=laundry_man, completed=False):
            context['Active_laundry_baskets'] = LaundryBasket.objects.filter(laundry_man=laundry_man, completed=False)
        requests = Request.objects.filter(laundry_man=laundry_man, viewed=False).order_by('-id')
        laundry_baskets = LaundryBasket.objects.filter(laundry_man=laundry_man, completed=True).order_by('-date_created')
        n = 3
        request_group = [requests[j:j+n] for j in range(0, len(requests), 3)]
        context['request_group'] = request_group
        laundry_baskets_group = [laundry_baskets[i:i+n] for i in range(0, len(laundry_baskets), 3)]
        context['laundry_baskets_group'] = laundry_baskets_group
        laundry_basket = LaundryBasket.objects.filter(laundry_man=laundry_man, completed=True)
        shirts = 0 
        trousers = 0
        weight = 0
        for laundry in laundry_basket:
            if laundry.shirt:
                shirts += laundry.shirt
            if laundry.trousers:
                trousers += laundry.trousers
            if laundry.weight:
                weight += laundry.weight
        context['shirts'] = shirts
        context['trousers'] = trousers
        context['weight'] = weight
        return context


class LaundryProfileView(DetailView):
    model = LaundryMan
    template_name = 'laundry_profile.html'

    def get_context_data(self, **kwargs):
        context = super(LaundryProfileView, self).get_context_data(**kwargs)
        laundry_man = LaundryMan.objects.get(laundry_man=self.request.user)
        if LaundryBasket.objects.filter(laundry_man=laundry_man, completed=False):            
            context['Active_laundry_basket'] = LaundryBasket.objects.filter(laundry_man=laundry_man, completed=False)
        laundry_basket = LaundryBasket.objects.filter(laundry_man=laundry_man, completed=True)
        shirts = 0 
        trousers = 0
        weight = 0
        for laundry in laundry_basket:
            if laundry.shirt:
                shirts += laundry.shirt
            if laundry.trousers:
                trousers += laundry.trousers
            if laundry.weight:
                weight += laundry.weight
        context['shirts'] = shirts
        context['trousers'] = trousers
        context['weight'] = weight
        return context


class NewLaundry(CreateView):
    model = LaundryBasket
    template_name = 'new_laundry.html'
    form_class = NewLaundryForm

    def get_context_data(self, **kwargs):
        context = super(NewLaundry, self).get_context_data(**kwargs)
        no_of_basket = LaundryBasket.objects.filter(user=self.request.user.client).count()
        context['no_of_basket'] = no_of_basket
        return context


class Newlaundry(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, 'create_laundry.html', context )


def new_laundry(request):
    client = Client.objects.get(client=request.user)
    no_of_basket = LaundryBasket.objects.filter(user=request.user.client).count()
    slug = request.user.username + '-basket-' + str(no_of_basket + 1)
    if request.method == 'POST':
        description = request.POST['description']
        laundry_basket = LaundryBasket.objects.create(user=client, clothing_description=description, slug=slug)
        if request.POST['description'] == 'Weight':
            weight = request.POST['weight']
            laundry_basket.weight = weight
        elif request.POST['description'] == 'quantity':
            shirt = request.POST['shirt']
            trousers = request.POST['trousers']
            suits_and_jackets = request.POST['suits_and_jackets']
            laundry_basket.shirt = shirt
            laundry_basket.trousers = trousers
            laundry_basket.suits_and_jackets = suits_and_jackets

        laundry_basket.save()
        return redirect('dashboard', slug=client.slug)
    else:
        pass


class NewIronBoard(CreateView):
    model = Iron
    template_name = 'new_iron_board.html'
    form_class = IroningForm

    def get_context_data(self, **kwargs):
        context = super(NewIronBoard, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = IroningForm(self.request.POST or None)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_iron");</script>' % (instance.pk, instance))


class PastBasket(DetailView):
    model = LaundryBasket
    template_name = 'past_basket.html'


class LaundryRequest(CreateView):
    model = Request
    template_name = 'request.html'
    form_class = RequestForm

    def get_context_data(self, *args, **kwargs):
        context = super(LaundryRequest, self).get_context_data(**kwargs)
        client = Client.objects.get(client=self.request.user)
        try:
            laundry_basket = LaundryBasket.objects.get(user=client, ordered=False)
            context['laundry_basket'] = laundry_basket
        except ObjectDoesNotExist:
            return HttpResponse('You do not have a laundry basket')
        no_of_request = Request.objects.filter(client=self.request.user.client).count()
        context['no_of_request'] = no_of_request
        return context


def random_select(request):
    user = request.user
    client = Client.objects.get(client=request.user)
    laundry_basket = LaundryBasket.objects.get(user=client, ordered=False)
    if laundry_basket.clothing_description == 'dry clean':
        laundry_men = LaundryMan.objects.filter(verified=True, dry_clean_company=True)
    else:
        laundry_men = LaundryMan.objects.filter(verified=True)
    laundry_men_for_select = []
    for laundry_man in laundry_men:
        distance = maps.distance_matrix(client=user, laundry_man=laundry_man)
        if distance is not None and distance < 10000:
            laundry_men_for_select.append(laundry_man)
    chosen = random.choice(laundry_men_for_select)
    laundry_man = chosen
    no_of_request = Request.objects.filter(client=client).count()
    new_request = Request.objects.create(client=client, laundry_man=laundry_man, laundry_basket=laundry_basket)
    new_request.slug = f'{client.client.username}-request-{no_of_request + 1}'
    new_request.save()
    sms.random_created_sms(client=client, request=new_request, laundry_basket=laundry_basket)
    sms.send_request_sms(laundry_man=laundry_man, request=new_request, laundry_basket=laundry_basket)
    return redirect('dashboard', slug=client.slug)


def map_request(request):
    user = request.user
    client = Client.objects.get(client=user)
    laundry_basket = LaundryBasket.objects.get(user=client, ordered=False)
    client_lat, client_lng = maps.get_client_location(user)
    if laundry_basket.clothing_description == 'dry clean':
        laundry_men = LaundryMan.objects.filter(verified=True, dry_clean_company=True)
    else:
        laundry_men = LaundryMan.objects.all()
    laun_lats, laun_lngs, slugs = maps.get_map_location(client)

    context = {
        'page_vars': {
            'client_lat': client_lat,
            'client_lng': client_lng,
            'laun_lats': laun_lats,
            'laun_lngs': laun_lngs,
            'slugs': slugs
        },
        'client': client,
        'laundry_men': laundry_men
    }

    return render(request, 'google_select.html', context)


def choose_laundry_man(request, slug):
    user = Client.objects.get(client=request.user)
    laundry_man = LaundryMan.objects.get(slug=slug)
    laundry_basket = LaundryBasket.objects.get(user=user, ordered=False)
    no_of_request = Request.objects.filter(client=request.user.client).count()
    new_request = Request.objects.create(client=user, laundry_man=laundry_man, laundry_basket=laundry_basket)
    new_request.slug = f'{user.client.username}-request-{no_of_request + 1}'
    new_request.save()
    sms.request_created_sms(client=user, request=new_request, laundry_basket=laundry_basket)
    sms.send_request_sms(laundry_man=laundry_man, request=new_request, laundry_basket=laundry_basket)
    return redirect('dashboard', slug=user.slug)


class RequestView(DetailView):
    model = Request
    template_name = 'view_request.html'


def completed(request, slug):
    client = Client.objects.get(client=request.user)
    laundry_basket = LaundryBasket.objects.get(user=client, slug=slug, completed=False)
    laundry_basket.completed = True
    laundry_basket.save()
    return redirect('dashboard', slug=client.slug)


def accept_request(request, slug):
    laundry_man = LaundryMan.objects.get(laundry_man=request.user)
    laundry_request = Request.objects.get(laundry_man=laundry_man, slug=slug)
    laundry_request.viewed = True
    laundry_request.accepted = True
    laundry_request.time_accepted = timezone.now()
    laundry_request.save()
    requesting_user = laundry_request.client
    laundry_basket = LaundryBasket.objects.filter(user=requesting_user, ordered=False, completed=False)
    laundry_basket.ordered = True
    laundry_basket.laundry_man = laundry_man
    laundry_basket.save()
    sms.laundry_accepted_sms(
        client=laundry_request.client,
        request=laundry_request,
        laundry_basket=laundry_basket,
        accepted=laundry_request.accepted
    )
    return redirect('office', slug=laundry_man.slug)


def reject_request(request, slug):
    laundry_man = LaundryMan.objects.get(laundry_man=request.user)
    laundry_request = Request.objects.get(laundry_man=laundry_man, slug=slug)
    laundry_request.viewed = True
    laundry_request.accepted = False
    laundry_request.time_accepted = timezone.now()
    laundry_request.save()
    laundry_basket = LaundryBasket.objects.get(request=laundry_request)
    sms.laundry_accepted_sms(
        client=laundry_request.client,
        request=laundry_request,
        laundry_basket=laundry_basket,
        accepted=laundry_request.accepted
    )
    return redirect('office', slug=laundry_man.slug)

