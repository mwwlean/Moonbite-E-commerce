# crudapp/forms.py

from django import forms
from .models import Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "name",
            "description",
            "price",
            "image",
            "stock",
        ]  # Include 'price' field in form


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # Not staff (admin)
        user.is_superuser = False  # Not superuser (admin)
        user.save()
        return user
