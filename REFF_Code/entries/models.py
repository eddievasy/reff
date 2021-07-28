# After making changes here, the following terminal commands are to be used:
# python manage.py makemigrations
# python manage.py migrate

# python manage.py createsuperuser  --> to be used when the old DB is wiped out

from django.db import models

# We want to have a connection between our platform's
# users and the database, therefore we import:
from django.contrib.auth.models import AbstractUser

# this signal listens for when the user is actually created in the DB
from django.db.models.signals import post_save


# Inherit the AbstractUser and create our own class from it
class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Entry(models.Model):
    CATEGORY = (
        ('Technology', 'Technology'),
        ('Nutrition', 'Nutrition'),
        ('Politics', 'Politics')
        # To add more
    )

    fact = models.CharField(max_length=50)
    source = models.URLField()
    credibility = models.FloatField()
    category = models.CharField(choices=CATEGORY, max_length=100)

    # Foreign Keys relationships
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    # picture = models.ImageField(blank=True, null=True)
    # special_files = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.fact


class Contributor(models.Model):
    # We user OneToOneField instead of ForeignKey so that
    # there is one Contributor per User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


def post_user_created_signal(sender, instance, created, **kwargs):
    print('User created / modified: ', instance)
    print('Was this user just created? ', created)

    # if the user was just created (therefore not modified)
    if created:
        UserProfile.objects.create(user=instance)


# When a User is created, Django sends out a post_save signal which triggers the run of the 'post_user_created_signal' function
post_save.connect(post_user_created_signal, sender=User)
