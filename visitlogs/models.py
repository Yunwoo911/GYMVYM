from django.db import models
from gyms.models import GymMember

class VisitLog(models.Model): # 출입관리
    visitlog_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    nfc_uid = models.CharField(max_length=30, null=True)
    enter_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True)
    fields = models.CharField(max_length=100, null=True)