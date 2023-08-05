from django import forms
# from django.forms import Form
from .models import Booking, Menu


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = fields = ['name', 'price', 'description', 'menu_image']
