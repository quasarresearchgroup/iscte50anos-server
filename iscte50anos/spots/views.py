import random
from datetime import datetime

from django.shortcuts import render

# Create your views here.
from _controllers import spots_controller
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from topics.models import Topic, TopicAccess

from topics.serializers import TopicSerializer

from _controllers import quiz_controller

from spots.models import QRCode, QRCodeAccess, QRCodePermit, Layout

from spots.serializers import SpotSerializer



@api_view()
@permission_classes([IsAuthenticated])
def access_qrcode(request, uuid):
    qrcode = QRCode.objects.get(uuid=uuid)
    has_permit = QRCodePermit.objects.filter(user=request.user, qrcode=qrcode).exists()
    if has_permit:
        has_access = QRCodeAccess.objects.filter(user=request.user, qrcode=qrcode).exists()
        if not has_access:
            QRCodeAccess.objects.create(user=request.user, qrcode=qrcode)
            QRCodePermit.objects.filter(user=request.user, qrcode=qrcode).delete()

            qrcode_accesses = list(QRCodeAccess.objects.filter(user=request.user))
            visited_qrcode_ids = [access.qrcode.id for access in qrcode_accesses]
            unvisited_qrcodes = list(QRCode.objects.exclude(id__in=visited_qrcode_ids))

            # UPDATE STATS
            spots_controller.update_total_spots_read(request.user)
            spots_controller.update_total_spot_time(request.user)

            if len(unvisited_qrcodes) == 5:
                return Response({"message": "Parabéns, visitaste todos os Spots!"}, status=200)

            next_qrcode = random.choice(unvisited_qrcodes)
            QRCodePermit.objects.create(user=request.user, qrcode=next_qrcode)

            # Check layouts to see where is the next QRCode
            today = datetime.today().strftime('%Y-%m-%d')
            next_spot = Layout.objects.get(period__start_date__lte=today,
                                           period__end_date__gte=today,
                                           qrcode=next_qrcode).spot
            if next_spot is None:
                return Response({"error": "Não existem QR Codes ativos de momento"}, status=403)

            serializer = SpotSerializer(next_spot)
            return Response(serializer.data)
        else:
            return Response({"error": "Já visitaste este Spot"}, status=403)
    else:
        return Response({"error": "Não podes aceder a este Spot ainda"}, status=403)
