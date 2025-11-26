from django.urls import path
from .views import health, chat, conversations_list, conversation_detail

urlpatterns = [
    path("health/", health, name="Health"),
    path("chat/", chat, name="Chat"),
    path("conversations/", conversations_list, name="ConversationsList"),
    path("conversations/<int:pk>/", conversation_detail, name="ConversationDetail"),
]
