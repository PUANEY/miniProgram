from .models import FiveTaskModel
from rest_framework import serializers


class FiveTaskSerializers(serializers.ModelSerializer):
    pub_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = FiveTaskModel
        fields = '__all__'
        depth = 1
