from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    # Create one to one relationship with User class
    # Do not inherit from that class, since it will messed up the databases
    user = models.OneToOneField(User, on_delete='cascade')

    # Add your additional field
    portfolio_site = models.URLField(blank = True) # it's optional blank = True

    # to use this you need pip install pillow
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank=True)

    def __str__ (self):
        return self.user.username
