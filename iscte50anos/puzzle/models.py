from django.conf import settings
from django.db import models
from spots.models import Spot


class Puzzle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    def __str__(self):
        return f"PUZZLE: {self.user} | {self.spot}"
