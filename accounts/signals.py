from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a Profile whenever a User is created
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Save the Profile whenever the User is saved
    """
    try:
        instance.profile.save() # This will save the profile if it exists
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance) #If profile doesn't exist for some reason, it will be created