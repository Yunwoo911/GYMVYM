from django.shortcuts import render
from django.http import JsonResponse
from .models import Event
from gyms.models import PT
import json

def calendar_view(request):

    # 로그인한 계정이 트레이너 계정일 경우에 
    if request.user.usertype == 1:
        gym_member = PT.objects.filter(trainer__user=request.user)

        return render(request, 'calendar.html', {'members': gym_member})

# 이벤트 데이터를 JSON 형태로 반환
def event_data(request):
    events = Event.objects.filter(pt__trainer__user=request.user) 
    events_json = [
        {
            'id': event.schedule_id,
            'title': event.title,
            'gym_member': str(event.pt.member.member_id),
            'start': event.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end.strftime('%Y-%m-%dT%H:%M:%S'),
            'description': event.description,
            'backgroundColor': event.background_color,
        } for event in events
    ]
    return JsonResponse(events_json, safe=False)

# 새로 추가된 이벤트 데이터를 저장
def save_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        for event in data:
            Event.objects.create(
                pt=PT.objects.filter(trainer__user=request.user, member__member_id=event['gym_member'])[0],
                title=event['title'],
                start=event['start'],
                end=event['end'],
                description=event['description'],
                background_color=event['backgroundColor']
            )
    return JsonResponse({'status': 'success'})


# 이벤트 삭제
def delete_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)        
        event_id = data.get('id')
        if event_id:
            Event.objects.filter(schedule_id=event_id).delete()            
    return JsonResponse({'status': 'success'})

