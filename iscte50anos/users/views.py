from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Profile

from users.serializers import ProfileSerializer, LeaderboardSerializer


@api_view()
@permission_classes([IsAuthenticated])
def get_profile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    return Response(status=200, data=serializer.data)


@api_view()
@permission_classes([IsAuthenticated])
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
        profile = {"name": f"{p.name()}", "points": p.points, "affiliation": p.affiliation.abbreviation}
        json_response.append(profile)
    return Response(data=json_response)


@api_view()
@permission_classes([IsAuthenticated])
def get_openday_leaderboard(request):
    user_type = request.GET.get("type")
    affiliation = request.GET.get("affiliation")

    if user_type and affiliation:
        if affiliation == "*":
            profiles = Profile.objects.filter(num_spots_read__gt=0,
                                              affiliation__subtype=user_type).order_by("-num_spots_read",
                                                                                       "total_time")[:10]
        else:
            profiles = Profile.objects.filter(num_spots_read__gt=0,
                                              affiliation__subtype=user_type,
                                              affiliation__name=affiliation).order_by("-num_spots_read",
                                                                                      "total_time")[:10]
    else:
        profiles = Profile.objects.filter(num_spots_read__gt=0).order_by("-num_spots_read", "total_time")[:10]

    serializer = LeaderboardSerializer(profiles, many=True)
    return Response(data=serializer.data)


'''@api_view()
@permission_classes([IsAuthenticated])
def get_openday_leaderboard_for_period(request):
    user_type = request.GET.get("type")
    affiliation = request.GET.get("affiliation")

    period = "2002-11-22"


    if user_type and affiliation:
        if affiliation == "*":
            profiles = Profile.objects.filter(num_spots_read__gt=0,
                                              affiliation__subtype=user_type).order_by("-num_spots_read", "total_time")[:10]

            participations = Participation.objects.filter(num_spots_read__gt=0,
                                                          user__profile__affiliation__subtype=user_type,
                                                          ).order_by("-num_spots_read", "total_time")[:10]

        else:
            profiles = Profile.objects.filter(num_spots_read__gt=0,
                                              affiliation__subtype=user_type,
                                              affiliation__name=affiliation).order_by("-num_spots_read", "total_time")[:10]

            participations = Participation.objects.filter(num_spots_read__gt=0,
                                                          user__profile__affiliation__subtype=user_type,
                                                          ).order_by("-num_spots_read", "total_time")[:10]
    else:
        profiles = Profile.objects.filter(num_spots_read__gt=0).order_by("-num_spots_read", "total_time")[:10]

    serializer = LeaderboardSerializer(profiles, many=True)
    return Response(data=serializer.data)'''



