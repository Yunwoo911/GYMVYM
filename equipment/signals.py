from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EquipmentReservation, EquipmentInUse
from django.utils import timezone

@receiver(post_save, sender=EquipmentReservation)
def create_equipment_in_use(sender, instance, **kwargs):
    if instance.res_start_time <= timezone.now():
        EquipmentInUse.objects.get_or_create(
            user_id=instance.user_id,
            equipment_id=instance.equipment_id,
            start_time=instance.res_start_time,
            end_time=instance.res_end_time
        )