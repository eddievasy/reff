from django.db import models

# We want to have a connection between our platform's 
# users and the database, therefore we import:
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Inherit the AbstractUser and create our own class from it
class User(AbstractUser):
    pass

class Entry(models.Model):
    CATEGORY = (
        ('Technology','Technology'),
        ('Nutrition','Nutrition'),
        ('Politics','Politics')
        # To add more
    )

    fact = models.CharField(max_length=50)
    source = models.URLField()
    credibility = models.FloatField()
    category = models.CharField(choices=CATEGORY,max_length=100)

    # Foreign Keys relationships
    user = models.ForeignKey("Contributor", on_delete=models.CASCADE)
    
    # picture = models.ImageField(blank=True, null=True)
    # special_files = models.FileField(blank=True, null=True)

    def __str__ (self):
        return self.fact


class Contributor(models.Model):
    # We user OneToOneField instead of ForeignKey so that 
    # there is one Contributor per User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email
