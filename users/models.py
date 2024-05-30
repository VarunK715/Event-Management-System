from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Organizer', 'Organizer'),
        ('Participant', 'Participant'),
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    objects = CustomUserManager()  # Use your custom manager


    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    bio = models.CharField(max_length=100,default='Default Bio')
    organization = models.CharField(max_length=200,default='Default organization')
    phone = models.CharField(max_length=12,default='987654321')
    work  = models.CharField(max_length=250,default='Developer')
    image = models.ImageField(default='default1.png',upload_to='profile_images/')

    def __str__(self):
        return self.username



