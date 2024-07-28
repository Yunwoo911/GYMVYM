from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Equipment, EquipmentReservation, TimeSlot
from django.utils import timezone
from datetime import datetime
from account.models import CustomUser
from gyms.models import GymMember
from .models import EquipmentInUse, EquipmentReservation
from datetime import datetime, timedelta
import json

# 피크타임 예약
# 수동 퇴장률에 따른 예약시간 배정
## 예약 페이지
# 프론트엔드에서 카테고리 별로 나눠서 보여주는 기능 필요
def show_equipments(request):
    #퇴장률별 예약 시작 시간 배정
    current_time = datetime.now() # 현재 시간
    exit_rate = int(request.user.manual_exit_rate) # 현재 로그인 한 유저의 퇴장률)
    '''
    exit_rate
    100% : 12시 이후
    90% 대  :  12시 1분 이후
    80% 대  :  12시 2분 이후
    70% 대  :  12시 3분 이후
    60% 대  :  12시 4분 이후
    50% 대  : 12시 5분 이후
    40% 대  :  12시 6분 이후
    30% 대  : 12시 7분 이후
    20% 대  :  12시 8분 이후
    10% 대  :  12시 9분 이후
    0% 대  :  12시 10분 이후
    '''
    if exit_rate == 100:
        # reservation_available_time = current_time.replace(hour=12, minute=0, second=0, microsecond=0)
        reservation_available_time = current_time
    else:
        # reservation_available_time = current_time.replace(hour=12, minute=10 - (exit_rate // 10), second=0, microsecond=0)
        reservation_available_time = current_time.replace(minute=current_time.minute + 10 - (exit_rate // 10))
    
    equipments = Equipment.objects.all() # 모든 운동 기구
    equipment_types = Equipment.objects.values_list('equipment_type', flat=True)
    equipment_type_list = equipment_types.distinct()
    context = {
        'equipment_type_list': equipment_type_list,
        'current_time': current_time,
        "equipments" : equipments,
        "reservation_available_time" : reservation_available_time,
    }
    return render(request, "equipment/reservations_test.html", context)

## 예약 로직
# 예약페이지에 접근할 수 없는 시간에 예약 로직이 작동하지 않도록 방지하는 방법 고민해보기
def reserve_equipment(request, equipment_id):
    try:
        # 주어진 equipment_id로 장비를 조회합니다.
        equipment = get_object_or_404(Equipment, equipment_id=equipment_id)
        
        # 요청에서 timeslot을 가져옵니다.
        timeslot = request.POST.get('timeslot')
        if not timeslot:
            return JsonResponse({"message": "타임슬롯이 제공되지 않았습니다."}, status=400)
        
        # timeslot 테이블에서 time_slot_id를 조회합니다.
        try:
            timeslot_obj = TimeSlot.objects.get(slot=timeslot)
            time_slot_id = timeslot_obj.timeslot_id
        except TimeSlot.DoesNotExist:
            return JsonResponse({"message": "해당 타임슬롯이 존재하지 않습니다."}, status=400)
        
        # 이미 예약된 장비인지 확인합니다.
        if EquipmentReservation.objects.filter(
            equipment_id=equipment.equipment_id,
            time_slot_id=time_slot_id
        ).exists():
            return JsonResponse({"message": "해당 타임슬롯에 이미 예약되었습니다."}, status=400)
        
        # 예약 정보를 EquipmentReservation 모델에 저장합니다.
        reservation = EquipmentReservation.objects.create(
            equipment_id=equipment.equipment_id,
            user_id=request.user.user,  # 예약한 회원의 user_id
            time_slot_id=time_slot_id  # time_slot_id 설정
        )
        
        # 예약 성공 메시지를 반환합니다.
        return JsonResponse({"message": "예약이 성공적으로 완료되었습니다.", "reservation_id": reservation.res_id})
    except Exception as e:
        # 기타 예외 발생 시 예약 실패 메시지를 반환합니다.
        return JsonResponse({"message": "예약 중 오류가 발생했습니다.", "error": str(e)}, status=500)

# nfc 태그를 통한 사용과 사용대기
    # 운동기구에 nfc 태그 이벤트가 일어났을 때
    # 미사용중인 기구일 경우 바로 사용중으로 상태를 변경하고
    # 사용중인 기구일 경우 예약을 생성하는 뷰

    # 1. 태그한 기구가 미사용중일 경우 equimentinuse 테이블에 바로 사용 정보 추가
    # 2. 태그한 기구가 사용중일 경우 equipmentreservation 테이블에 예약 정보 추가(res_start_time, res_end_time 포함)
    
    # 3. res_start_time이 됐을 때 equipmentreservation의 예약 정보를 equimentinuse에 사용 정보로 바꿔주기
    # 4. res_end_time이 됐을 때 equimentinuse 테이블에서 삭제
    # 5. 매일 자정 직전 equipmentreservation 테이블 초기화
def tag_equipment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # JSON 데이터를 파싱 / json.loads() 함수를 사용하여 JSON 문자열을 Python 딕셔너리로 변환
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)
        
        # NFC 리더기로 읽은 값과 고정값 가져오기
        reader_gym_id = data.get('gym_id') 
        reader_equipment_id = data.get('equipment_id')
        taged_nfc_uid = data.get('nfc_uid')
        
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

        equipment = get_object_or_404(Equipment, equipment_id=request.equipment_id)
        # equipment_id에 해당하는 Equipment 객체를 조회합니다.
        # 만약 해당 equipment_id를 가진 Equipment 객체가 존재하지 않을 경우 404 에러를 반환합니다.

        is_using = EquipmentInUse.objects.filter(equipment_id=reader_equipment_id,start_time__gte=timezone.now() - timedelta(hours=0.5), end_time__isnull=False)
        # 기구가 사용중인지 확인 (start_time이 지금부터 30분전 안쪽인지, end_time이 비어있는지 확인)

        if is_using: # 태그한 기구가 사용중일 경우
            last_res  = EquipmentReservation.objects.filter(res_end_time = request.res_end_time).last() # 예약 테이블의 res_end_time 필드의 항목 중 마지막 항목
            last_res_end_time = last_res.res_end_time

            EquipmentReservation.objects.create(equipment_id = equipment.equipment_id, res_start_time = last_res_end_time, res_end_time = last_res_end_time + timedelta(hours=0.5))
            
        else: # 태그한 기구가 미사용중일 경우
            EquipmentInUse.objects.create(user_id = which_user.user_id, equipment_id = equipment.equipment_id, start_time = timezone.now(), end_time = timezone.now() + timedelta(hours=0.5))
    
    return JsonResponse({"message": "태그 중 오류가 발생했습니다."}, status=500)

# 운동기구 사용 현황 표시
# 운동기구 type별로 3분할로 보여주기
def equipment_status(request):
    equipments = Equipment.objects.all()
    equipmentinuse_ids = EquipmentInUse.objects.values_list('equipment_id', flat=True)
    return render(request, "equipment/equipment_status.html", {"equipments": equipments, "equipmentinuse_ids": equipmentinuse_ids})

# 기구의 사용이 끝난 경우 inuse 테이블에서 삭제되도록 하는 로직 필요
# 예약 취소 기능 필요