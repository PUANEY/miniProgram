from rest_framework import serializers
from .models import NotifyModel


class NotifySerializers(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = NotifyModel
        fields = '__all__'
        depth = 1


