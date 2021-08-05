from django import forms
from .models import Request, Iron, LaundryBasket, Payment


class NewLaundryForm(forms.ModelForm):
    class Meta:
        model = LaundryBasket
        fields = ('user', 'clothing_description', 'weight', 'shirt', 'trousers', 'suits_and_jackets',
                  'natives', 'underwear', 'bedsheets', 'blankets_and_duvets', 'date_required', 'iron', 'slug')

        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'client', 'type': 'hidden'}),
            'clothing_description': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control form-control-alternative'}),
            'shirt': forms.NumberInput(attrs={'class': 'form-control form-control-alternative'}),
            'trousers': forms.NumberInput(attrs={'class': 'form-control form-control-alternative'}),
            'suits_and_jackets': forms.NumberInput(attrs={'class': 'form-control form-control-alternative'}),
            'natives': forms.NumberInput(attrs={'class': 'form-control form-control-alternative'}),
            'underwear': forms.NumberInput(attrs={'class': 'form-control form-control-alternative'}),
            'bedsheets': forms.NumberInput(attrs={'class': 'form-control form-control-alternative'}),
            'blankets_and_duvets': forms.NumberInput(attrs={'class': 'form-control form-control-alternative'}),
            'date_required': forms.DateInput(attrs={'class': 'form-control form-control-alternative', 'placeholder': '2000-12-21'}),
            'iron': forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'slug', 'type': 'hidden'}),
    }


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('client', 'laundry_man', 'laundry_basket', 'slug')

        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'client', 'type': 'hidden'}),
            'laundry_man': forms.Select(attrs={'class': 'form-control'}),
            'laundry_basket': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'laundry', 'type': 'hidden'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'slug', 'type': 'hidden'}),
        }


class IroningForm(forms.ModelForm):
    class Meta:
        model = Iron
        fields = ('shirt', 'trousers', 'suits_and_jackets')

        widgets = {
            'shirt': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'trousers': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'suits_and_jackets': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
