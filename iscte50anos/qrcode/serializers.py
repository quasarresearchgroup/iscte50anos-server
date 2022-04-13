from rest_framework import serializers

from qrcode.models import QRCode


class QRCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = QRCode
        fields = ['link']


