from django.db import models


# Create your models here.
class TimelinePoll(models.Model):
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False)
    year = models.IntegerField(null=True)
    description = models.TextField()
