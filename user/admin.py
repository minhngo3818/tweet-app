from django.contrib import admin
from .models import Profile, Tweet, Like, Comment, LikeComment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(LikeComment)