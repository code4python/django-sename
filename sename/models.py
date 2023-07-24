from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your models here.



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()



class Movie(models.Model):
    hall = models.CharField(max_length = 50)
    movie = models.CharField(max_length = 50)
    
    
    def __str__(self) -> str:
        return self.movie

class Guest(models.Model):
    name = models.CharField(max_length = 50)
    mobile = models.CharField(max_length = 50)
    
    def __str__(self) -> str:
        return self.name


class Reservtion(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.guest.name
    
    


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)