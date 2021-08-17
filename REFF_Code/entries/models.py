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


class Entry(models.Model):
    CATEGORY = (
        # The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name;
        # We'll be using the same naming convention for both;
        ('Tech', 'Tech'),
        ('Health', 'Health'),
        ('Politics', 'Politics'),
        ('History', 'History'),
        ('Education', 'Education'),
        ('Sports', 'Sports'),
        ('Business', 'Business'),
        ('Science', 'Science'),
        ('Other', 'Other')
    )

    fact = models.CharField(max_length=400)
    # URLField() has a URL identifier which makes sure the entry is of format ['http', 'https', 'ftp', 'ftps']
    source = models.URLField(max_length=400)
    short_url = models.CharField(max_length=7, null=True, unique=True)
    category = models.CharField(choices=CATEGORY, max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    normal_entry = models.BooleanField(default=True)

    # Foreign Keys relationships
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    # picture = models.ImageField(blank=True, null=True)
    # special_files = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.fact


class Review(models.Model):

    VALUES = (
        (0, 0), (1, 1), (2, 2),
        (3, 3), (4, 4), (5, 5)
    )
    
    VALUES_EXPERTISE = (
        # Academic
        (1,1),
        # Professional
        (2,2), 
        # Academic and professional
        (3,3),
        # None
        (0,0)
    )

    rating = models.FloatField(choices=VALUES, default=0)
    expertise = models.IntegerField(choices=VALUES_EXPERTISE)
    comment = models.CharField(max_length=400)

    entry = models.ForeignKey("Entry", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)


class Like(models.Model):

    entry = models.ForeignKey("Entry", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user[" + str(self.user) + "] LIKED entry[" + str(self.entry.id) + "]"


# Not relevant anymore:
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username

# Not relevant anymore:
# class Contributor(models.Model):
#     # We user OneToOneField instead of ForeignKey so that
#     # there is one Contributor per User
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.CharField(max_length=100)
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.email

# We got rid of the UserProfile model so the following code is not relevant anymore
# def post_user_created_signal(sender, instance, created, **kwargs):
#     print('User created / modified: ', instance)
#     print('Was this user just created? ', created)

#     # if the user was just created (therefore not modified)
#     if created:
#         UserProfile.objects.create(user=instance)

# # When a User is created, Django sends out a post_save signal which triggers the run of the 'post_user_created_signal' function
# post_save.connect(post_user_created_signal, sender=User)
