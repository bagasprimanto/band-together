from django.contrib import admin
from .models import Profile, ProfileType, Genre, Skill


admin.site.register(Profile)
admin.site.register(ProfileType)
admin.site.register(Genre)
admin.site.register(Skill)
