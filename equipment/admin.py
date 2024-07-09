from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Equipment)
admin.site.register(EquipmentInUse)
admin.site.register(EquipmentReservation)
