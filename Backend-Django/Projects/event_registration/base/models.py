from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    # avatar =
    hackathon_participant = models.BooleanField(default=True, null=True)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']


class Event(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True, related_name='events')
    date = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    details = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.event) + ' ------- ' + str(self.participant)


