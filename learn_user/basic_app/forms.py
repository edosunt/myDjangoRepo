from django import forms
from django.contrib.auth.models import User
from basic_app.models import User, UserProfileInfo

# creating normal base form for the User class
class UserForm(forms.ModelForm):
    # specifying the password field
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ['username','password','email']

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ['portfolio_site','profile_pic']
