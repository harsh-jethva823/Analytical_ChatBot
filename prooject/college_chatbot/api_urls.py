from django.urls import path
from . import api_views

urlpatterns = [
    path('chat/', api_views.chat_message, name='chat_message'),
    path('conversation/<str:session_id>/', api_views.get_conversation, name='get_conversation'),
]