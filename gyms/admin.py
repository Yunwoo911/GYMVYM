from django.contrib import admin
from .models import *

admin.site.register(Owner)
admin.site.register(Gym)
admin.site.register(Trainer)
admin.site.register(GymMember)
admin.site.register(PT)