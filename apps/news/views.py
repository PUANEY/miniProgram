from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from .models import NewsInfo, NewsComment, Banner
from .serializers import NewsSerializers, NewsCommentSerializers, BannerSerializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()


class NewsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = NewsInfo.objects.all().order_by('-pub_time')
    serializer_class = NewsSerializers
    # 重写get方法，加速页面加载

    def list(self, request, *args, **kwargs):
        queryset = NewsInfo.objects.all().order_by('-pub_time')
        print(queryset)
        news_list = []
        data = {}
        for qs in queryset:
            ser = NewsSerializers(qs).data
            data["id"] = ser.get("id")
            data["title"] = ser.get("title")
            data["pub_time"] = ser.get("pub_time")
            data["image"] = ser.get("image")
            data["tag"] = ser.get("tag")
            news_list.append(data)
            data = {}
        return Response(news_list)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.visit += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NewsCommentViewSet(APIView):

    def get(self, request, news_id):
        comments = NewsComment.objects.filter(news_id=news_id)
        serializer = NewsCommentSerializers(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 哪个用户评论的: 获取用户名 username
        # 评论的是哪一篇文章： 获取文章id
        # 评论的内容是什么： 获取评论的content
        user_id = request.data['user_id']
        news_id = request.data['news_id']
        content = request.data['content']
        comment = NewsComment.objects.create(user_id=user_id, news_id=news_id, content=content)
        if comment:
            comment.save()
            return Response({"msg":"评论成功"}, status=status.HTTP_201_CREATED)
        return Response({"msg": "评论失败,请检查你的网络"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        comment_id = request.data['comment_id']
        if_comment = NewsComment.objects.get(id=comment_id)
        if if_comment:
            if_comment.delete()
            return Response({"msg": "删除成功!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"msg": "该评论已被删除!"}, status=status.HTTP_404_NOT_FOUND)


class BannerListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializers

