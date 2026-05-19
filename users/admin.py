from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Workout, Exercise, Set


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Set)