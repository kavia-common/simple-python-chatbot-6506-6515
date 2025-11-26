from typing import Optional

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ChatRequestSerializer,
    ChatResponseSerializer,
)


@api_view(["GET"])
def health(request):
    """
    Health check endpoint.

    Returns:
        200 OK with {"message": "Server is up!"}
    """
    return Response({"message": "Server is up!"})


def _rule_based_reply(user_text: str) -> str:
    """
    Very simple rule-based reply generator.

    - Greetings
    - Farewells
    - Contains '?' -> basic helpful answer
    - Fallback echo
    """
    text = user_text.strip().lower()
    if any(greet in text for greet in ["hello", "hi", "hey"]):
        return "Hello! How can I assist you today?"
    if any(bye in text for bye in ["bye", "goodbye", "see you"]):
        return "Goodbye! Have a great day!"
    if "help" in text:
        return "Sure, I'm here to help. Tell me more about what you need."
    if "?" in text:
        return "That's a great question! While I'm a simple bot, I suggest providing more details."
    if "weather" in text:
        return "I can't fetch live weather, but you can check your local forecast app."
    return f"You said: {user_text}"


@api_view(["POST"])
def chat(request):
    """
    Chat with the assistant.

    summary: Send a message and receive a rule-based assistant reply.
    description: |
      This endpoint accepts a user message and an optional conversation_id.
      If conversation_id is omitted or null, a new conversation is created.
      The user's message is stored, a simple rule-based reply is generated,
      and the assistant reply is stored and returned.

    requestBody:
      required: true
      content:
        application/json:
          schema: ChatRequestSerializer

    responses:
      200:
        description: Successful response with assistant reply.
        content:
          application/json:
            schema: ChatResponseSerializer
    """
    serializer = ChatRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    conversation: Optional[Conversation] = None
    conv_id = data.get("conversation_id", None)

    if conv_id is not None:
        conversation = get_object_or_404(Conversation, pk=conv_id)
    else:
        # Create a new conversation
        conversation = Conversation.objects.create(title=data.get("title", "") or "")

    # Save user message
    Message.objects.create(
        conversation=conversation,
        role=Message.ROLE_USER,
        content=data["message"],
    )

    # Generate assistant reply
    reply_text = _rule_based_reply(data["message"])

    # Save assistant message
    Message.objects.create(
        conversation=conversation,
        role=Message.ROLE_ASSISTANT,
        content=reply_text,
    )

    response_payload = {
        "conversation_id": conversation.id,
        "reply": reply_text,
        # Do not include full conversation by default to keep it lightweight.
    }
    response = ChatResponseSerializer(response_payload)
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def conversations_list(request):
    """
    List all conversations.

    summary: List conversations
    description: Returns a list of conversations with nested messages.
    """
    qs = Conversation.objects.all().order_by("-updated_at")
    serializer = ConversationSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def conversation_detail(request, pk: int):
    """
    Retrieve a single conversation by ID.

    summary: Conversation detail
    description: Returns a conversation and all associated messages.
    """
    conversation = get_object_or_404(Conversation, pk=pk)
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data)
