from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    # PUBLIC_INTERFACE
    class Meta:
        model = Message
        fields = ["id", "conversation", "role", "content", "created_at"]
        read_only_fields = ["id", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation with nested messages (read-only).
    """
    messages = MessageSerializer(many=True, read_only=True)

    # PUBLIC_INTERFACE
    class Meta:
        model = Conversation
        fields = ["id", "title", "created_at", "updated_at", "messages"]
        read_only_fields = ["id", "created_at", "updated_at", "messages"]


class ChatRequestSerializer(serializers.Serializer):
    """
    Request payload for /api/chat.
    """
    conversation_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Existing conversation ID. Omit or null to start a new conversation.",
    )
    message = serializers.CharField(
        help_text="User message text to send to the chatbot.",
    )
    title = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        help_text="Optional title for a new conversation. Ignored if conversation_id is provided.",
    )

    # PUBLIC_INTERFACE
    def validate(self, attrs):
        """
        Validate combination of fields (no special rules now).
        """
        return super().validate(attrs)


class ChatResponseSerializer(serializers.Serializer):
    """
    Response payload for /api/chat, includes conversation_id and assistant reply.
    """
    conversation_id = serializers.IntegerField(help_text="The conversation ID for this chat turn.")
    reply = serializers.CharField(help_text="Assistant's response to the user's message.")
    conversation = ConversationSerializer(read_only=True, help_text="Optional conversation snapshot (when verbose).", required=False)

    # PUBLIC_INTERFACE
    def to_representation(self, instance):
        """
        Instance is expected to be a dict with keys:
        - conversation_id (int)
        - reply (str)
        - conversation (optional Conversation instance)
        """
        return super().to_representation(instance)
