from users.models import Profile

profiles = Profile.objects.all()
for p in profiles:
    p.num_spots_read = 0
    p.total_time = 0
    p.save()