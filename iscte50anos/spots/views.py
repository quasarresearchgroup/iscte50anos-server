import random
from datetime import datetime

from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from _controllers import spots_controller
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from topics.models import Topic, TopicAccess

from topics.serializers import TopicQRSerializer

from _controllers import quiz_controller

from spots.models import QRCode, QRCodeAccess, Layout, LayoutPeriod, Spot

from spots.serializers import SpotSerializer


@api_view()
def access_qrcode(request, uuid):
    is_app = request.GET.get("app", False)
    if is_app is False:
        source = request.META['HTTP_USER_AGENT']
        if "Android" in source:
            return redirect("https://play.google.com/store/apps/details?id=com.kiloo.subwaysurf")
        else:
            return redirect("https://apps.apple.com/us/app/subway-surfers/id512939461")

    qrcode = QRCode.objects.filter(uuid=uuid).select_related('topic').first()

    if qrcode is None:
        return Response(data={"error": "QR Code does not exist"}, status=404)

    return Response(data=TopicQRSerializer(qrcode.topic).data)

@api_view()
def get_spot_list(request):
    spots = Spot.objects.all()
    return Response(data=SpotSerializer(spots, many=True))

@api_view()
@permission_classes([IsAuthenticated])
@transaction.atomic
def open_day_get_or_create_permit(request):
    today = datetime.today().strftime('%Y-%m-%d')

    num_accesses = request.user.profile.num_spots_read
    if num_accesses >= 4:
        return Response({"message": "Parabéns, visitaste todos os Spots!"}, status=200)

    has_any_access = QRCodeAccess.objects.filter(user=request.user).exists()

    if not has_any_access:
        layouts = Layout.objects.prefetch_related('qrcode').filter(period__start_date__lte=today,
                                    period__end_date__gte=today)

        available_qrcodes = [layout.qrcode for layout in layouts]
        qrcode = random.choice(list(available_qrcodes))
        QRCodeAccess.objects.create(user=request.user, qrcode=qrcode)
    else:
        qrcode = QRCodeAccess.objects.filter(user=request.user, has_accessed=False).first().qrcode

    try:
        layout = Layout.objects.get(period__start_date__lte=today,
                                    period__end_date__gte=today,
                                    qrcode=qrcode)
        message = SpotSerializer(layout.spot).data
        message["spot_number"] = num_accesses + 1
        return Response(data=message)
    except Layout.DoesNotExist:
        return Response({"message": "Não existem QR Codes ativos de momento"}, status=400)


@api_view()
@permission_classes([IsAuthenticated])
@transaction.atomic
def open_day_access_qrcode(request, uuid):
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        qrcode = QRCode.objects.get(uuid=uuid)

        num_accesses = request.user.profile.num_spots_read
        if num_accesses >= 4:
            return Response({"message": "Parabéns, visitaste todos os Spots!"}, status=200)

        # Lock access to prevent data inconsistency
        access = QRCodeAccess.objects.select_for_update().filter(user=request.user, qrcode=qrcode).first()

        if access is None:
            return Response({"message": "Não podes aceder a este Spot ainda"}, status=400)
        elif access.has_accessed:
            return Response({"message": "Já visitaste este Spot"}, status=400)

        access.has_accessed = True
        access.save() # AUTO SAVES Date

        # UPDATE STATS
        spots_controller.update_total_spots_read(request.user)
        spots_controller.update_total_spot_time(request.user)

        if num_accesses >= 3:
            return Response({"message": "Parabéns, visitaste todos os Spots!"}, status=200)

        qrcode_accesses = list(QRCodeAccess.objects.select_related("qrcode").filter(user=request.user))
        visited_qrcodes = [access.qrcode for access in qrcode_accesses]

        layouts = Layout.objects.prefetch_related('qrcode').filter(period__start_date__lte=today,
                                                                   period__end_date__gte=today)

        available_qrcodes = [layout.qrcode for layout in layouts]
        unvisited_qrcodes = [qrcode for qrcode in available_qrcodes if qrcode not in visited_qrcodes]

        #unvisited_qrcodes = list(QRCode.objects.exclude(id__in=visited_qrcode_ids))

        next_qrcode = random.choice(unvisited_qrcodes)

        # Check layouts to see where is the next QRCode
        try:
            layout = Layout.objects.get(period__start_date__lte=today,
                                        period__end_date__gte=today,
                                        qrcode=next_qrcode)

            # SUCCESS
            QRCodeAccess.objects.create(user=request.user, qrcode=next_qrcode)
            message = SpotSerializer(layout.spot).data
            message["spot_number"] = num_accesses + 2
            return Response(data=message)
        except Layout.DoesNotExist:
            return Response({"message": "Não existem QR Codes ativos de momento"}, status=400)

    except QRCode.DoesNotExist:
        return Response({"message": "QRCode inválido"}, status=404)




