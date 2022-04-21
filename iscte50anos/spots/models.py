from django.conf import settings
from django.db import models


class QRCode(models.Model):
    uuid = models.UUIDField()

    def __str__(self):
        return f'{self.id} - {self.uuid}'

    # Serve API in order of content type


class QRCodePermit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE)

    def location_photo_link(self):
        return self

    def __str__(self):
        return f'{self.qrcode} - {self.user}'


class QRCodeAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.qrcode} - {self.user}'


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