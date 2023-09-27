from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from spots.models import Spot

from puzzle.models import Puzzle


@api_view(["POST"])
@transaction.atomic
@permission_classes([IsAuthenticated])
def submit_puzzle(request, spot_id):
    spot = Spot.objects.filter(id=spot_id).select_for_update().first()
    if spot is None:
        return Response(status=404, data={"status": "Spot does not exist"})

    if Puzzle.objects.filter(user=request.user, spot=spot).exists():
        return Response(status=400, data={"status": "This puzzle is already submitted"})

    Puzzle.objects.create(user=request.user, spot=spot)

    return Response(status=201, data={"status": "Puzzle submitted"})
