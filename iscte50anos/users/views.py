from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Profile

from users.serializers import ProfileSerializer


@api_view()
#@permission_classes([IsAuthenticated])
def get_profile(request):
    #profile = Profile.objects.get(user=request.user)
    #serializer = ProfileSerializer(profile)
    return Response(status=200)#data=serializer.data)

@api_view()
#@permission_classes([IsAuthenticated])
def get_leaderboard(request):
    user_type = request.GET.get("type")
    affiliation = request.GET.get("affiliation")

    if user_type and affiliation:
        if affiliation == "*":
            profiles = Profile.objects.filter(affiliation__type=user_type).order_by("-points")[:10]
        else:
            profiles = Profile.objects.filter(affiliation__type=user_type,
                                              affiliation__abbreviation=affiliation).order_by("-points")[:10]
    else:
        profiles = Profile.objects.order_by("-points")[:10]

    json_response = []
    for p in profiles:
        name = p.user.first_name
        surname = p.user.last_name
        last_name = ""
        if surname != "":
            last_name = surname.split()[-1]
        profile = {"name": f"{name} {last_name}", "points": p.points, "affiliation": p.affiliation.abbreviation}
        json_response.append(profile)
    return Response(data=json_response)



