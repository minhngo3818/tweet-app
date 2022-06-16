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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='tweets')
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # comments = models.OneToManyField(Tweet, default=None, blank=True, related_name='comments')
    liked = models.ManyToManyField(Profile, default=None, blank=True, related_name='liked')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.name

    @property
    def numLikes(self):
        num_likes = str(self.liked.all().count()) + " Like"
        if self.liked.all().count() > 1:
            num_likes += "s"
        return num_likes


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_comment')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True, blank=True, related_name='comments_set')
    content = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    liked = models.ManyToManyField(Profile, default=None, blank=True, related_name='comment_like')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    class Meta:
        ordering = ['created', '-updated']

    def __str__(self):
        return "{}, comment created on {}".format(self.author.name, self.content)

    @property
    def numLikes(self):
        num_likes = str(self.liked.all().count()) + " Like"
        if self.liked.all().count() > 1:
            num_likes += "s"
        return num_likes


class Like(models.Model):
    LIKE_CHOICES = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike')
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.tweet)

class LikeComment(models.Model):
    LIKE_CHOICES = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike')
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.comment)
# Add hashing protect when render id on html templates