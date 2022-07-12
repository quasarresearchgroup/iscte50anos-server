from django.conf import settings
from django.db import models

from topics.models import Topic


class QRCode(models.Model):
    uuid = models.UUIDField()
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id} - {self.uuid}'

    # Serve API in order of content type


class QRCodeAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE)

    # Changed when accessed
    has_accessed = models.BooleanField(default=False)
    access_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.has_accessed:
            return f'{self.qrcode} - {self.user} (accessed time: {self.access_date})'
        else:
            return f'{self.qrcode} - {self.user} (NOT ACCESSED)'


class Spot(models.Model):
    description = models.CharField(max_length=100, blank=True)
    location_photo_link = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.description}'


class LayoutPeriod(models.Model):
    description = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    def __str__(self):
        return f'{self.description}: {self.start_date} to {self.end_date}'


class Layout(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    period = models.ForeignKey(LayoutPeriod, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.spot} | {self.qrcode} | {self.period}'