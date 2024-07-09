from django.db import models
from account.models import CustomUser

# 채팅방
class ChatRoom(models.Model):
    chatroom_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(CustomUser, related_name='chatrooms_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='chatrooms_as_user2', on_delete=models.CASCADE)
    chatroom_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # 채팅방 생성 시간
    updated_at = models.DateTimeField(auto_now=True) # 채팅방 최근 활동 시간

    # last_message = models.ForeignKey('Message', related_name='last_message_chatroom', on_delete=models.SET_NULL, null=True, blank=True) 
    # 채팅방의 마지막 메시지를 쉽게 확인

# 메시지
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE) #메시지를 보내는 사람    
    content = models.TextField() # 메시지 내용
    created_at = models.DateTimeField(auto_now_add=True) # 메시지 생성 시간
    is_read = models.BooleanField(default=False) # 읽음 여부 확인
# code review start