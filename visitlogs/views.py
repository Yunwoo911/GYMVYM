from django.shortcuts import render
from .models import VisitLog
from django.utils import timezone
from django.http import JsonResponse
from gyms.models import GymMember
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

# 현재 뷰의 문제점. 며칠 지난것도 퇴실이 가능할듯함 <-timezone.now().date()로 해결?

# 입실확인 뷰

# request.nfc_uid
from account.models import CustomUser
def nfc_entrance(request):
    # 입구 리더기에서 온 nfc_uid
    # 해당 nfc_uid를 CustomUser의 nfc_uid를 대조해서 입장한 유저를 확인
    # visitlog 테이블에 enter_time에 nfc카드를 찍은 시간을 저장
    # visitlog 테이블에 member 필드는 그 유저의 헬스장의 헬스장 회원 id

    if request.method == 'POST':
        nfc_uid = request.POST.get('nfc_uid') 
        visitor = CustomUser.objects.get(nfc_uid=nfc_uid)
        enter_log = VisitLog.objects.create(member__user=visitor, enter_time=timezone.now())
        enter_log.save()
        return JsonResponse({'message': '입실이 완료되었습니다'})
    return JsonResponse({'message': '잘못된 요청'}, status=400)

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
            exit_log = VisitLog.objects.get(member__user=user, exit_time__isnull=True, enter_time__date=timezone.now().date())
            # 퇴장 시간은 버튼을 누른 시점
            exit_log.exit_time = timezone.now()
            exit_log.save()
            return JsonResponse({'message': '퇴장이 완료되었습니다'})
        except VisitLog.DoesNotExist:
            return JsonResponse({'message': '출입 기록이 없습니다.'})   
    return JsonResponse({'message': '잘못된 요청'}, status=400)

# 자동퇴실

def auto_exit(request):
    
    pass


def check_in(request, nfc_uid):
    member = get_object_or_404(GymMember, nfc_uid=nfc_uid)
    # 입장 로그 생성
    VisitLog.objects.create(member=member, nfc_uid=nfc_uid, enter_time=timezone.now())
    return JsonResponse({"status": "checked_in", "nfc_uid": nfc_uid})

def check_out(request, nfc_uid):
    member = get_object_or_404(GymMember, nfc_uid=nfc_uid)
    visit_log = get_object_or_404(VisitLog, member=member, exit_time__isnull=True)
    # 퇴장 시간 업데이트
    visit_log.exit_time = timezone.now()
    visit_log.save()
    return JsonResponse({"status": "checked_out", "nfc_uid": nfc_uid})
