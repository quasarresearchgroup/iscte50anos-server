from django.db import models

# Create your models here.
class AccessLog(models.Model):
    origin_ip = models.CharField(max_length=15)
    link = models.CharField(max_length=100)
    access_time = models.DateTimeField(auto_now_add=True)