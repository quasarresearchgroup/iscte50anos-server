from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Affiliation(models.Model):
    title = models.CharField(max_length=300, blank=True)
    '''type = models.CharField(
        max_length=10,
        choices=(("student", "Student"), ("professor", "Professor"), ("researcher", "Researcher"), ("staff", "Staff")),
        default="student"
    )
    cycle = models.CharField(
        max_length=3,
        choices=(("bsc", "Bachelor's"), ("msc", "Master's"), ("phd", "Doctorate"))
    )'''

    department = models.CharField(max_length=200, blank=True)

    # For open day
    '''subtype = models.CharField(max_length=50, blank=True)

    abbreviation = models.CharField(max_length=30, blank=True)
    full_description = models.CharField(max_length=100, blank=True)'''

    def full_description(self):
        return f'{self.title} em {self.department}'

    def __str__(self):
        return self.full_description()


class Profile(models.Model):
    # name, surname, email, username in django User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    affiliation = models.ForeignKey(Affiliation, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    # For beta test
    num_spots_read = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    is_logged = models.BooleanField(default=False)

    def name(self):
        last_name = ""
        surname = self.user.last_name
        if surname != "":
            last_name = surname.split()[-1]
        return f"{self.user.first_name} {last_name}"

    def username(self):
        return self.user.username

    def affiliation_name(self):
        if self.affiliation:
            return f"{self.affiliation.full_description()}"
        return "Sem afiliação"

    def ranking(self):
        return Profile.objects.exclude(points=0).filter(points__gt=self.points).count() + 1

    def affiliation_ranking(self):
        return Profile.objects.exclude(points=0).filter(affiliation=self.affiliation,
                                                        points__gt=self.points).count() + 1

    def initials(self):
        if self.user.first_name:
            return self.user.first_name[0]
        return "?"
        #"".join([name[0] for name in self.name().split(" ")])

    def open_day_ranking(self):
        return Profile.objects.exclude(num_spots_read=0).filter(num_spots_read__gt=self.num_spots_read).count() + \
               Profile.objects.exclude(num_spots_read=0).filter(num_spots_read=self.num_spots_read,
                                                                total_time__lt=self.total_time).count() + 1

    def open_day_affiliation_ranking(self):
        return Profile.objects.exclude(num_spots_read=0).filter(affiliation=self.affiliation,
                                                                num_spots_read__gt=self.num_spots_read).count() + \
               Profile.objects.exclude(num_spots_read=0).filter(affiliation=self.affiliation,
                                                                num_spots_read=self.num_spots_read,
                                                                total_time__lt=self.total_time).count() + 1

    def __str__(self):
        return f'{self.user.username}'

    # For leaderboard and ranking performance
    class Meta:
        indexes = [
            # models.Index(fields=['num_spots_read', '-total_time']),
            models.Index(fields=['points']),
        ]


class Level(models.Model):
    number = models.IntegerField()
    num_topics = models.IntegerField()
    question_score = models.IntegerField()

    def __str__(self):
        return "Level " + str(self.number)
