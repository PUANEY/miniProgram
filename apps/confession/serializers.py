from rest_framework import serializers
from .models import PostModel, PostCommentModel, LikeNumModel


class PostSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = PostModel
        fields = '__all__'
        depth = 1


class PostCommentSerializers(serializers.ModelSerializer):
    pub_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = PostCommentModel
        fields = '__all__'
        depth = 1


class LikeNumSerializers(serializers.ModelSerializer):
    like_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = LikeNumModel
        fields = '__all__'
        depth = 1