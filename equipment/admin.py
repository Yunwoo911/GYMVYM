from django.contrib import admin
from .models import *

admin.site.register(Equipment)
admin.site.register(EquipmentInUse)
admin.site.register(EquipmentReservation)
