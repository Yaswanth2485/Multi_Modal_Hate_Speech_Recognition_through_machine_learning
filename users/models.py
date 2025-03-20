from django.db import models
from django.utils.timezone import now


class registrationmodel(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    mobile = models.CharField(unique=True,max_length=20)
    status = models.CharField(max_length=100, default='waiting')
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=now) 
    
    
    def __str__(self):
        return self.name




