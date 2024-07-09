from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Owner)
admin.site.register(Gym)
admin.site.register(Trainer)
admin.site.register(GymMember)
admin.site.register(PT)
