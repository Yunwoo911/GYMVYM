from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from account.models import CustomUser
from equipment.models import Equipment
from gyms.models import GymMember

class DataAnalysis(models.Model):
    analysis_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    equipment_use_time = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    fields = models.CharField(max_length=100, null=True)
>>>>>>> test
