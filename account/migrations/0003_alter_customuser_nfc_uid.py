# Generated by Django 5.0.3 on 2024-07-21 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_gym_entry_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nfc_uid',
            field=models.CharField(blank=True, null=True, unique=True),
        ),
    ]