from rest_framework import serializers
from .models import Approved, Pending, Rejected, Deleted


class PendingSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('more_data')

    def more_data(self, arg):
        return {"id": arg.id, "is_safe": arg.is_safe, "suggestion": arg.suggestion, "created": arg.created}

    class Meta:
        model = Pending
        fields = ('message', 'info')


class ApprovedSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('more_data')

    def more_data(self, arg):
        return {"id": arg.id, "is_safe": arg.is_safe, "suggestion": arg.suggestion, "created": arg.created, "by_api": arg.by_api}

    class Meta:
        model = Approved
        fields = ('message', 'info')


class RejectedSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('more_data')

    def more_data(self, arg):
        return {"id": arg.id, "is_safe": arg.is_safe, "suggestion": arg.suggestion, "created": arg.created, "by_api": arg.by_api, "reason": arg.reason}

    class Meta:
        model = Rejected
        fields = ('message', 'info')


class DeletedSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('more_data')

    def more_data(self, arg):
        return {"id": arg.id, "is_safe": arg.is_safe, "suggestion": arg.suggestion, "created": arg.created, "by_api": arg.by_api, "by": arg.by}

    class Meta:
        model = Deleted
        fields = ('message', 'info')
