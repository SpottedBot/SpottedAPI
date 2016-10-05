from rest_framework import serializers
from .models import Spam, NotSpam


class SpamSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('more_data')

    def more_data(self, arg):
        return {"id": arg.id}

    class Meta:
        model = Spam
        fields = ('message', 'info')


class NotSpamSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('more_data')

    def more_data(self, arg):
        return {"id": arg.id}

    class Meta:
        model = NotSpam
        fields = ('message', 'info')
