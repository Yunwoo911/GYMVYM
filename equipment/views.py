from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Equipment, EquipmentReservation, TimeSlot
from django.utils import timezone
from datetime import datetime
from account.models import CustomUser
from .models import EquipmentInUse, EquipmentReservation
from datetime import datetime, timedelta

# 피크타임 예약
## 예약 페이지
def show_equipments(request):
    equipments = Equipment.objects.all()
    return render(request, "equipment/reservations_test.html", {"equipments": equipments})

## 예약 로직
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
            equipment=equipment,
            time_slot_id=time_slot_id
        ).exists():
            return JsonResponse({"message": "해당 타임슬롯에 이미 예약되었습니다."}, status=400)
        
        # 예약 정보를 EquipmentReservation 모델에 저장합니다.
        reservation = EquipmentReservation.objects.create(
            equipment=equipment,
            # user=request.user,  # 예약한 사용자 정보
            time_slot_id=time_slot_id  # time_slot_id 설정
        )
        
        # 예약 성공 메시지를 반환합니다.
        return JsonResponse({"message": "예약이 성공적으로 완료되었습니다.", "reservation_id": reservation.res_id})
    except Exception as e:
        # 기타 예외 발생 시 예약 실패 메시지를 반환합니다.
        return JsonResponse({"message": "예약 중 오류가 발생했습니다.", "error": str(e)}, status=500)

# nfc 태그를 통한 사용과 사용대기
def tag_equipment(request):
    # 운동기구에 nfc 태그 이벤트가 일어났을 때
    # 미사용중인 기구일 경우 바로 사용중으로 상태를 변경하고
    # 사용중인 기구일 경우 예약을 생성하는 함수

    # 1. 태그한 기구가 미사용중일 경우 equimentinuse 테이블에 바로 사용 정보 추가
    # 2. 태그한 기구가 사용중일 경우 equipmentreservation 테이블에 예약 정보 추가(res_start_time, res_end_time 포함)
    
    # 3. res_start_time이 됐을 때 equimentinuse 테이블에 추가
    # 4. res_end_time이 됐을 때 equimentinuse 테이블에서 삭제
    # 5. 매일 자정 equipmentreservation 테이블 초기화
    try:
        tag_user = CustomUser.objects.filter(user=request.user, nfc_uid=request.nfc_uid).first()
        # 현재 요청을 보낸 사용자(request.user)와 NFC UID(request.nfc_uid)를 사용하여 CustomUser 테이블에서 해당 사용자를 조회합니다.
        # filter() 메서드를 사용하여 조건에 맞는 사용자들을 필터링하고, first() 메서드를 사용하여 첫 번째 결과를 가져옵니다.
        if not tag_user:
            return JsonResponse({"message": "해당 사용자가 존재하지 않습니다."}, status=400)

        equipment = get_object_or_404(Equipment, equipment_id=request.equipment_id)
        # equipment_id에 해당하는 Equipment 객체를 조회합니다.
        # 만약 해당 equipment_id를 가진 Equipment 객체가 존재하지 않을 경우 404 에러를 반환합니다.

        is_using = EquipmentInUse.objects.filter(equipment_id=request.equipment_id, start_time__gte=timezone.now() - timedelta(hours=0.5), end_time__isnull=False) 
        # 기구가 사용중인지 확인 (start_time이 지금부터 30분전 안쪽인지, end_time이 비어있는지 확인)

        if is_using: # 태그한 기구가 사용중일 경우
            last_res  = EquipmentReservation.objects.filter(res_end_time = request.res_end_time).last() # 예약 테이블의 res_end_time 필드의 항목 중 마지막 항목
            last_res_end_time = last_res.res_end_time

            EquipmentReservation.objects.create(equipment_id = equipment.equipment_id, res_start_time = last_res_end_time, res_end_time = last_res_end_time + timedelta(hours=0.5))
            
        else: # 태그한 기구가 미사용중일 경우
            EquipmentInUse.objects.create(user_id = tag_user.user_id, equipment_id = equipment.equipment_id, start_time = timezone.now(), end_time = timezone.now() + timedelta(hours=0.5))
    
    except Exception as e:
        return JsonResponse({"message": "태그 중 오류가 발생했습니다.", "error": str(e)}, status=500)

def show_equipment_status(request):
    equipments = Equipment.objects.all()
    return render(request, "equipment/equipment_status.html", {"equipments": equipments})