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
        return JsonResponse({'message': '입장이 완료되었습니다'})
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
        reader_gym_id = request.POST.get('gym_id') # 입실 리더기에 고정된 gym_id를 가져온다.
        taged_nfc_uid = request.POST.get('nfc_uid') # 입실 리더기로 읽은 휴대폰의 nfc_uid를 가져온다.
        
        if not reader_gym_id: # reader_gym_id 없으면 에러
            return JsonResponse({'error': '헬스장 id가 없습니다.'}, status=400)
        if not taged_nfc_uid: # taged_nfc_uid 없으면 에러
            return JsonResponse({'error': 'nfc_uid가 없습니다.'}, status=400)
        
        try:
            which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid) # customuser 테이블에서 taged_nfc_uid로 어떤 유저인지 찾는다.
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': '해당 nfc_uid를 가진 사용자가 없습니다.'}, status=404)
        
        try:
            # which_member = GymMember.objects.get(gym_id=reader_gym_id, user=which_user.user)  # gymmember 테이블에서 gym_id와 user로 멤버인지 찾는다.
            # gymmember 상에서의 중복 오류 해결하기 전까지 임시 방편
            which_member = GymMember.objects.filter(gym_id=reader_gym_id, user=which_user.user).last()
        except GymMember.DoesNotExist:
            return JsonResponse({'error': '해당 헬스장에 등록된 사용자가 아닙니다.'}, status=404)

        nfc_enter_time = timezone.now() # 현재 시간
        # 입실 기록 생성 + 2시간 후 퇴실 정보 저장
        enter_log = VisitLog.objects.create(nfc_uid=taged_nfc_uid, enter_time=nfc_enter_time, exit_time=nfc_enter_time + datetime.timedelta(hours=2), member=which_member.member_id)
        enter_log.save()
        return JsonResponse({'message': '입실이 완료되었습니다'})
    return JsonResponse({'error': '잘못된 요청'}, status=400)

def nfc_exit(request):
    if request.method == 'POST':
        try:
            # nfc 리더기로 부터 온 nfc_uid랑 gym_id
            taged_nfc_uid = request.POST.get('nfc_uid')
            reader_gym_id = request.POST.get('gym_id')
            
            # taged_user는 CustomUser 테이블에서 태그된 nfc_uid가 일치하는 유저 객체를 가져온다.
            taged_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid)
            # GymMember 테이블에서 
            gym_member_id = GymMember.objects.get(user=taged_user.user, gym_id=reader_gym_id).member_id
            # exit_log는 VisitLog 테이블에서 퇴실기록(자동퇴실: 입장시간으로부터 2시간 뒤), 이 현재 시간에서 2시간 이내에 퇴장 기록이 없으면.
            exit_log = VisitLog.objects.filter(member_id=gym_member_id, exit_time__gte = timezone.now() - datetime.timedelta(hours=2)).last()
            # 퇴장 시간은 버튼을 누른 시점
            exit_log.exit_time = timezone.now()
            # 퇴장 기록 DB에 저장
            exit_log.save()
            return JsonResponse({'message': '퇴장이 완료되었습니다'})
        except VisitLog.DoesNotExist:
            return JsonResponse({'message': '입장 기록이 없습니다.'})   
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
