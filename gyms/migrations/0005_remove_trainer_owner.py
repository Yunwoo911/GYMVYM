# Generated by Django 5.0.4 on 2024-07-29 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0004_remove_trainer_owner_trainer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainer',
            name='owner',
        ),
    ]