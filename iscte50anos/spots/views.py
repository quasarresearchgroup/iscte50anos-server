import random
from datetime import datetime

from django.db import transaction
from django.shortcuts import render

# Create your views here.
from _controllers import spots_controller
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from topics.models import Topic, TopicAccess

from topics.serializers import TopicSerializer

from _controllers import quiz_controller

from spots.models import QRCode, QRCodeAccess, Layout, LayoutPeriod

from spots.serializers import SpotSerializer


@api_view()
@permission_classes([IsAuthenticated])
@transaction.atomic
def get_or_create_permit(request):
    today = datetime.today().strftime('%Y-%m-%d')

    num_accesses = request.user.profile.num_spots_read
    if num_accesses >= 4:
        return Response({"message": "Parabéns, visitaste todos os Spots!"}, status=200)

    has_any_access = QRCodeAccess.objects.filter(user=request.user).exists()

    if not has_any_access:
        qrcode = random.choice(list(QRCode.objects.all()))
        QRCodeAccess.objects.create(user=request.user, qrcode=qrcode)
    else:
        qrcode = QRCodeAccess.objects.filter(user=request.user, has_accessed=False).first().qrcode

    try:
        layout = Layout.objects.get(period__start_date__lte=today,
                                    period__end_date__gte=today,
                                    qrcode=qrcode)
        return Response(data=SpotSerializer(layout.spot).data)
    except Layout.DoesNotExist:
        return Response({"message": "Não existem QR Codes ativos de momento"}, status=403)



@api_view()
@permission_classes([IsAuthenticated])
@transaction.atomic
def access_qrcode(request, uuid):
    try:
        qrcode = QRCode.objects.get(uuid=uuid)

        num_accesses = request.user.profile.num_spots_read
        if num_accesses >= 4:
            return Response({"message": "Parabéns, visitaste todos os Spots!"}, status=200)

        # Lock access to prevent data inconsistency
        access = QRCodeAccess.objects.select_for_update().filter(user=request.user, qrcode=qrcode).first()

        if access is None:
            return Response({"message": "Não podes aceder a este Spot ainda"}, status=403)
        elif access.has_accessed:
            return Response({"message": "Já visitaste este Spot"}, status=403)

        access.has_accessed = True
        access.save() # AUTO SAVES Date

        # UPDATE STATS
        spots_controller.update_total_spots_read(request.user)
        spots_controller.update_total_spot_time(request.user)

        if num_accesses >= 3:
            return Response({"message": "Parabéns, visitaste todos os Spots!"}, status=200)

        qrcode_accesses = list(QRCodeAccess.objects.filter(user=request.user))
        visited_qrcode_ids = [access.qrcode.id for access in qrcode_accesses]
        unvisited_qrcodes = list(QRCode.objects.exclude(id__in=visited_qrcode_ids))
        next_qrcode = random.choice(unvisited_qrcodes)

        # Check layouts to see where is the next QRCode
        today = datetime.today().strftime('%Y-%m-%d')
        try:
            layout = Layout.objects.get(period__start_date__lte=today,
                                        period__end_date__gte=today,
                                        qrcode=next_qrcode)

            # SUCCESS
            QRCodeAccess.objects.create(user=request.user, qrcode=next_qrcode)
            return Response(data=SpotSerializer(layout.spot).data)
        except Layout.DoesNotExist:
            return Response({"message": "Não existem QR Codes ativos de momento"}, status=403)

    except QRCode.DoesNotExist:
        return Response({"message": "QRCode inválido"}, status=404)
