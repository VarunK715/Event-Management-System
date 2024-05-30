from django import forms
from django.contrib.auth.models import User
from .models import CustomUser,Profile
from django.contrib.auth.forms import UserCreationForm

# class UserProfile(UserCreationForm):
#     #if you add fields here then it will be visible after password2 , 
#     #but if you add it in fields below where you want , it will show like that in form
#     organization = forms.CharField(max_length=200)
#     class Meta:
#         model = User
#         fields = ('username','email','organization') #arrangement order to view in form


class UserOForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','organization','phone','work','image']

    
class UserPForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','phone','work','image']

