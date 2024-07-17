from django.shortcuts import render
from .models import VisitLog
from django.utils import timezone
from django.http import JsonResponse

# Create your views here.

# 현재 뷰의 문제점. 며칠 지난것도 퇴실이 가능할듯함

def web_exit(request):
    try:
        # user는 현재 요청을 보낸 유저
        user = request.user
        # visitlog는 현재 유저의 출입관리 중 아직 퇴실 시간이 없는 것 중 가장 최근에 입장한 기록
        visitlog = VisitLog.objects.get(member__user=user, exit_time__isnull=True, enter_time__date=timezone.now().date())
        # 퇴실 시간은 버튼을 누른 시간
        visitlog.exit_time = timezone.now()
        visitlog.save()
        return JsonResponse({'message': '출입관리 저장 성공'})
    except VisitLog.DoesNotExist:
        return JsonResponse({'message': '출입관리 저장 실패'})