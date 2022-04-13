from django.conf import settings
from django.db import models


class QRCode(models.Model):
    uuid = models.UUIDField()
    link = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    # Serve API in order of content type


class QRCodeAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)
    #is_scan = models.BooleanField()

    def __str__(self):
        return f'{self.topic} - {self.user}'
