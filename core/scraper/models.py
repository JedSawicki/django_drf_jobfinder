from django.db import models

# Create your models here.

class Offer(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    href = models.CharField(max_length=500)
    offer_root = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name