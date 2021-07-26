from django.contrib import auth
from django.contrib.auth.models import User, UserManager
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import DetailView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import SignUpForm, PasswordChangedForm, ClientForm, LaundryManForm
from .models import Client, LaundryMan
from washapp.models import LaundryBasket


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            pass
    else:
            pass


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name= lastname
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            print('wrong password')
    else:
        print('error')

class EditProfileView(DetailView):
    model = Client
    template_name = 'registration/editprofile.html'

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
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



def edit_profile(request):
    if request.method == 'POST':
        if request.user.client:
            client = Client.objects.get(client=request.user)
            user = User.objects.get(username=request.user.username)
            user.email = request.POST['email']
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            client.phone_number = request.POST['phone_number']
            client.auxiliary_phone_number = request.POST['auxilary_phone_number'] or None
            client.street_address = request.POST['street']
            client.area = request.POST['area']
            client.house_number = request.POST['house_number']
            client.city = request.POST['city']
            client.state = request.POST['state']
            client.about = request.POST['about']
            client.save()
            user.save()
            return redirect('profile', slug=client.slug)
        elif request.user.laundryman:
            pass
        pass


class EditLaundryProfileView(DetailView):
    model = LaundryMan
    template_name = 'registration/edit_laundry_profile.html'

    def get_context_data(self, **kwargs):
        context = super(EditLaundryProfileView, self).get_context_data(**kwargs)
        laundry_man = LaundryMan.objects.get(laundry_man=self.request.user)
        if LaundryBasket.objects.filter(laundry_man=laundry_man, completed=False):            
            context['Active_laundry_basket'] = LaundryBasket.objects.get(laundry_man=laundry_man, completed=False)
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


def edit_laundry_profile(request):
    if request.method == 'POST':
        if request.user.laundryman:
            laundry_man = LaundryMan.objects.get(laundry_man=request.user)
            user = User.objects.get(username=request.user.username)
            user.email = request.POST['email']
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            laundry_man.phone_number = request.POST['phone_number']
            laundry_man.auxiliary_phone_number = request.POST['auxilary_phone_number'] or None
            laundry_man.street_address = request.POST['street']
            laundry_man.area = request.POST['area']
            laundry_man.house_number = request.POST['house_number']
            laundry_man.city = request.POST['city']
            laundry_man.state = request.POST['state']
            laundry_man.about = request.POST['about']
            laundry_man.save()
            user.save()
            return redirect('office', slug=laundry_man.slug)
        elif request.user.client:
            pass
        pass

class ClientFormView(generic.CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'registration/client.html'
    success_url = reverse_lazy('index')


class LaundryManFormView(generic.CreateView):
    model = LaundryMan
    form_class = LaundryManForm
    template_name = 'registration/laundry_man.html'
    success_url = reverse_lazy('index')


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangedForm
    success_url = reverse_lazy('password_updated')


def password_success(request):
    return render(request, 'registration/password_updated.html', {})

