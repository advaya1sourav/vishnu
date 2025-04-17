
from django.contrib.auth.models import AbstractUser
from django.db import models

class Volunteer(AbstractUser):
    
    dob = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.IntegerField(default=0, blank=True, null=True)
    is_organizer = models.BooleanField(default=False)  # Admin-controlled
    request_organizer = models.BooleanField(default=False)  # Tracks requests
    is_approved = models.BooleanField(default=False)  # Admin must approve organizers



    

    def __str__(self):
        return self.username

class Organizer(models.Model):
    user = models.OneToOneField(Volunteer, on_delete=models.CASCADE)  # Linking the Organizer to a Volunteer user
    

