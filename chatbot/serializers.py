from rest_framework import serializers
from .models import Chat, Message


class ProcessMessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    chat = serializers.HyperlinkedRelatedField(view_name='api:chat-detail', read_only=True)

    class Meta:
        model = Message
        fields = ('sender', 'chat', 'created', 'text')


class ChatListSerializer(serializers.HyperlinkedModelSerializer):
    message_log = serializers.HyperlinkedRelatedField(many=True, view_name='api:message-detail', read_only=True)
    detail = serializers.HyperlinkedIdentityField(view_name='api:chat-detail', read_only=True, source='id')

    class Meta:
        model = Chat
        fields = ('conversation_id', 'origin', 'created', 'detail', 'message_log')


class ChatDetailSerializer(serializers.HyperlinkedModelSerializer):
    message_log = serializers.HyperlinkedRelatedField(many=True, view_name='api:message-detail', read_only=True)
    full_log = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text', source='message_log')

    class Meta:
        model = Chat
        fields = ('conversation_id', 'origin', 'created', 'message_log', 'full_log')


class ChatSubmitSerializer(serializers.ModelSerializer):

    text = serializers.CharField(required=False)
    sender = serializers.CharField(required=False)

    class Meta:
        model = Chat
        fields = ('conversation_id', 'origin', 'text', 'sender')
        extra_kwargs = {
            'conversation_id': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        conv_id = validated_data.get('conversation_id')
        origin = validated_data.get('origin')
        text = self.context['request'].data.get('text')
        sender = self.context['request'].data.get('sender')
        instance, _ = self.Meta.model.objects.get_or_create(conversation_id=conv_id, origin=origin)
        instance.append_message(text, sender)
        return instance

    def is_valid(self, raise_exception=False):
        valid = super().is_valid(raise_exception)
        if not valid:
            return False

        messageserializer = MessageSerializer(data=self.context['request'].data)
        messageserializer.is_valid(raise_exception=True)
