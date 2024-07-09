from django.db import models
from account.models import CustomUser

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    owner_name = models.CharField(max_length=100)

class Gym(models.Model):
    gym_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    gym_name = models.CharField(max_length=100)
    gym_address = models.CharField(max_length=255)

class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    trainer_name = models.CharField(max_length=100)
    certificate = models.CharField(max_length=100, null=True)
    trainer_image = models.ImageField(upload_to='trainer_images', null=True)

class GymMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    join_date = models.DateField()
    membership_type = models.CharField(max_length=100)
    expiry_date = models.DateField()
    recent_joined_date = models.DateField()
    recent_membership = models.CharField(max_length=100)
    recent_expiry = models.DateField()
    renewal_status = models.BooleanField(default=False)
    renewal_count = models.IntegerField(default=0)

class PT(models.Model):
    pt_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=100)
    registration_date = models.DateField()
    pt_end_date = models.DateField()
    duration = models.IntegerField()