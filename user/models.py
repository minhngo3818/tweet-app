from django.db import models
from django.contrib.auth.models import User

import uuid
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='images', default='default-avatar.png', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    @property
    def imageURL(self):
        try:
            img_url = self.profile_img.url
        except:
            img_url = ''

        return img_url

    class Meta:
        ordering = ['created']

class Tweet(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['created']