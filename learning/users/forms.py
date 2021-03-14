from django import forms

from users.models import Profile

class UpdateUser(forms.Form):
    website = forms.URLField(max_length=200, required=True)

    biography = forms.CharField(max_length=256,  required=False)

    phone_number = forms.CharField(max_length=20, required=True)

    picture = forms.ImageField(required=False)