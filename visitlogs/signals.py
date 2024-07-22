from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import VisitLog
import datetime

@receiver(post_save, sender=VisitLog)
def auto_checkout(sender, instance, **kwargs):
    if instance.exit_time is None:  # 이미 퇴실 처리된 로그는 무시
        now = timezone.now()
        auto_exit_time = datetime.timedelta(hours=2)
        if now - instance.enter_time > auto_exit_time:
            instance.exit_time = now
            instance.save()
