from django.db import models

# Create your models here.

class Offer(models.Model):
    name = models.CharField(max_length=50, unique=False)
    
    def __str__(self):
        return self.name
    
    
