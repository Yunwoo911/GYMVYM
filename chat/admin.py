from django.contrib import admin
from chat.models import ChatRoom, Message
# Register your models here.
from .models import *

admin.site.register(ChatRoom)
admin.site.register(Message)
