from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Client, LaundryMan


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class PasswordChangedForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('client', 'phone_number', 'auxiliary_phone_number', 'house_number', 'street_address', 'area', 'city', 'state', 'slug')

        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'client', 'type': 'hidden'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'auxiliary_phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'house_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'slug', 'type': 'hidden'}),
        }


class LaundryManForm(forms.ModelForm):
    class Meta:
        model = LaundryMan
        fields = ('laundry_man', 'phone_number', 'auxiliary_phone_number', 'house_number', 'street_address', 'area',
                  'city', 'state', 'dry_clean_company', 'slug')

        widgets = {
            'laundry_man': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'laundry_man', 'type': 'hidden'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'auxiliary_phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'house_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'dry_clean_company': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'slug', 'type': 'hidden'}),
        }

