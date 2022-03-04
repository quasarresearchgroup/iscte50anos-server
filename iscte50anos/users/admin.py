from django.contrib import admin

# Register your models here.
from users.models import Affiliation, Profile, Level

admin.site.register(Affiliation)
admin.site.register(Profile)
admin.site.register(Level)