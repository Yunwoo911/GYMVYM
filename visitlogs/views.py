from django.shortcuts import render
from .models import VisitLog
from django.utils import timezone
from django.http import JsonResponse

def web_exit(request):
    if request.method == 'POST':
        try:
            user = request.user
            visitlog = VisitLog.objects.get(member__user=user, exit_time__isnull=True, enter_time__date=timezone.now().date())
            visitlog.exit_time = timezone.now()
            visitlog.save()
            return JsonResponse({'message': '퇴장이 완료되었습니다'})
        except VisitLog.DoesNotExist:
            return JsonResponse({'message': '출입 기록이 없습니다.'})
    return JsonResponse({'message': '잘못된 요청'}, status=400)
