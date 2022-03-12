from django import forms
from accounts.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OrderForm(forms.ModelForm):
	class Meta:
		model = Orders
		fields='__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username','email','password1','password2')

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customers
		fields = "__all__"
		exclude = ['user']