
from users.models import Profile

from spots.models import QRCodeAccess


def get_user_ranking(user):
    return Profile.objects.filter(total_time__lt=user.profile.total_time,
                                  num_spots_read__gte=user.profile.num_spots_read).count() + 1
    # order_by('num_spots_read', 'total_time')


def update_total_spot_time(user):
    qrcode_accesses = list(QRCodeAccess.objects.filter(user=user, has_accessed=True))
    if len(qrcode_accesses) > 1:
        profile = user.profile
        time_delta = qrcode_accesses[-1].access_date - qrcode_accesses[0].access_date
        profile.total_time = time_delta.total_seconds()
        profile.save()


def update_total_spots_read(user):
    profile = user.profile
    num_spots_read = QRCodeAccess.objects.filter(user=user, has_accessed=True).count()
    profile.num_spots_read = num_spots_read
    profile.save()
