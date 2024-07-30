from django.contrib import admin
from .models import VisitLog

@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('visitlog_id', 'member', 'nfc_uid', 'enter_time', 'exit_time', 'is_checked_out')
    list_filter = ('enter_time', 'exit_time')
    search_fields = ('member__name', 'nfc_uid')
