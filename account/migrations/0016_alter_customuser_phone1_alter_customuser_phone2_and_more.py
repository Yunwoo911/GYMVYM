# Generated by Django 5.0.3 on 2024-07-29 05:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_customuser_phone1_alter_customuser_phone2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone1',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: 'OOO-OOOO-OOOO'.", regex='^\\d{3}-\\d{4}-\\d{4}$')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone2',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: 'OOO-OOOO-OOOO'.", regex='^\\d{3}-\\d{4}-\\d{4}$')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone3',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: 'OOO-OOOO-OOOO'.", regex='^\\d{3}-\\d{4}-\\d{4}$')]),
        ),
    ]