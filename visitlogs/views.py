from django.shortcuts import render
from .models import VisitLog
from django.utils import timezone
from django.http import JsonResponse
from gyms.models import GymMember
from django.shortcuts import get_object_or_404, redirect
import datetime

# 

# 현재 뷰의 문제점. 며칠 지난것도 퇴실이 가능할듯함 <-timezone.now().date()로 해결?

# 입실확인 뷰

# request.nfc_uid
from account.models import CustomUser
def web_entrance(request):
    if request.method == 'POST':
        # taged_nfc_uid = request.POST.get('nfc_uid')
        user = request.user
        taged_nfc_uid = user.nfc_uid
        # which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid)
        which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid,nickname=user.nickname)
        print(which_user)
        # enter_log = VisitLog.objects.create(member__user=visitor, enter_time=timezone.now())
        print(which_user.user)
        # which_member = GymMember.objects.get(user=which_user.user)  # GymMember 인스턴스를 가져옴
        which_member = GymMember.objects.get(user=which_user.user)
        print(which_member)
        real_enter_time = timezone.now()
        enter_exit_log = VisitLog.objects.create(member=which_member, enter_time=real_enter_time,exit_time=real_enter_time + datetime.timedelta(hours=2))
        enter_exit_log.save()
        return JsonResponse({'message': '입실이 완료되었습니다'})
    return JsonResponse({'message': '잘못된 요청'}, status=400)

def web_exit(request):
    if request.method == 'POST':
        try:
            # user는 요청을 보낸 유저
            user = request.user
            # VisitLog 모델에서 현재 로그인한 사용자의 출입 기록을 가져옵니다.
            # 조건: 어서오세요
            # 1. member 필드의 user가 현재 요청을 보낸 사용자와 일치해야 합니다. 
            # 2. exit_time 필드가 null이어야 합니다 (아직 퇴장하지 않은 기록).
            # 3. enter_time 필드의 날짜가 오늘이어야 합니다.
            # exit_log = VisitLog.objects.get(member__user=user, exit_time__isnull=True, enter_time__date=timezone.now().date())
            # entertime = VisitLog.objects.get(member__user=user)
            exit_log = VisitLog.objects.filter(member__user=user, exit_time__gte = timezone.now() - datetime.timedelta(hours=2)).last()
            # 퇴장 시간은 버튼을 누른 시점
            exit_log.exit_time = timezone.now()
            exit_log.save()
            return JsonResponse({'message': '퇴장이 완료되었습니다'})
        except VisitLog.DoesNotExist:
            return JsonResponse({'message': '출입 기록이 없습니다.'})   
    return JsonResponse({'message': '잘못된 요청'}, status=400)

def nfc_entrance(request):
    if request.method == 'POST':
        taged_nfc_uid = request.POST.get('nfc_uid')
        which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid)
        print(which_user)
        # enter_log = VisitLog.objects.create(member__user=visitor, enter_time=timezone.now())
        print(which_user.user)
        # which_member = GymMember.objects.get(user=which_user.user)  # GymMember 인스턴스를 가져옴
        which_member = GymMember.objects.get(user=which_user.user)
        print(which_member)
        real_enter_time = timezone.now()
        enter_exit_log = VisitLog.objects.create(member=which_member, enter_time=real_enter_time,exit_time=real_enter_time + datetime.timedelta(hours=2))
        enter_exit_log.save()
        return JsonResponse({'message': '입실이 완료되었습니다'})
    return JsonResponse({'message': '잘못된 요청'}, status=400)

def nfc_exit(request):
    if request.method == 'POST':
        try:
            taged_nfc_uid = request.POST.get('nfc_uid')
            which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid)
            # 조건: 어서오세요
            # 1. member 필드의 user가 현재 요청을 보낸 사용자와 일치해야 합니다. 
            # 2. exit_time 필드가 null이어야 합니다 (아직 퇴장하지 않은 기록).
            # 3. enter_time 필드의 날짜가 오늘이어야 합니다.
            # exit_log = VisitLog.objects.get(member__user=user, exit_time__isnull=True, enter_time__date=timezone.now().date())
            # entertime = VisitLog.objects.get(member__user=user)

            # member_id 수정 필요
            exit_log = VisitLog.objects.filter(member_id=which_user.member_id, exit_time__gte = timezone.now() - datetime.timedelta(hours=2)).last()
            # 퇴장 시간은 버튼을 누른 시점
            exit_log.exit_time = timezone.now()
            exit_log.save()
            return JsonResponse({'message': '퇴장이 완료되었습니다'})
        except VisitLog.DoesNotExist:
            return JsonResponse({'message': '출입 기록이 없습니다.'})   
    return JsonResponse({'message': '잘못된 요청'}, status=400)

# 자동퇴실
# def auto_exit(request):
#     pass

# def check_in(request, nfc_uid):
#     member = get_object_or_404(GymMember, nfc_uid=nfc_uid)
#     # 입장 로그 생성
#     VisitLog.objects.create(member=member, nfc_uid=nfc_uid, enter_time=timezone.now())
#     return JsonResponse({"status": "checked_in", "nfc_uid": nfc_uid})

# def check_out(request, nfc_uid):
#     member = get_object_or_404(GymMember, nfc_uid=nfc_uid)
#     visit_log = get_object_or_404(VisitLog, member=member, exit_time__isnull=True)
#     # 퇴장 시간 업데이트
#     visit_log.exit_time = timezone.now()
#     visit_log.save()
#     return JsonResponse({"status": "checked_out", "nfc_uid": nfc_uid})



# 예약, 입퇴실

# nfc 여진님이 진행중이셔서 그동안 다른 기구예약이나, 웹퇴실버튼, 자동퇴실



# 입퇴실 받는 고유번호를
# nfc_uid로 or user_id로

# 회원정보에 user_id
# nfc_uid 퇴실 인식필드로 사용하는쪽으로 가기로 했었는데

# 2단계 정도 건너뛰어서 말씀드림

# 커스텀유저 키로 받는가?
