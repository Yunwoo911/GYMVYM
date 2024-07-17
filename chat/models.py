from django.db import models
from django.utils import timezone
from account.models import CustomUser

class ChatRoom(models.Model):
    chatroom_id = models.AutoField(primary_key=True)
    participant1 = models.ForeignKey(CustomUser, related_name='chatrooms_as_participant1', on_delete=models.CASCADE)  # 첫 번째 참여자
    participant2 = models.ForeignKey(CustomUser, related_name='chatrooms_as_participant2', on_delete=models.CASCADE)  # 두 번째 참여자
    chatroom_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간 필드: 자동으로 현재 시간 설정
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 시간 필드: 자동으로 현재 시간 설정

    def __str__(self):
        return f'ChatRoom {self.id}'

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)  # 채팅방 필드: ChatRoom과의 외래키 관계
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)  # 발신자 필드: CustomUser와의 외래키 관계
    content = models.TextField()  # 메시지 내용 필드: 텍스트 필드
    timestamp = models.DateTimeField(default=timezone.now)  # 타임스탬프 필드: 기본값으로 현재 시간 설정
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간 필드: 자동으로 현재 시간 설정
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 시간 필드: 자동으로 현재 시간 설정
    is_read = models.BooleanField(default=False)  # 메시지 읽음 상태 필드: 기본값은 False

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'