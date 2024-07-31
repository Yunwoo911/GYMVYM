from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import EquipmentReservation, EquipmentInUse
import logging

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_reservations, 'interval', seconds=10)  # 30초마다 실행
    scheduler.start()

def check_reservations():
    now = timezone.now() # 현재시간 < 지금보다 
    reservations = EquipmentReservation.objects.filter(res_start_time__lte=now, res_end_time__gte=now)
    for reservation in reservations:
        try:
            EquipmentInUse.objects.get_or_create(
                user_id=reservation.user_id,
                equipment_id=reservation.equipment_id,
                start_time=reservation.res_start_time,
                end_time=reservation.res_end_time
            )
            logger.info(f"Reservation {reservation.res_id} processed successfully.")
        except Exception as e:
            logger.error(f"Error processing reservation {reservation.res_id}: {e}")