from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Conversation
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from useraccount.models import User


@api_view(["GET"])
def conversations_list(request):
    serializer = ConversationListSerializer(
        request.user.conversations.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def coversations_detail(request, pk):
    conversation = request.user.conversations.get(pk=pk)
    conversation_serializer = ConversationDetailSerializer(conversation)
    message_serializer = ConversationMessageSerializer(
        conversation.messages.all(), many=True)
    return Response({"conversation": conversation_serializer.data,
                     "messages": message_serializer.data})


@api_view(["GET"])
def conversations_start(request, user_id):
    conversations = Conversation.objects.filter(
        users__in=[user_id]).filter(users__in=[request.user])
    if conversations.count() > 0:
        conversation = conversations.first()
        return Response({"success": True, "conversation_id": conversation.id})
    else:
        user = User.objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.users.add(request.user)
        conversation.users.add(user)
        return Response({"success": True, "conversation_id": conversation.id})