from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User
from django.conf import settings

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(sender,instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

    print('Deleted user!')


