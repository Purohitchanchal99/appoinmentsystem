from django import forms
from .models import User  # Assuming your custom user model is in the same app

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Add other fields as needed
