from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'username', 'password1', 'password2']
        

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': 'form3Example4c'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name', 'email', 'username',
                  'location','short_intro', 'bio' , 'profile_image',
                  'social_instagram', 'social_twitter',
                  'social_youtube', 'social_website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


