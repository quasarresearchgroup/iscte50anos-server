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

from spots.models import QRCode, QRCodeAccess, QRCodePermit, Layout, LayoutPeriod

from spots.serializers import SpotSerializer


@api_view()
@permission_classes([IsAuthenticated])
def get_or_create_permit(request):
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        permit = QRCodePermit.objects.get(user=request.user)
        try:
            layout = Layout.objects.get(period__start_date__lte=today,
                                        period__end_date__gte=today,
                                        qrcode=permit.qrcode)
            return Response(data=SpotSerializer(layout.spot).data)
        except Layout.DoesNotExist:
            return Response({"message": "Não existem QR Codes ativos de momento"}, status=403)
    except QRCodePermit.DoesNotExist:
        first_qrcode = random.choice(list(QRCode.objects.all()))
        try:
            layout = Layout.objects.get(period__start_date__lte=today,
                                        period__end_date__gte=today,
                                        qrcode=first_qrcode)

            QRCodePermit.objects.create(user=request.user, qrcode=first_qrcode)
            return Response(data=SpotSerializer(layout.spot).data)
        except Layout.DoesNotExist:
            return Response({"message": "Não existem QR Codes ativos de momento"}, status=403)




@api_view()
@permission_classes([IsAuthenticated])
@transaction.atomic
def access_qrcode(request, uuid):
    try:
        qrcode = QRCode.objects.get(uuid=uuid)
        has_access = QRCodeAccess.objects.filter(user=request.user, qrcode=qrcode).exists()
        num_accesses = QRCodeAccess.objects.filter(user=request.user).count()

        if num_accesses >= 4:
            return Response({"message": "Parabéns, visitaste todos os Spots!"}, status=200)

        if not has_access:
            has_permit = QRCodePermit.objects.filter(user=request.user, qrcode=qrcode).exists()
            if has_permit:

                QRCodeAccess.objects.create(user=request.user, qrcode=qrcode)
                qrcode_accesses = list(QRCodeAccess.objects.filter(user=request.user))
                visited_qrcode_ids = [access.qrcode.id for access in qrcode_accesses]
                unvisited_qrcodes = list(QRCode.objects.exclude(id__in=visited_qrcode_ids))

                # UPDATE STATS
                spots_controller.update_total_spots_read(request.user)
                spots_controller.update_total_spot_time(request.user)

                next_qrcode = random.choice(unvisited_qrcodes)

                # Check layouts to see where is the next QRCode
                today = datetime.today().strftime('%Y-%m-%d')
                try:
                    layout = Layout.objects.get(period__start_date__lte=today,
                                                period__end_date__gte=today,
                                                qrcode=next_qrcode)

                    # SUCCESS
                    QRCodePermit.objects.create(user=request.user, qrcode=next_qrcode)
                    QRCodePermit.objects.filter(user=request.user, qrcode=qrcode).delete()
                    return Response(data=SpotSerializer(layout.spot).data)
                except Layout.DoesNotExist:
                    return Response({"message": "Não existem QR Codes ativos de momento"}, status=403)
            else:
                return Response({"message": "Não podes aceder a este Spot ainda"}, status=403)
        else:
            return Response({"message": "Já visitaste este Spot"}, status=403)
    except QRCode.DoesNotExist:
        return Response({"message": "QRCode inválido"}, status=404)

