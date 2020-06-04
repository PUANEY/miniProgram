from .models import SearchRecordsModel, UserSearchRecordsModel
from rest_framework import serializers


class SearchRecordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchRecordsModel
        fields = '__all__'


class UserSearchRecordsSerializer(serializers.ModelSerializer):
    search_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserSearchRecordsModel
        fields = '__all__'
