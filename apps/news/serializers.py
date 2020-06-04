from rest_framework import serializers
from .models import NewsComment, Banner, NewsInfo, Tag


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class NewsCommentSerializers(serializers.ModelSerializer):
    pub_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = NewsComment
        fields = "__all__"
        depth = 1


class NewsSerializers(serializers.ModelSerializer):
    pub_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = NewsInfo
        fields = "__all__"
        depth = 1


class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
        depth = 1
