from django.shortcuts import render
from .models import VisitLog
from django.utils import timezone
from django.http import JsonResponse

# Create your views here.

# 현재 뷰의 문제점. 며칠 지난것도 퇴실이 가능할듯함 <-timezone.now().date()로 해결?

def web_exit(request):
    if request.method == 'POST':
        try:
            # user는 요청을 보낸 유저
            user = request.user
            # VisitLog 모델에서 현재 로그인한 사용자의 출입 기록을 가져옵니다.
            # 조건: 
            # 1. member 필드의 user가 현재 요청을 보낸 사용자와 일치해야 합니다.
            # 2. exit_time 필드가 null이어야 합니다 (아직 퇴장하지 않은 기록).
            # 3. enter_time 필드의 날짜가 오늘이어야 합니다.
            visitlog = VisitLog.objects.get(member__user=user, exit_time__isnull=True, enter_time__date=timezone.now().date())
            # 퇴장 시간은 버튼을 누른 시점
            visitlog.exit_time = timezone.now()
            visitlog.save()
            return JsonResponse({'message': '퇴장이 완료되었습니다'})
        except VisitLog.DoesNotExist:
            return JsonResponse({'message': '출입 기록이 없습니다.'})   
    return JsonResponse({'message': '잘못된 요청'}, status=400)

# 자동퇴실